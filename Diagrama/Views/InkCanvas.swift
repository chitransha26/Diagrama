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
    var onChange: (_ added: Bool, _ isPencil: Bool) -> Void

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    func makeUIView(context: Context) -> PKCanvasView {
        let view = PKCanvasView()
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

    func updateUIView(_ view: PKCanvasView, context: Context) {
        context.coordinator.parent = self
        view.isUserInteractionEnabled = isEnabled
        view.tool = tool
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

extension PKStroke {
    /// The stroke's points in on-screen points.
    var screenPoints: [CGPoint] {
        path.interpolatedPoints(by: .distance(3)).map { $0.location.applying(transform) }
    }

    /// The stroke's points in diagram space.
    func diagramPoints(scale: CGFloat) -> [CGPoint] {
        path.interpolatedPoints(by: .distance(3)).map {
            let p = $0.location.applying(transform)
            return CGPoint(x: p.x / scale, y: p.y / scale)
        }
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
