import SwiftUI

struct LessonView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var session: LessonSession
    @State private var showLegend = false

    init(lesson: Lesson) {
        _session = State(initialValue: LessonSession(lesson: lesson))
    }

    var body: some View {
        VStack(spacing: 0) {
            header
            if session.finished {
                ResultsView(session: session) { dismiss() }
            } else {
                VStack(alignment: .leading, spacing: 4) {
                    Text(session.step.title).font(.title2.bold())
                    // Always two lines tall, so the canvas stays put from step to step.
                    Text(session.step.instruction)
                        .foregroundStyle(.secondary)
                        .lineLimit(2, reservesSpace: true)
                        .minimumScaleFactor(0.85)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(.horizontal)
                .padding(.top, 4)

                // No transition: two live drawing canvases at once would split the learner's strokes.
                stepView
                    .id(session.step.id)
                    .padding()
            }
        }
        .sheet(isPresented: $showLegend) {
            LegendSheet(lesson: session.lesson)
                .presentationDetents([.medium, .large])
        }
    }

    private var header: some View {
        HStack(spacing: 14) {
            Button {
                dismiss()
            } label: {
                Image(systemName: "xmark").font(.headline)
            }
            .accessibilityLabel("Close lesson")

            ProgressView(value: session.finished ? 1 : session.progress)
                .tint(Theme.cyan)
                .accessibilityLabel("Lesson progress")

            Button {
                showLegend = true
            } label: {
                Label(session.lesson.colorMode.title, systemImage: "paintpalette")
                    .font(.caption.weight(.semibold))
            }
            .buttonStyle(.bordered)
            .accessibilityHint("Shows what the colors mean")
        }
        .padding(.horizontal)
        .padding(.top, 12)
    }

    @ViewBuilder private var stepView: some View {
        switch session.step.kind {
        case .trace(let structure, let part):
            TraceStepView(session: session, structureID: structure, part: part)
        case .color(let structures):
            ColorStepView(session: session, structureIDs: structures)
        case .recall(let structures):
            RecallStepView(session: session, structureIDs: structures)
        case .label(let step):
            LabelStepView(session: session, step: step)
        case .choice(let step):
            ChoiceStepView(session: session, step: step)
        case .order(let step):
            OrderStepView(session: session, step: step)
        case .build(let step):
            BuildStepView(session: session, step: step)
        }
    }
}

struct LegendSheet: View {
    let lesson: Lesson

    var body: some View {
        NavigationStack {
            List {
                Section {
                    Text(lesson.colorMode.explanation)
                }
                Section("Legend") {
                    ForEach(lesson.legend) { entry in
                        HStack(spacing: 12) {
                            RoundedRectangle(cornerRadius: 6)
                                .fill(entry.color ?? Theme.paper)
                                .overlay(RoundedRectangle(cornerRadius: 6).stroke(Theme.ink.opacity(0.4),
                                                                                   style: StrokeStyle(lineWidth: 1, dash: entry.color == nil ? [3, 3] : [])))
                                .frame(width: 28, height: 28)
                            VStack(alignment: .leading) {
                                Text(entry.color == nil ? "\(entry.name) (clear)" : entry.name).font(.headline)
                                Text(entry.meaning).font(.subheadline).foregroundStyle(.secondary)
                            }
                        }
                        .accessibilityElement(children: .combine)
                    }
                }
            }
            .navigationTitle(lesson.colorMode.title)
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}
