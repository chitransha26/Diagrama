import SwiftUI

/// Label numbered markers by picking terms. Errors are named and explained (PRD §05).
struct LabelStepView: View {
    @Bindable var session: LessonSession
    let step: LabelStep

    @State private var answers: [Int: String] = [:]
    @State private var checked: [Int: Bool] = [:]
    @State private var recorded = false
    @State private var selected: Int?

    private var allCorrect: Bool { step.targets.allSatisfy { checked[$0.id] == true } }

    var body: some View {
        ScrollViewReader { proxy in
        ScrollView {
            VStack(spacing: 14) {
                LearnerDiagram(session: session, markers: markers)
                    .aspectRatio(1, contentMode: .fit)
                    .clipShape(RoundedRectangle(cornerRadius: 16))
                    .overlay(RoundedRectangle(cornerRadius: 16).stroke(Theme.ink.opacity(0.12)))
                    .frame(maxWidth: 520)

                ForEach(step.targets) { target in
                    row(for: target)
                }

                Group {
                    if allCorrect {
                        ContinueButton { session.advance() }
                    } else {
                        ContinueButton(title: "Check labels", enabled: answers.count == step.targets.count) { check() }
                    }
                }
                .id("action")
            }
            .padding(.bottom)
        }
        .onChange(of: allCorrect) { _, done in
            if done { withAnimation { proxy.scrollTo("action", anchor: .bottom) } }
        }
        }
    }

    private var markers: [DiagramMarker] {
        step.targets.map { t in
            let state: DiagramMarker.State = switch checked[t.id] {
            case true: .correct
            case false: .wrong
            default: selected == t.id ? .selected : .neutral
            }
            return DiagramMarker(number: t.id, point: t.point, state: state)
        }
    }

    private func row(for target: LabelTarget) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Text("\(target.id)")
                    .font(.headline)
                    .frame(width: 30, height: 30)
                    .background(Circle().fill(Theme.indigo.opacity(0.12)))
                Menu {
                    ForEach(step.vocabulary, id: \.self) { term in
                        Button(term) {
                            answers[target.id] = term
                            checked[target.id] = nil
                            selected = target.id
                        }
                    }
                } label: {
                    HStack {
                        Text(answers[target.id] ?? "Choose a name…")
                            .foregroundStyle(answers[target.id] == nil ? .secondary : .primary)
                        Spacer()
                        Image(systemName: "chevron.up.chevron.down").font(.caption)
                    }
                    .padding(10)
                    .background(RoundedRectangle(cornerRadius: 10).fill(Color(.secondarySystemBackground)))
                }
                .disabled(checked[target.id] == true)
                .accessibilityLabel("Marker \(target.id): \(answers[target.id] ?? "no name chosen")")
            }
            if let ok = checked[target.id], let answer = answers[target.id] {
                FeedbackRow(
                    kind: ok ? .correct : .wrong,
                    text: ok ? target.role : LabelGrader.explanation(for: answer, target: target, step: step)
                )
                .padding(.leading, 38)
            }
        }
    }

    private func check() {
        for t in step.targets {
            let ok = LabelGrader.isCorrect(answers[t.id] ?? "", for: t)
            checked[t.id] = ok
            if !recorded { session.recordScience(correct: ok, topic: "Label: \(t.answer.lowercased())") }
        }
        recorded = true
        selected = nil
    }
}

struct ChoiceStepView: View {
    @Bindable var session: LessonSession
    let step: ChoiceStep

    @State private var picked: UUID?
    @State private var recorded = false
    @State private var solved = false

