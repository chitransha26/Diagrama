import SwiftUI

/// Feedback that carries meaning through an icon and words, not color alone (PRD §06).
struct FeedbackRow: View {
    enum Kind { case correct, wrong, info }
    let kind: Kind
    let text: String

    var body: some View {
        Label {
            Text(text).fixedSize(horizontal: false, vertical: true)
        } icon: {
            Image(systemName: symbol).foregroundStyle(tint)
        }
        .font(.callout)
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    private var symbol: String {
        switch kind {
        case .correct: "checkmark.circle.fill"
        case .wrong: "xmark.octagon.fill"
        case .info: "lightbulb"
        }
    }

    private var tint: Color {
        switch kind {
        case .correct: Theme.lime
        case .wrong: Theme.coral
        case .info: Theme.indigo
        }
    }
}

struct Metric: View {
    let symbol: String
    let label: String
    let value: Double

    var body: some View {
        HStack(spacing: 6) {
            Image(systemName: symbol).foregroundStyle(Theme.indigo)
            Text(label).foregroundStyle(.secondary)
            Text(value, format: .percent.precision(.fractionLength(0))).bold().monospacedDigit()
        }
        .font(.subheadline)
        .accessibilityElement(children: .combine)
    }
}

struct ContinueButton: View {
    var title = "Continue"
    var enabled = true
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title).font(.headline).frame(maxWidth: .infinity).padding(.vertical, 6)
        }
        .buttonStyle(.borderedProminent)
        .tint(Theme.indigo)
        .disabled(!enabled)
    }
}

/// Shown when a part is finished: what it is, what it does, and a tip to remember it.
struct NoteCard: View {
    let title: String
    let note: PartNote

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Label {
                Text(title).font(.headline)
            } icon: {
                Image(systemName: "checkmark.circle.fill").foregroundStyle(Theme.lime)
            }
            Text(note.text)
                .font(.subheadline)
                .fixedSize(horizontal: false, vertical: true)
            if let tip = note.remember {
                Label {
                    Text(tip).fixedSize(horizontal: false, vertical: true)
                } icon: {
                    Image(systemName: "lightbulb.fill").foregroundStyle(Theme.indigo)
                }
                .font(.subheadline.weight(.medium))
            }
        }
        .padding(10)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(RoundedRectangle(cornerRadius: 14).fill(Theme.indigo.opacity(0.08)))
        .accessibilityElement(children: .combine)
    }
}

/// Every note from a lesson, in drawing order: a short study sheet.
struct LessonNotes: View {
    let lesson: Lesson

    var body: some View {
        let notes = lesson.steps.compactMap { step in step.note.map { (step.title, $0) } }
        if !notes.isEmpty {
            VStack(alignment: .leading, spacing: 12) {
                Label("Your notes", systemImage: "book.closed").font(.headline)
                ForEach(notes, id: \.0) { title, note in
                    VStack(alignment: .leading, spacing: 3) {
                        Text(title).font(.subheadline.weight(.semibold))
                        Text(note.text).font(.subheadline)
                        if let tip = note.remember {
                            Text(tip).font(.subheadline).foregroundStyle(Theme.indigo)
                        }
                    }
                    .fixedSize(horizontal: false, vertical: true)
                    .accessibilityElement(children: .combine)
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
    }
}
