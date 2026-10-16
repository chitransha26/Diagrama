import CoreGraphics

/// Drawing-execution feedback (PRD §05): how well strokes follow a guide.
/// This never decides scientific correctness — that is graded separately.
struct TraceResult: Equatable {
    /// Share of the learner's ink that stayed within tolerance of the guide.
    var precision: Double
    /// Share of the guide that the learner's ink covered.
    var coverage: Double
    /// Ink points that strayed off the guide, in diagram space.
    var offGuidePoints: [CGPoint]

    var score: Double { (precision + coverage) / 2 }

    static let empty = TraceResult(precision: 0, coverage: 0, offGuidePoints: [])
}

enum StrokeScorer {
    /// Coverage needed to complete a guided trace.
    static let tracePass = 0.8
    /// Below this precision, more ink is off the guide than on it: suggest restarting the step.
    static let restartBelow = 0.5
    /// Recall drawings are rougher, so they are aligned first and judged more loosely.
    static let recallCoveragePass = 0.6
    static let recallPrecisionPass = 0.5

    /// Tolerance in diagram units. Fingers and capacitive styluses get a wider band than
    /// pens (PRD §05), measured in on-screen points so it feels the same on every device.
    static func tolerance(isPencil: Bool, scale: CGFloat) -> CGFloat {
        let points: CGFloat = isPencil ? 8 : 12
        return max(points / max(scale, 0.01), 12)
    }

    static func score(strokes: [[CGPoint]], guides: [Polyline], tolerance: CGFloat) -> TraceResult {
        let ink = strokes.flatMap { $0 }
        guard !ink.isEmpty, !guides.isEmpty else { return .empty }

        var off: [CGPoint] = []
        for p in ink where guides.map({ $0.distance(from: p) }).min()! > tolerance {
            off.append(p)
        }

        let samples = guides.flatMap { $0.resampled(spacing: 10) }
        let covered = samples.filter { s in ink.contains { $0.distance(to: s) <= tolerance } }.count

        return TraceResult(
            precision: Double(ink.count - off.count) / Double(ink.count),
            coverage: samples.isEmpty ? 0 : Double(covered) / Double(samples.count),
            offGuidePoints: off
        )
    }

    /// Scores a from-memory drawing. Position and size are up to the learner, so the
    /// drawing's bounding box is first mapped onto the reference before comparing.
    static func scoreRecall(strokes: [[CGPoint]], guides: [Polyline], tolerance: CGFloat) -> TraceResult {
        let ink = strokes.flatMap { $0 }
        let ref = CGRect.enclosing(guides.flatMap(\.points))
        let drawn = CGRect.enclosing(ink)
        guard ink.count > 1, drawn.width > 1, drawn.height > 1 else { return .empty }

        let sx = ref.width / drawn.width, sy = ref.height / drawn.height
        let aligned = strokes.map { stroke in
            stroke.map { CGPoint(x: ref.midX + ($0.x - drawn.midX) * sx, y: ref.midY + ($0.y - drawn.midY) * sy) }
        }
        return score(strokes: aligned, guides: guides, tolerance: tolerance * 2)
    }

    /// How steady the line is, 0...1, from how far each point wobbles off the line through
    /// its neighbours. Takes strokes in on-screen points, so it means the same on any device.
    static func smoothness(strokes: [[CGPoint]]) -> Double {
        var wobble: [CGFloat] = []
        for s in strokes where s.count >= 3 {
            for i in 1..<(s.count - 1) {
                wobble.append(s[i].distance(to: s[i - 1].lerp(to: s[i + 1], 0.5)))
            }
        }
        guard !wobble.isEmpty else { return 1 }
        let mean = wobble.reduce(0, +) / CGFloat(wobble.count)
        return Double(max(0, min(1, 1 - (mean - 0.2) / 1.5)))
    }

    static func recallPassed(_ r: TraceResult) -> Bool {
        r.coverage >= recallCoveragePass && r.precision >= recallPrecisionPass
    }
}