    var body: some View {
        ScrollViewReader { proxy in
        ScrollView {
            VStack(alignment: .leading, spacing: 14) {
                if step.showsDiagram, !session.lesson.structures.isEmpty {
                    LearnerDiagram(session: session)
                        .aspectRatio(1, contentMode: .fit)
                        .clipShape(RoundedRectangle(cornerRadius: 16))
                        .frame(maxWidth: 330)
                        .frame(maxWidth: .infinity)
                }
                Text(step.question).font(.title3.weight(.semibold))

                ForEach(step.options) { option in
                    Button {
                        choose(option)
                    } label: {
                        HStack {
                            Text(option.text).multilineTextAlignment(.leading)
                            Spacer()
                            if picked == option.id {
                                Image(systemName: option.correct ? "checkmark.circle.fill" : "xmark.octagon.fill")
                                    .foregroundStyle(option.correct ? Theme.lime : Theme.coral)
                            }
                        }
                        .padding(14)
                        .frame(maxWidth: .infinity)
                        .background(RoundedRectangle(cornerRadius: 12).fill(Color(.secondarySystemBackground)))
                        .overlay(RoundedRectangle(cornerRadius: 12).stroke(picked == option.id ? Theme.indigo : .clear, lineWidth: 2))
                    }
                    .buttonStyle(.plain)
                    .disabled(solved)
                }

                if let option = step.options.first(where: { $0.id == picked }) {
                    FeedbackRow(kind: option.correct ? .correct : .wrong,
                                text: option.correct ? option.feedback : option.feedback + " Try another answer.")
                }

                if solved {
                    ContinueButton { session.advance() }
                        .id("action")
                }
            }
            .padding(.bottom)
        }
        .onChange(of: solved) { _, done in
            if done { withAnimation { proxy.scrollTo("action", anchor: .bottom) } }
        }
        }
    }

    private func choose(_ option: ChoiceOption) {
        picked = option.id
        if !recorded {
            session.recordScience(correct: option.correct, topic: step.question)
            recorded = true
        }
        if option.correct { solved = true }
    }
}

/// Put items in order by tapping them (PRD §04: "arrange").
struct OrderStepView: View {
    @Bindable var session: LessonSession
    let step: OrderStep

    @State private var pool: [String]
    @State private var sequence: [String] = []
    @State private var result: Bool?
    @State private var recorded = false

    init(session: LessonSession, step: OrderStep) {
        self.session = session
        self.step = step
        var shuffled = step.items.shuffled()
        while shuffled == step.items, step.items.count > 1 { shuffled.shuffle() }
        _pool = State(initialValue: shuffled)
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 12) {
                ForEach(pool, id: \.self) { item in
                    let position = sequence.firstIndex(of: item)
                    Button {
                        tap(item)
                    } label: {
                        HStack(spacing: 12) {
                            Text(position.map { "\($0 + 1)" } ?? " ")
                                .font(.headline)
                                .frame(width: 30, height: 30)
                                .background(Circle().fill(position == nil ? Color(.tertiarySystemFill) : Theme.indigo))
                                .foregroundStyle(.white)
                            Text(item)
                            Spacer()
                        }
                        .padding(12)
                        .background(RoundedRectangle(cornerRadius: 12).fill(Color(.secondarySystemBackground)))
                    }
                    .buttonStyle(.plain)
                    .disabled(result == true)
                    .accessibilityLabel(position.map { "\(item), position \($0 + 1)" } ?? item)
                }

                if let ok = result {
                    FeedbackRow(kind: ok ? .correct : .wrong, text: ok ? step.why : "Not quite. \(step.hint) Tap Reset and try again.")
                }

                HStack {
                    Button("Reset") {
                        sequence = []
                        result = nil
                    }
                    .buttonStyle(.bordered)
                    .disabled(sequence.isEmpty || result == true)
                    Spacer()
                    if result == true {
                        ContinueButton { session.advance() }.frame(maxWidth: 180)
                    }
                }
            }
        }
    }

    private func tap(_ item: String) {
        if let i = sequence.firstIndex(of: item) {
            sequence.remove(at: i)
            result = nil
            return
        }
        sequence.append(item)
        if sequence.count == step.items.count {
            let ok = sequence == step.items
            result = ok
            if !recorded {
                session.recordScience(correct: ok, topic: "Order of the layers")
                recorded = true
            }
        }
    }
}
