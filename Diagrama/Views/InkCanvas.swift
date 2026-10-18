import PencilKit
import SwiftUI
import UIKit.UIGestureRecognizerSubclass

/// PencilKit canvas that accepts fingers, capacitive styluses and Apple Pencil (PRD §07).
/// The tool is set by the lesson, never picked by the learner. Reports each change to the
/// ink (a new stroke, or an erase) and the kind of touch behind it.
struct InkCanvas: UIViewRepresentable {
    @Binding var drawing: PKDrawing
    var tool: PKTool
    var isEnabled = true
    /// For zoomed tracing: the canvas stays exactly the size of its box and zooms its own
    /// content (PencilKit's built-in zoom), so nothing overflows onto the toolbar around it.
    /// Stroke coordinates stay in unzoomed canvas space, whatever the zoom.
    var viewport: Viewport = .whole
    /// Two-finger pinch to zoom and pan, for free drawing without guides. One finger draws.
    var allowsZoom = false
    /// Called when the learner lifts the pen, finger or eraser.
    var onLift: () -> Void = {}
    var onChange: (_ added: Bool, _ isPencil: Bool) -> Void

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    /// Applies the requested zoom once the canvas knows its size.
    final class Canvas: PKCanvasView {
        var target: Viewport = .whole
        var fixedZoom = false
        private var applied: (CGFloat, CGPoint, CGSize)?

        #if DEBUG
        /// The last laid-out canvas width and zoom, for the trace recorder.
        nonisolated(unsafe) static var lastLayout: (width: CGFloat, zoom: CGFloat) = (0, 1)
        #endif

        override func layoutSubviews() {
            super.layoutSubviews()
            applyTarget()
            #if DEBUG
            Self.lastLayout = (bounds.width, zoomScale)
            #endif
        }

        func applyTarget() {
            guard fixedZoom, bounds.width > 0 else { return }
            let key = (target.zoom, target.origin, bounds.size)
            if let a = applied, a.0 == key.0, a.1 == key.1, a.2 == key.2 { return }
            applied = key
            if zoomScale != 1 { setZoomScale(1, animated: false) }
            contentSize = bounds.size
            minimumZoomScale = 1
            maximumZoomScale = max(1, target.zoom)
            setZoomScale(target.zoom, animated: false)
            let unit = bounds.width / DiagramSpace.size * target.zoom
            contentOffset = CGPoint(x: target.origin.x * unit, y: target.origin.y * unit)
        }
    }

    func makeUIView(context: Context) -> Canvas {
        let view = Canvas()
        view.drawingPolicy = .anyInput
        view.backgroundColor = .clear
        view.isOpaque = false
        view.overrideUserInterfaceStyle = .light
        view.tool = tool
        view.isScrollEnabled = false
        view.minimumZoomScale = 1
        view.maximumZoomScale = 1
        view.contentInsetAdjustmentBehavior = .never
        view.drawing = drawing
        view.delegate = context.coordinator
        view.accessibilityLabel = "Drawing area"

        let recorder = TouchTypeRecorder()
        view.addGestureRecognizer(recorder)
        context.coordinator.recorder = recorder
        return view
    }

    func updateUIView(_ view: Canvas, context: Context) {
        context.coordinator.parent = self
        view.isUserInteractionEnabled = isEnabled
        view.tool = tool
        view.isScrollEnabled = allowsZoom
        if viewport.zoom > 1 {
            // Guided, app-controlled zoom: the learner doesn't pan or pinch.
            view.fixedZoom = true
            view.target = viewport
            view.applyTarget()
        } else {
            view.fixedZoom = false
            view.maximumZoomScale = allowsZoom ? 4 : 1
            if !allowsZoom, view.zoomScale != 1 { view.setZoomScale(1, animated: true) }
            if view.zoomScale == 1, view.contentSize != view.bounds.size { view.contentSize = view.bounds.size }
        }
        if view.drawing != drawing {
            view.drawing = drawing
        }
    }

    final class Coordinator: NSObject, PKCanvasViewDelegate {
        var parent: InkCanvas
        var recorder: TouchTypeRecorder?

        init(_ parent: InkCanvas) {
            self.parent = parent
        }

        func canvasViewDrawingDidChange(_ canvasView: PKCanvasView) {
            let new = canvasView.drawing
            guard new != parent.drawing else { return }
            let added = new.strokes.count > parent.drawing.strokes.count
            // A stroke can finish just after the step locks; drop it.
            if added, !parent.isEnabled {
                canvasView.drawing = parent.drawing
                return
            }
            parent.drawing = new
            parent.onChange(added, recorder?.lastType == .pencil)
        }

        func canvasViewDidEndUsingTool(_ canvasView: PKCanvasView) {
            parent.onLift()
        }
    }
}

/// Watches touches without interfering, to tell pencil strokes from finger strokes.
final class TouchTypeRecorder: UIGestureRecognizer {
    private(set) var lastType: UITouch.TouchType = .direct

    init() {
        super.init(target: nil, action: nil)
        cancelsTouchesInView = false
        delaysTouchesBegan = false
        delaysTouchesEnded = false
    }

    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent) {
        if let t = touches.first { lastType = t.type }
    }

    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent) { state = .failed }
    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent) { state = .failed }
}

/// The eraser rubs out just the ink it passes over, like a real eraser, rather than
/// deleting whole strokes.
enum Eraser {
    static let tool = PKEraserTool(.bitmap, width: 16)

    /// The same on-screen size at any zoom (canvas units are magnified by the zoom).
    static func tool(zoom: CGFloat) -> PKEraserTool { PKEraserTool(.bitmap, width: 16 / max(zoom, 1)) }
}

extension PKStroke {
    /// The parts of the stroke still visible, in on-screen points. Partly erased strokes are
    /// masked rather than cut, so only the unmasked ranges count.
    var visibleScreenSegments: [[CGPoint]] { visibleSegments(spacing: 3) }

    private func visibleSegments(spacing: CGFloat) -> [[CGPoint]] {
        let ranges: [ClosedRange<CGFloat>?] = mask == nil ? [nil] : maskedPathRanges.map { $0 }
        return ranges
            .map { r in path.interpolatedPoints(in: r, by: .distance(spacing)).map { $0.location.applying(transform) } }
            .filter { !$0.isEmpty }
    }

    /// The visible parts of the stroke in diagram space, read densely: zoom magnifies the
    /// gaps between points, and at 4x a sparser reading left gaps wider than the tolerance.
    func diagramSegments(scale: CGFloat) -> [[CGPoint]] {
        visibleSegments(spacing: 0.5).map { $0.map { CGPoint(x: $0.x / scale, y: $0.y / scale) } }
    }
}

extension PKDrawing {
    /// Renders the ink as it looks on the white canvas, regardless of dark mode.
    func lightImage(side: CGFloat) -> UIImage {
        var image = UIImage()
        UITraitCollection(userInterfaceStyle: .light).performAsCurrent {
            image = self.image(from: CGRect(x: 0, y: 0, width: side, height: side), scale: 2)
        }
        return image
    }
}
