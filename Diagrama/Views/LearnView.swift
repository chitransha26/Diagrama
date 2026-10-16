import SwiftUI

struct LearnView: View {
    @Environment(ProgressStore.self) private var store
    @State private var query = ""
    @State private var active: Lesson?
    @State private var requested: String?

    private var results: [Lesson] { Catalog.lessons.filter { $0.matches(query) } }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 26) {
                    if query.isEmpty {
                        Text("Draw it. Label it. Explain it.")
                            .font(.title3.weight(.semibold))
                            .foregroundStyle(.secondary)
                    }

                    ForEach(Subject.allCases) { subject in
                        let lessons = results.filter { $0.subject == subject }
                        if !lessons.isEmpty {
                            VStack(alignment: .leading, spacing: 10) {
                                Label(subject.rawValue, systemImage: subject.symbol)
                                    .font(.headline)
                                ForEach(lessons) { lesson in
                                    Button {
                                        active = lesson
                                    } label: {
                                        LessonCard(lesson: lesson, status: store.status(for: lesson.id))
                                    }
                                    .buttonStyle(.plain)
                                }
                            }
                        }
                    }

                    if results.isEmpty {
                        missingContent
                    }
                }
                .padding()
            }
            .navigationTitle("Diagrama")
            .searchable(text: $query, prompt: "Search, e.g. plasma membrane")
            #if DEBUG
            .onAppear {
                // `-openLesson <id>` opens a lesson straight away, for testing. Debug builds only.
                let args = ProcessInfo.processInfo.arguments
                if active == nil, let i = args.firstIndex(of: "-openLesson"), i + 1 < args.count {
                    active = Catalog.lesson(id: args[i + 1])
                }
            }
            #endif
            .fullScreenCover(item: $active) { lesson in
                LessonView(lesson: lesson)
                    .environment(store)
            }
        }
    }

    /// Missing content gets a request action, not a dead end (PRD §03).
    private var missingContent: some View {
        VStack(spacing: 12) {
            Image(systemName: "magnifyingglass").font(.largeTitle).foregroundStyle(.secondary)
            Text("No lesson for “\(query)” yet").font(.headline)
            if requested == query || store.requests.contains(where: { $0.caseInsensitiveCompare(query) == .orderedSame }) {
                FeedbackRow(kind: .correct, text: "Requested. We'll use requests to decide which diagrams to add next.")
            } else {
                Button {
                    store.request(query)
                    requested = query
                } label: {
                    Label("Request this diagram", systemImage: "plus.bubble")
                }
                .buttonStyle(.borderedProminent)
                .tint(Theme.indigo)
            }
        }
        .frame(maxWidth: .infinity)
        .padding(.top, 40)
    }
}

private struct LessonCard: View {
    let lesson: Lesson
    let status: LessonStatus

    var body: some View {
        HStack(spacing: 14) {
            Image(systemName: lesson.subject.symbol)
                .font(.title2)
                .foregroundStyle(Theme.indigo)
                .frame(width: 56, height: 56)
                .background(RoundedRectangle(cornerRadius: 14).fill(lesson.subject.tint.opacity(0.22)))

            VStack(alignment: .leading, spacing: 4) {
                Text(lesson.title).font(.headline)
                Text(lesson.level).font(.caption).foregroundStyle(.secondary)
                HStack(spacing: 10) {
                    Label("\(lesson.minutes) min", systemImage: "clock")
                    Label(status.title, systemImage: status.symbol)
                }
                .font(.caption.weight(.medium))
                .foregroundStyle(Theme.indigo)
            }
            Spacer(minLength: 0)
            Image(systemName: "chevron.right").foregroundStyle(.tertiary)
        }
        .padding(14)
        .background(RoundedRectangle(cornerRadius: 18).fill(Color(.secondarySystemBackground)))
        .contentShape(Rectangle())
        .accessibilityElement(children: .combine)
        .accessibilityHint("Starts the lesson")
    }
}
