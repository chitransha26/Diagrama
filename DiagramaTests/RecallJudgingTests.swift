import CoreGraphics
import Foundation
import Testing
@testable import Diagrama

/// Copy and from-memory drawings: judged on shapes and layout, but every part must be there
/// and stray lines don't pass. (A chicken copy with scribbles and no arrows once passed.)
struct RecallJudgingTests {
    let lesson = Catalog.lesson(id: "g3-chicken-life-cycle")!
    var parts: [(name: String, guides: [Polyline])] { lesson.structures.map { ($0.name, $0.outlines) } }
    /// A 330 pt canvas, drawn with a finger.
    let tolerance = StrokeScorer.tolerance(isPencil: false, scale: 330 / DiagramSpace.size)

    /// Each outline drawn as one stroke, as a learner copying carefully would.
    var clean: [[CGPoint]] { parts.flatMap(\.guides).map { $0.resampled(spacing: 3) } }

    /// Every part placed a little off by eye, with a shaky hand. Fixed offsets, so the test
    /// gives the same answer every run.
    var handDrawn: [[CGPoint]] {
        clean.enumerated().map { i, stroke in
            let dx = CGFloat((i * 37) % 81 - 40), dy = CGFloat((i * 53) % 81 - 40)
            return stroke.enumerated().map { j, p in
                CGPoint(x: p.x + dx + CGFloat((j * 7) % 17 - 8), y: p.y + dy + CGFloat((j * 11) % 17 - 8))
            }
        }
    }

    func judge(_ strokes: [[CGPoint]]) -> RecallVerdict {
        StrokeScorer.judgeRecall(strokes: strokes, parts: parts, tolerance: tolerance)
    }

    @Test func faithfulCopiesPass() {
        #expect(judge(clean).passed)
        #expect(judge(clean.map { $0.map { CGPoint(x: 200 + $0.x * 0.6, y: 300 + $0.y * 0.6) } }).passed, "smaller and off-center")
        let v = judge(handDrawn)
        #expect(v.passed, "placed by eye: missing \(v.missing), stray \(v.strayLines), precision \(v.result.precision)")
    }

    @Test func aMissingPartFails() {
        let arrows = lesson.structure("arrows").outlines
        let withoutArrows = zip(clean, parts.flatMap(\.guides)).filter { !arrows.contains($0.1) }.map(\.0)
        let v = judge(withoutArrows)
        #expect(!v.passed)
        #expect(v.missing == [lesson.structure("arrows").name])
    }

    @Test func tinyDetailsArentRequiredOneByOne() {
        let comb = lesson.structure("comb").outlines
        let withoutComb = zip(clean, parts.flatMap(\.guides)).filter { !comb.contains($0.1) }.map(\.0)
        #expect(judge(withoutComb).passed)
    }

    @Test func aStrayLineFails() {
        let scribble = (0...120).map { i in CGPoint(x: 250 + Double(i) * 4, y: 750 - Double(i) * 4) }
        let v = judge(clean + [scribble])
        #expect(!v.passed)
        #expect(v.strayLines == 1)
    }

    /// Legs and wing lines are part of the picture: drawing them must not count against you.
    @Test func innerDetailsCountAsPartOfThePicture() {
        let beetles = Catalog.lesson(id: "g3-beetle-variation")!
        let parts = beetles.structures.map { ($0.name, $0.outlines) }
        let details = beetles.structures.flatMap(\.details)
        let ink = (parts.flatMap(\.1) + details).map { $0.resampled(spacing: 3) }
        let v = StrokeScorer.judgeRecall(strokes: ink, parts: parts, details: details, tolerance: tolerance)
        #expect(v.passed, "precision \(v.result.precision), missing \(v.missing), stray \(v.strayLines)")
    }

    /// Like a real copy: the rows drawn close together and each beetle drawn taller, by eye.
    /// Placement and size are the learner's; the shapes are right, so it passes.
    @Test func aCopyWithItsOwnSpacingPasses() {
        let beetles = Catalog.lesson(id: "g3-beetle-variation")!
        let parts = beetles.structures.map { ($0.name, $0.outlines) }
        let details = beetles.structures.flatMap(\.details)
        let ink = (parts.flatMap(\.1) + details).map { line -> [CGPoint] in
            line.resampled(spacing: 3).map { p in
                let bottomRow = p.y > 500
                // Each beetle 25% taller around its own middle; the bottom row moved up 250.
                let mid: CGFloat = bottomRow ? 720 : 300
                return CGPoint(x: p.x, y: mid + (p.y - mid) * 1.25 - (bottomRow ? 250 : 0))
            }
        }
        let start = Date()
        let v = StrokeScorer.judgeRecall(strokes: ink, parts: parts, details: details, tolerance: tolerance)
        #expect(v.passed, "precision \(v.result.precision), missing \(v.missing), stray \(v.strayLines)")
        // Runs when the learner taps Check, so it must feel instant.
        #expect(Date().timeIntervalSince(start) < 1, "took \(Date().timeIntervalSince(start)) s")
    }
}
