import SwiftUI

/// The finished diagram, in its real colors, to study before drawing it from memory.
struct StudyStepView: View {
    let session: LessonSession

    private var everything: Set<String> {
        Set(session.lesson.structures.flatMap { [$0.id, TracePart.details.key($0.id)] })
    }

    var body: some View {
        VStack(spacing: 10) {
            SquareStage { _ in
                DiagramView(lesson: session.lesson, revealed: everything)
            }
            VStack(alignment: .leading, spacing: 8) {
                FeedbackRow(kind: .info, text: session.step.instruction)
            }
            .frame(height: 156, alignment: .top)
            ContinueButton(title: "I'm ready") { session.advance() }
        }
    }
}
