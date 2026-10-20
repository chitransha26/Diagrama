import SwiftUI

struct LearnView: View {
    @Environment(ProgressStore.self) private var store
    @State private var query = ""
    @State private var active: Lesson?
    @State private var requested: String?
    @AppStorage("gradeBand") private var bandRaw = GradeBand.middle.rawValue

    private var band: GradeBand { GradeBand(rawValue: bandRaw) ?? .middle }

    /// Search looks across every grade; browsing shows one grade band at a time.
    private var results: [Lesson] {
        query.isEmpty ? Catalog.lessons.filter { $0.band == band } : Catalog.lessons.filter { $0.matches(query) }
    }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 26) {
                    if query.isEmpty {
                        Picker("Grade", selection: $bandRaw) {
                            ForEach(GradeBand.allCases) { Text($0.rawValue).tag($0.rawValue) }
                        }
                        .pickerStyle(.segmented)
                    }

                    ForEach(Subject.allCases) { subject in
                        let lessons = results.filter { $0.subject == subject }
                        if !lessons.isEmpty {
                            VStack(alignment: .leading, spacing: 10) {
                                Label(subject.rawValue, systemImage: subject.symbol)
                                    .font(.headline)
                                ForEach(lessons) { lesson in
                                    Button {
                                        Analytics.track("lesson opened", Analytics.lessonProperties(lesson)
                                            .merging(["from": query.isEmpty ? "browse" : "search"]) { $1 })
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
            .analyticsScreen("Learn", ["grade_band": band.rawValue])
            .onChange(of: bandRaw) { _, new in Analytics.track("grade band selected", ["grade_band": new]) }
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
                .onAppear { Analytics.track("search found nothing", ["query_length": query.count]) }
            Text("No lesson for “\(query)” yet").font(.headline)
            if requested == query || store.requests.contains(where: { $0.caseInsensitiveCompare(query) == .orderedSame }) {
                FeedbackRow(kind: .correct, text: "Requested. We'll use requests to decide which diagrams to add next.")
            } else {
                Button {
                    store.request(query)
                    // What was asked for stays on the device: learners type it, so it isn't sent.
                    Analytics.track("diagram requested")
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
                Text(lesson.grade.first?.isNumber == true ? "Grade \(lesson.grade) · \(lesson.standard)" : lesson.standard)
                    .font(.caption).foregroundStyle(.secondary)
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
