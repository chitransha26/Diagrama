import PencilKit
import SwiftUI

/// Free drawing of a Lewis structure around printed atom symbols. The drawing is read as a
/// bond graph and checked scientifically; there are no guides and no electron counter.
struct LewisDrawStepView: View {
    @Bindable var session: LessonSession
    let step: LewisStep

    @State private var drawing = PKDrawing()
    @State private var erasing = false
    @State private var side: CGFloat = 0
    @State private var issues: [String] = []
    @State private var checks = 0
    @State private var passed = false

    var body: some View {
        VStack(spacing: 10) {
            DrawingToolbar(
                pen: .pen, erasing: $erasing, canUndo: !drawing.strokes.isEmpty, enabled: !passed,
                onUndo: { if !drawing.strokes.isEmpty { drawing.strokes.removeLast(); issues = [] } },
                onRestart: { drawing = PKDrawing(); issues = [] }
            )

            SquareStage { side in
                ZStack {
                    PrintedAtoms(atoms: step.target.atoms, positions: step.positions)
                    InkCanvas(
                        drawing: $drawing,
                        tool: erasing ? Eraser.tool : Pen.pen.tool(scale: side / DiagramSpace.size),
                        isEnabled: !passed,
                        onLift: { if erasing { DispatchQueue.main.async { erasing = false } } }
                    ) { _, _ in issues = [] }
                }
                .onAppear { self.side = side }
                .onChange(of: side) { _, new in self.side = new }
            }

            VStack(alignment: .leading, spacing: 6) {
                if passed {
                    FeedbackRow(kind: .correct, text: "Correct, from memory. Every atom has a full outer shell, and all \(step.target.valenceElectrons) valence electrons are placed.")
                } else if issues.isEmpty {
                    FeedbackRow(kind: .info, text: "Lines between atoms are bonds. Pairs of dots beside an atom are lone pairs.")
                } else {
                    ForEach(issues.prefix(2), id: \.self) { FeedbackRow(kind: .wrong, text: $0) }
                }
            }
            .frame(height: 112, alignment: .top)

            HStack {
                Spacer()
                if passed || checks >= 3 {
                    ContinueButton {
                        session.recallPassed = passed
                        session.advance()
                    }
                    .frame(maxWidth: 200)
                } else {
                    ContinueButton(title: "Check", enabled: !drawing.strokes.isEmpty) { check() }
                        .frame(maxWidth: 200)
                }
            }
        }
    }

    private func check() {
        guard side > 0 else { return }
        let scale = side / DiagramSpace.size
        let reading = LewisInterpreter.read(
            strokes: drawing.strokes.flatMap { $0.diagramSegments(scale: scale) },
            atoms: step.target.atoms, positions: step.positions
        )
        let found = reading.notes + ChemistryValidator.issues(in: reading.molecule, target: step.target)
        checks += 1
        if checks == 1 {
            session.recordScience(correct: found.isEmpty, topic: "Lewis structure of \(step.target.name), from memory")
        }
        issues = found
        if found.isEmpty {
            withAnimation { passed = true; erasing = false }
        }
    }
}

/// Atom symbols printed on the page, as in a worksheet.
struct PrintedAtoms: View {
    let atoms: [Element]
    let positions: [CGPoint]

    var body: some View {
        Canvas { ctx, size in
            ctx.fill(Path(CGRect(origin: .zero, size: size)), with: .color(Theme.paper))
            let s = size.width / DiagramSpace.size
            for (i, e) in atoms.enumerated() {
                ctx.draw(Text(e.rawValue).font(.system(size: 110 * s, weight: .regular)).foregroundStyle(Theme.ink),
                         at: CGPoint(x: positions[i].x * s, y: positions[i].y * s))
            }
        }
        .accessibilityElement()
        .accessibilityLabel("Atoms: " + atoms.map(\.name).joined(separator: ", "))
    }
}
