import SwiftUI

/// The color stage (ArtWorkout's last stage). The app picks each scientifically accurate color
/// and names the part; the learner finds that part in their drawing and taps every piece of
/// it to fill it. Finding the part on the first tap counts as a science check.
struct ColorStepView: View {
    @Bindable var session: LessonSession
    let structureIDs: [String]

    @State private var feedback: (kind: FeedbackRow.Kind, text: String)?
    @State private var missedCurrent = false

    private var current: Structure? {
        structureIDs.map { session.lesson.structure($0) }.first { !isFilled($0) }
    }

    var body: some View {
        VStack(spacing: 10) {
            SquareStage { side in
                LearnerDiagram(session: session)
                    .contentShape(Rectangle())
                    .onTapGesture(coordinateSpace: .local) { location in
                        fill(at: location, side: side)
                    }
            }

            // Everything to read sits here, under the canvas.
            VStack(alignment: .leading, spacing: 8) {
                task
                if let feedback {
                    FeedbackRow(kind: feedback.kind, text: feedback.text)
                } else {
                    FeedbackRow(kind: .info, text: session.step.instruction)
                }
            }
            .frame(height: 156, alignment: .top)

            ContinueButton(enabled: current == nil) { session.advance() }
        }
    }

    /// The current color and the part it goes on, picked by the app.
    @ViewBuilder private var task: some View {
        HStack(spacing: 10) {
            if let s = current, let color = s.fill {
                Circle()
                    .fill(color)
                    .overlay(Circle().stroke(Theme.ink.opacity(0.35)))
                    .frame(width: 26, height: 26)
                Text("Fill the \(s.fillName)").font(.headline)
                if s.fillable.count > 1 {
                    Text("· tap all \(s.fillable.count)").font(.subheadline).foregroundStyle(.secondary)
                }
            } else {
                Image(systemName: "checkmark.circle.fill").font(.title3).foregroundStyle(Theme.lime)
                Text("All colored").font(.headline)
            }
        }
        .accessibilityElement(children: .combine)
    }

    private func isFilled(_ s: Structure) -> Bool {
        s.fillable.allSatisfy { session.filled.contains("\(s.id)#\($0)") }
    }

    private func fill(at location: CGPoint, side: CGFloat) {
        guard let target = current, side > 0 else { return }
        let point = CGPoint(x: location.x / side * DiagramSpace.size, y: location.y / side * DiagramSpace.size)
        guard let hit = session.lesson.hit(at: point, among: session.revealed) else {
            feedback = (.info, "Tap inside the \(target.fillName).")
            return
        }
        let key = "\(hit.structure.id)#\(hit.outline)"

        if hit.structure.id == target.id {
            guard !session.filled.contains(key) else {
                feedback = (.info, "That one's done. Find the next \(target.fillName).")
                return
            }
            withAnimation(.easeOut(duration: 0.25)) { _ = session.filled.insert(key) }
            if isFilled(target) {
                session.recordScience(correct: !missedCurrent, topic: "Find the \(target.fillName)")
                missedCurrent = false
                let name = target.fillName.prefix(1).uppercased() + target.fillName.dropFirst()
                feedback = (.correct, "\(name) filled.")
            } else {
                let left = target.fillable.filter { !session.filled.contains("\(target.id)#\($0)") }.count
                feedback = (.correct, "Good. \(left) more to fill.")
            }
        } else {
            missedCurrent = true
            feedback = (.wrong, "That's the \(hit.structure.fillName). Find the \(target.fillName).")
        }
    }
}
