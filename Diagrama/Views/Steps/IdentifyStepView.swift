import SwiftUI

/// Find a part that can't be drawn, such as the cytoplasm, by tapping it in your own drawing.
struct IdentifyStepView: View {
    @Bindable var session: LessonSession
    let step: IdentifyStep

    @State private var found: CGPoint?
    @State private var feedback: String?
    @State private var missed = false

    var body: some View {
        VStack(spacing: 10) {
            SquareStage { side in
                ZStack {
                    LearnerDiagram(session: session)
                    if let p = found {
                        Circle()
                            .stroke(Theme.cyan, lineWidth: 3)
                            .frame(width: 26, height: 26)
                            .position(x: p.x / DiagramSpace.size * side, y: p.y / DiagramSpace.size * side)
                        PartNameTag(name: step.name.prefix(1).uppercased() + step.name.dropFirst(),
                                    target: CGRect(x: p.x - 20, y: p.y - 20, width: 40, height: 40), viewport: .whole)
                    }
                }
                .contentShape(Rectangle())
                .onTapGesture(coordinateSpace: .local) { location in
                    tap(CGPoint(x: location.x / side * DiagramSpace.size, y: location.y / side * DiagramSpace.size))
                }
                .accessibilityAddTraits(.allowsDirectInteraction)
            }

            ScrollView {
                VStack(alignment: .leading, spacing: 8) {
                    if found != nil, let note = session.step.note {
                        NoteCard(title: session.step.title, note: note)
                            .transition(.scale(scale: 0.85, anchor: .bottom).combined(with: .opacity))
                    } else if let feedback {
                        FeedbackRow(kind: .wrong, text: feedback)
                    } else {
                        FeedbackRow(kind: .info, text: session.step.instruction)
                    }
                }
            }
            .scrollBounceBehavior(.basedOnSize)
            .frame(height: 156, alignment: .top)

            ContinueButton(enabled: found != nil) { session.advance() }
        }
    }

    private func tap(_ point: CGPoint) {
        guard found == nil else { return }
        let hit = session.lesson.hit(at: point, among: session.revealed)
        if hit?.structure.id == step.structureID {
            session.recordScience(correct: !missed, topic: "Find the \(step.name)")
            withAnimation(.spring(response: 0.45, dampingFraction: 0.7)) { found = point }
        } else {
            missed = true
            if let hit {
                feedback = step.mistakes[hit.structure.id] ?? "That's the \(hit.structure.name). Look for the \(step.name)."
            } else {
                feedback = "That's outside the cell. Tap inside it."
            }
        }
    }
}
