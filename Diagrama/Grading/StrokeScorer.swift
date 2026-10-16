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
    /// Coverage of each guide on its own, so no single part can be skipped.
    var guideCoverage: [Double] = []
    /// The longest untraced stretch of any guide, in diagram units.
    var longestGap: CGFloat = 0
    /// Points along the guides that still need tracing, in diagram space.
    var untraced: [CGPoint] = []

    var score: Double { (precision + coverage) / 2 }

    static let empty = TraceResult(precision: 0, coverage: 0, offGuidePoints: [])
}

enum StrokeScorer {
    /// Every guide must be at least this fully traced to complete a step, as in ArtWorkout,
    /// where a drawing isn't finished until every line is drawn.
    static let guidePass = 0.96
    /// The longest untraced stretch allowed, in diagram units: about the width of a pen line.
    static let maxGap: CGFloat = 16
    /// Below this precision, more ink is off the guide than on it: suggest restarting the step.
    static let restartBelow = 0.5
    /// Recall drawings are rougher, so they are aligned first and judged more loosely.
    static let recallCoveragePass = 0.6
    static let recallPrecisionPass = 0.5

    private static let sampleSpacing: CGFloat = 8
    /// Shapes this small (diagram units) are dots: a quick dab draws them, as on paper.
    static let dotSize: CGFloat = 24
    /// Ink counted toward a part must span at least this share of the part, so ink near one
    /// end (say, an arrow's tip) can't complete a whole small part like the arrowhead.
    static let minimumSpan = 0.6

    static func isDot(_ g: Polyline) -> Bool { max(g.bounds.width, g.bounds.height) <= dotSize }

    /// How far ink may stray from a guide, in on-screen points. Fingers and capacitive
    /// styluses get a wider band than pens (PRD §05).
    static let fingerTolerance: CGFloat = 10
    static let pencilTolerance: CGFloat = 6

    /// Tolerance in diagram units for the current zoom. It's fixed on screen, so zooming in
    /// makes it tighter on the diagram, never looser on screen.
    static func tolerance(isPencil: Bool, scale: CGFloat) -> CGFloat {
        (isPencil ? pencilTolerance : fingerTolerance) / max(scale, 0.01)
    }

    /// A trace is complete only when every guide is fully drawn, with no real gaps, and
    /// most of the ink is on the guide.
    static func isComplete(_ r: TraceResult) -> Bool {
        !r.guideCoverage.isEmpty
            && r.guideCoverage.allSatisfy { $0 >= guidePass }
            && r.longestGap <= maxGap
            && r.precision >= restartBelow
    }

    static func score(strokes: [[CGPoint]], guides: [Polyline], tolerance: CGFloat) -> TraceResult {
        let ink = strokes.flatMap { $0 }
        guard !ink.isEmpty, !guides.isEmpty else { return .empty }

        // Each ink point counts only toward the guide it is closest to, so one line drawn
        // between two close guides can't trace both.
        var off: [CGPoint] = []
        var inkByGuide = Array(repeating: [CGPoint](), count: guides.count)
        for p in ink {
            let distances = guides.map { $0.distance(from: p) }
            let nearest = distances.indices.min { distances[$0] < distances[$1] }!
            if distances[nearest] > tolerance {
                off.append(p)
            } else {
                inkByGuide[nearest].append(p)
            }
        }

        var perGuide: [Double] = []
        var untraced: [CGPoint] = []
        var longestGap: CGFloat = 0
        var totalSamples = 0, totalCovered = 0
        for (g, guide) in guides.enumerated() {
            let samples = guide.resampled(spacing: sampleSpacing)
            let corners = sharpCorners(guide)
            // Hands and pens round off sharp corners (a tail tip, an arrow point), so the tip
            // itself gets a little more leeway than the rest of the line.
            let covered = samples.map { s -> Bool in
                let nearCorner = corners.contains { $0.distance(to: s) <= tolerance * 2.5 }
                let reach = nearCorner ? tolerance * 2 : tolerance
                return inkByGuide[g].contains { $0.distance(to: s) <= reach }
            }
            var count = covered.filter { $0 }.count
            if !isDot(guide) {
                let extent = max(guide.bounds.width, guide.bounds.height)
                let ink = CGRect.enclosing(inkByGuide[g])
                let span = inkByGuide[g].isEmpty ? 0 : max(ink.width, ink.height)
                let spanShare = Double(span / max(extent, 1)) / minimumSpan
                if spanShare < 1 { count = Int(Double(count) * spanShare) }
            }
            perGuide.append(samples.isEmpty ? 1 : Double(count) / Double(samples.count))
            untraced += zip(samples, covered).filter { !$0.1 }.map(\.0)
            longestGap = max(longestGap, CGFloat(longestRun(of: false, in: covered, wraps: guide.closed)) * guide.length / CGFloat(max(samples.count, 1)))
            totalSamples += samples.count
            totalCovered += count
        }

        return TraceResult(
            precision: Double(ink.count - off.count) / Double(ink.count),
            coverage: totalSamples == 0 ? 0 : Double(totalCovered) / Double(totalSamples),
            offGuidePoints: off,
            guideCoverage: perGuide,
            longestGap: longestGap,
            untraced: untraced
        )
    }

    /// Points where a guide turns sharply (more than 60 degrees), like a tail tip or arrow point.
    static func sharpCorners(_ guide: Polyline) -> [CGPoint] {
        let p = guide.points
        guard p.count >= 3 else { return guide.closed ? [] : [] }
        var result: [CGPoint] = []
        let range = guide.closed ? Array(p.indices) : Array(1..<(p.count - 1))
        for i in range {
            let a = p[(i - 1 + p.count) % p.count], b = p[i], c = p[(i + 1) % p.count]
            let v1 = CGPoint(x: b.x - a.x, y: b.y - a.y), v2 = CGPoint(x: c.x - b.x, y: c.y - b.y)
            let l1 = hypot(v1.x, v1.y), l2 = hypot(v2.x, v2.y)
            guard l1 > 0, l2 > 0 else { continue }
            let cosTurn = (v1.x * v2.x + v1.y * v2.y) / (l1 * l2)
            if cosTurn < 0.5 { result.append(b) }   // turn sharper than 60 degrees
        }
        return result
    }

    /// Longest run of `value` in `flags`, treating closed shapes as a loop.
    private static func longestRun(of value: Bool, in flags: [Bool], wraps: Bool) -> Int {
        guard !flags.isEmpty else { return 0 }
        if flags.allSatisfy({ $0 == value }) { return flags.count }
        let seq = wraps ? flags + flags : flags
        var best = 0, run = 0
        for f in seq {
            run = f == value ? run + 1 : 0
            best = max(best, run)
        }
        return min(best, flags.count)
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
