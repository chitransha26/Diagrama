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
        VStack(spacing: 12) {
            if let s = current, let color = s.fill {
                HStack(spacing: 12) {
                    Circle()
                        .fill(color)
                        .overlay(Circle().stroke(Theme.ink.opacity(0.35)))
                        .frame(width: 34, height: 34)
                    VStack(alignment: .leading, spacing: 2) {
                        Text("Fill the \(s.fillName)").font(.headline)
                        Text(s.outlines.count > 1 ? "Tap each of the \(s.outlines.count) parts." : "Tap inside it.")
                            .font(.subheadline).foregroundStyle(.secondary)
                    }
                    Spacer()
                    Image(systemName: "paintbrush.pointed.fill").foregroundStyle(Theme.indigo)
                }
                .padding(12)
                .background(RoundedRectangle(cornerRadius: 14).fill(Color(.secondarySystemBackground)))
                .accessibilityElement(children: .combine)
            } else {
                // Same size as the instruction card, so the canvas doesn't move.
                HStack(spacing: 12) {
                    Image(systemName: "checkmark.circle.fill").font(.system(size: 30)).foregroundStyle(Theme.lime)
                    VStack(alignment: .leading, spacing: 2) {
                        Text("All colored").font(.headline)
                        Text("Every colored part is filled.").font(.subheadline).foregroundStyle(.secondary)
                    }
                    Spacer()
                }
                .padding(12)
                .background(RoundedRectangle(cornerRadius: 14).fill(Color(.secondarySystemBackground)))
            }

            SquareStage { side in
                LearnerDiagram(session: session)
                    .contentShape(Rectangle())
                    .onTapGesture(coordinateSpace: .local) { location in
                        fill(at: location, side: side)
                    }
            }

            Group {
                if let feedback {
                    FeedbackRow(kind: feedback.kind, text: feedback.text)
                } else {
                    FeedbackRow(kind: .info, text: "The color is picked for you. Find the part and tap it.")
                }
            }
            .frame(height: 64, alignment: .top)

            ContinueButton(enabled: current == nil) { session.advance() }
        }
    }

    private func isFilled(_ s: Structure) -> Bool {
        s.outlines.indices.allSatisfy { session.filled.contains("\(s.id)#\($0)") }
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
                let left = target.outlines.indices.filter { !session.filled.contains("\(target.id)#\($0)") }.count
                feedback = (.correct, "Good. \(left) more to fill.")
            }
        } else {
            missedCurrent = true
            feedback = (.wrong, "That's the \(hit.structure.fillName). Find the \(target.fillName).")
        }
    }
}
