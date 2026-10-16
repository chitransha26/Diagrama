import PencilKit
import SwiftUI

/// One finished step's ink. Like ArtWorkout, every step draws on its own layer, created for
/// the learner, so erasing in one step can't damage another. Learners never see layers.
struct InkLayer {
    let drawing: PKDrawing
    /// Side of the canvas the ink was drawn on, which spans the whole diagram square.
    let canvasSide: CGFloat
    /// The ink over the whole diagram, for unzoomed views.
    let image: UIImage
}

/// The result of one guided tracing step, for the scorecard.
struct TraceRecord {
    let match: Double
    let smoothness: Double
    /// Finished without undo, erasing or restarting.
    let firstTry: Bool
}

/// State for one run through a lesson.
@Observable
final class LessonSession {
    let lesson: Lesson
    private(set) var index = 0
    private(set) var finished = false
    let startedAt = Date()
    private(set) var finishedAt: Date?

    /// Parts drawn so far: structure IDs for outlines, "id.details" for inner detail.
    var revealed: Set<String> = []
    /// Filled outlines, as "structureID#outlineIndex".
    var filled: Set<String> = []
    private(set) var layers: [InkLayer] = []
    @ObservationIgnored private var cropCache: [String: UIImage] = [:]

    private(set) var traces: [TraceRecord] = []
    private(set) var scienceTotal = 0
    private(set) var scienceFirstTry = 0
    /// Topics answered wrongly on the first try.
    private(set) var review: [String] = []
    var recallPassed = false

    init(lesson: Lesson) {
        self.lesson = lesson
    }

    var step: LessonStep { lesson.steps[index] }
    var progress: Double { Double(index) / Double(lesson.steps.count) }

    func addLayer(_ drawing: PKDrawing, canvasSide: CGFloat) {
        guard !drawing.strokes.isEmpty, canvasSide > 0 else { return }
        layers.append(InkLayer(drawing: drawing, canvasSide: canvasSide, image: drawing.lightImage(side: canvasSide)))
    }

    /// A layer's ink re-rendered sharply for just the part of the diagram a zoomed step shows.
    func layerImage(_ i: Int, crop: CGRect, pointsWide: CGFloat) -> UIImage {
        let key = "\(i)|\(crop.debugDescription)|\(Int(pointsWide))"
        if let cached = cropCache[key] { return cached }
        let layer = layers[i]
        let unit = layer.canvasSide / DiagramSpace.size
        let rect = CGRect(x: crop.minX * unit, y: crop.minY * unit, width: crop.width * unit, height: crop.height * unit)
        var image = UIImage()
        UITraitCollection(userInterfaceStyle: .light).performAsCurrent {
            image = layer.drawing.image(from: rect, scale: 2 * pointsWide / rect.width)
        }
        cropCache[key] = image
        return image
    }

    func recordTrace(_ record: TraceRecord) {
        traces.append(record)
    }

    /// Records a scientific check. Only the first try counts toward the score.
    func recordScience(correct: Bool, topic: String) {
        scienceTotal += 1
        if correct { scienceFirstTry += 1 } else { review.append(topic) }
    }

    func advance() {
        if index + 1 < lesson.steps.count {
            index += 1
        } else {
            finishedAt = .now
            finished = true
        }
    }

    // MARK: Scorecard (ArtWorkout's Match /1000, Smoothness /300, First try /50, Time)

    var match: Int? { average(\.match).map { Int(($0 * 1000).rounded()) } }
    var smoothness: Int? { average(\.smoothness).map { Int(($0 * 300).rounded()) } }
    var firstTry: Int? {
        traces.isEmpty ? nil : Int((Double(traces.filter(\.firstTry).count) / Double(traces.count) * 50).rounded())
    }
    var duration: TimeInterval { (finishedAt ?? .now).timeIntervalSince(startedAt) }

    private func average(_ key: KeyPath<TraceRecord, Double>) -> Double? {
        traces.isEmpty ? nil : traces.map { $0[keyPath: key] }.reduce(0, +) / Double(traces.count)
    }

    func makeRecord() -> AttemptRecord {
        AttemptRecord(
            lessonID: lesson.id, date: .now, match: match, smoothness: smoothness, firstTry: firstTry,
            duration: duration, scienceCorrect: scienceFirstTry, scienceTotal: scienceTotal,
            independent: recallPassed
        )
    }
}
