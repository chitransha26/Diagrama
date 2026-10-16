import CoreGraphics
import PencilKit
import Testing
@testable import Diagrama

struct InkSamplingTests {
    /// A real PencilKit stroke along `points` (canvas points), as the learner's finger makes it.
    private func stroke(_ points: [CGPoint]) -> PKStroke {
        PKStroke(ink: PKInk(.pen, color: .black), path: PKStrokePath(
            controlPoints: points.enumerated().map { i, p in
                PKStrokePoint(location: p, timeOffset: Double(i) * 0.01, size: CGSize(width: 2, height: 2),
                              opacity: 1, force: 1, azimuth: 0, altitude: .pi / 2)
            },
            creationDate: .now))
    }

    /// At 4x zoom a line drawn slightly beside the guide, but well within the on-screen
    /// tolerance, must count. Reading the ink too sparsely used to leave gaps between ink
    /// points, so the step could never finish (the butterfly's cycle arrows).
    @Test(arguments: [1.0, 2.0, 4.0])
    func lineBesideGuideCountsAtEveryZoom(zoom: CGFloat) {
        let canvasSide: CGFloat = 318, scale = canvasSide / DiagramSpace.size
        let tolerance = StrokeScorer.tolerance(isPencil: false, scale: scale * zoom)
        // 9 pt off the guide on screen; the finger tolerance is 10 pt.
        let offset = 9 / (scale * zoom)
        let guide = Polyline(points: [CGPoint(x: 600, y: 700), CGPoint(x: 700, y: 700)], closed: false)
        let ink = stroke([CGPoint(x: 600 * scale, y: (700 + offset) * scale), CGPoint(x: 700 * scale, y: (700 + offset) * scale)])
        let r = StrokeScorer.score(strokes: ink.diagramSegments(scale: scale), guides: [guide], tolerance: tolerance)
        #expect(StrokeScorer.isComplete(r), "coverage \(r.guideCoverage), gap \(r.longestGap)")
    }
}
