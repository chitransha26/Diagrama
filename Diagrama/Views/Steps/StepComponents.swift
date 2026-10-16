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
