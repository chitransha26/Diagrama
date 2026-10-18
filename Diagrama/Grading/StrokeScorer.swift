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
    static let recallPrecisionPass = 0.75

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
        guard let aligned = align(strokes, to: guides) else { return .empty }
        return score(strokes: aligned, guides: guides, tolerance: tolerance * recallLeeway)
    }

    /// Copy and memory drawings get this much more leeway than tracing: parts are placed by eye.
    static let recallLeeway: CGFloat = 1.5
    /// Every part must be at least this well matched, so no part (say, the arrows) can be skipped.
    static let recallPartPass = 0.5
    /// Parts smaller than this (diagram units), like a hen's comb, are details: they count
    /// toward the overall match but aren't required one by one.
    static let recallDetailSize: CGFloat = 50
    /// A stroke at least this long (diagram units) that mostly runs nowhere near the picture is
    /// a stray line.
    static let strayLength: CGFloat = 60
    /// A long stroke whose average distance from the picture, after fitting, is more than this
    /// share of the leeway is a stray line.
    static let strayFit: CGFloat = 0.33

    /// Judges a copy or from-memory drawing part by part: every part drawn, no stray lines.
    /// `details` (legs, veins, wing lines) belong to the picture, so ink on them is fine and
    /// they set its size, but they aren't required one by one.
    static func judgeRecall(strokes: [[CGPoint]], parts: [(name: String, guides: [Polyline])],
                            details: [Polyline] = [], tolerance: CGFloat) -> RecallVerdict {
        let guides = parts.flatMap(\.guides)
        let picture = guides + details
        guard let aligned = align(strokes, to: picture) else { return RecallVerdict(result: .empty, missing: parts.map(\.name), strayLines: 0) }
        let reach = tolerance * recallLeeway
        // Learners place and size each piece by eye, so each stroke may shift and stretch a
        // little to its best fit. It can't rotate, so a line that matches nothing stays off.
        let field = DistanceField(picture)
        let fitted = aligned.map { fit($0, to: field, reach: reach) }
        var result = score(strokes: fitted, guides: guides, tolerance: reach)
        // Ink on inner details counts as on the picture too.
        let ink = fitted.flatMap { $0 }
        let off = ink.filter { field.distance($0) > reach }
        result.offGuidePoints = off
        result.precision = Double(ink.count - off.count) / Double(max(ink.count, 1))
        var missing: [String] = []
        var i = 0
        for part in parts {
            let share = result.guideCoverage[i..<(i + part.guides.count)]
            let size = part.guides.map(\.bounds).reduce(CGRect.null) { $0.union($1) }
            if max(size.width, size.height) >= recallDetailSize, share.reduce(0, +) / Double(max(share.count, 1)) < recallPartPass { missing.append(part.name) }
            i += part.guides.count
        }
        let stray = fitted.filter { stroke in
            guard stroke.count > 1, Polyline(points: stroke, closed: false).length >= strayLength else { return false }
            // Even at its best fit it runs loosely beside things rather than along them.
            // (Measured: real copied strokes average under 13 units off; scribbles 19 to 35.)
            let mean = stroke.reduce(CGFloat(0)) { $0 + field.distance($1) } / CGFloat(stroke.count)
            return mean > reach * strayFit
        }.count
        return RecallVerdict(result: result, missing: missing, strayLines: stray)
    }

    /// How far a stroke may move (diagram units) and stretch while fitting.
    static let fitShift: CGFloat = 90
    static let fitScales: [CGFloat] = [0.75, 0.9, 1, 1.1, 1.3]

    /// Moves and stretches one stroke (no rotation) to where it best matches the picture.
    private static func fit(_ stroke: [CGPoint], to field: DistanceField, reach: CGFloat) -> [CGPoint] {
        guard stroke.count > 1 else { return stroke }
        let step = max(1, stroke.count / 24)
        let sample = stride(from: 0, to: stroke.count, by: step).map { stroke[$0] }
        let c = CGPoint(x: stroke.map(\.x).reduce(0, +) / CGFloat(stroke.count),
                        y: stroke.map(\.y).reduce(0, +) / CGFloat(stroke.count))
        func moved(_ p: CGPoint, _ sx: CGFloat, _ sy: CGFloat, _ dx: CGFloat, _ dy: CGFloat) -> CGPoint {
            CGPoint(x: c.x + (p.x - c.x) * sx + dx, y: c.y + (p.y - c.y) * sy + dy)
        }
        func cost(_ sx: CGFloat, _ sy: CGFloat, _ dx: CGFloat, _ dy: CGFloat) -> CGFloat {
            let total = sample.reduce(CGFloat(0)) { $0 + min(field.distance(moved($1, sx, sy, dx, dy)), reach * 3) }
            // A slight preference for leaving the stroke as drawn, when fits are equal.
            return total / CGFloat(sample.count) + (abs(dx) + abs(dy)) * 0.01 + (abs(sx - 1) + abs(sy - 1)) * 0.5
        }
        var best = (sx: CGFloat(1), sy: CGFloat(1), dx: CGFloat(0), dy: CGFloat(0), cost: cost(1, 1, 0, 0))
        let shifts = stride(from: -fitShift, through: fitShift, by: 30)
        for sx in fitScales { for sy in fitScales { for dx in shifts { for dy in shifts {
            let k = cost(sx, sy, dx, dy)
            if k < best.cost { best = (sx, sy, dx, dy, k) }
        } } } }
        let coarse = best
        for ddx in stride(from: CGFloat(-15), through: 15, by: 5) {
            for ddy in stride(from: CGFloat(-15), through: 15, by: 5) {
                let k = cost(coarse.sx, coarse.sy, coarse.dx + ddx, coarse.dy + ddy)
                if k < best.cost { best = (coarse.sx, coarse.sy, coarse.dx + ddx, coarse.dy + ddy, k) }
            }
        }
        return stroke.map { moved($0, best.sx, best.sy, best.dx, best.dy) }
    }

    private static func align(_ strokes: [[CGPoint]], to guides: [Polyline]) -> [[CGPoint]]? {
        let ink = strokes.flatMap { $0 }
        let ref = CGRect.enclosing(guides.flatMap(\.points))
        let drawn = CGRect.enclosing(ink)
        guard ink.count > 1, drawn.width > 1, drawn.height > 1 else { return nil }
        let sx = ref.width / drawn.width, sy = ref.height / drawn.height
        return strokes.map { stroke in
            stroke.map { CGPoint(x: ref.midX + ($0.x - drawn.midX) * sx, y: ref.midY + ($0.y - drawn.midY) * sy) }
        }
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

/// Distance from any point to the nearest line of a picture, precomputed on a grid so that
/// fitting many strokes stays fast.
struct DistanceField {
    private let cell: CGFloat = 4
    private let n = 300   // covers -100...1100, a margin around the 1000-unit diagram
    private let origin: CGFloat = -100
    private var values: [Float]

    init(_ lines: [Polyline]) {
        let n = self.n, cell = self.cell, origin = self.origin
        var v = [Float](repeating: .greatestFiniteMagnitude, count: n * n)
        for line in lines {
            for p in line.resampled(spacing: cell / 2) {
                let i = Int(((p.x - origin) / cell).rounded()), j = Int(((p.y - origin) / cell).rounded())
                if i >= 0, i < n, j >= 0, j < n { v[j * n + i] = 0 }
            }
        }
        // Two-pass chamfer distance transform.
        let a = Float(cell), d = Float(cell * 1.4142)
        for j in 0..<n {
            for i in 0..<n {
                var x = v[j * n + i]
                if i > 0 { x = min(x, v[j * n + i - 1] + a) }
                if j > 0 {
                    x = min(x, v[(j - 1) * n + i] + a)
                    if i > 0 { x = min(x, v[(j - 1) * n + i - 1] + d) }
                    if i < n - 1 { x = min(x, v[(j - 1) * n + i + 1] + d) }
                }
                v[j * n + i] = x
            }
        }
        for j in stride(from: n - 1, through: 0, by: -1) {
            for i in stride(from: n - 1, through: 0, by: -1) {
                var x = v[j * n + i]
                if i < n - 1 { x = min(x, v[j * n + i + 1] + a) }
                if j < n - 1 {
                    x = min(x, v[(j + 1) * n + i] + a)
                    if i < n - 1 { x = min(x, v[(j + 1) * n + i + 1] + d) }
                    if i > 0 { x = min(x, v[(j + 1) * n + i - 1] + d) }
                }
                v[j * n + i] = x
            }
        }
        values = v
    }

    func distance(_ p: CGPoint) -> CGFloat {
        let fi = (p.x - origin) / cell, fj = (p.y - origin) / cell
        let i = min(max(Int(fi.rounded()), 0), n - 1), j = min(max(Int(fj.rounded()), 0), n - 1)
        // Outside the grid, add how far outside the point is.
        let outside = hypot(max(0, abs(fi - CGFloat(i)) - 0.5), max(0, abs(fj - CGFloat(j)) - 0.5)) * cell
        return CGFloat(values[j * n + i]) + outside
    }
}

/// How a copy or from-memory drawing went, part by part.
struct RecallVerdict {
    var result: TraceResult
    /// Parts drawn too little to count (or not at all).
    var missing: [String]
    /// Long strokes that don't match anything in the picture.
    var strayLines: Int

    var passed: Bool { missing.isEmpty && strayLines == 0 && StrokeScorer.recallPassed(result) }
}
