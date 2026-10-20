import SwiftUI

struct GalleryView: View {
    @Environment(ProgressStore.self) private var store

    private let columns = [GridItem(.adaptive(minimum: 150), spacing: 12)]

    var body: some View {
        NavigationStack {
            Group {
                if store.attempts.isEmpty {
                    ContentUnavailableView(
                        "No drawings yet", systemImage: "photo.on.rectangle",
                        description: Text("Finish a lesson and your diagram is saved here.")
                    )
                } else {
                    ScrollView {
                        LazyVGrid(columns: columns, spacing: 12) {
                            ForEach(store.attempts.reversed()) { attempt in
                                NavigationLink(value: attempt.id) {
                                    GalleryCell(attempt: attempt, image: store.image(for: attempt))
                                }
                                .buttonStyle(.plain)
                            }
                        }
                        .padding()
                    }
                }
            }
            .navigationTitle("Gallery")
            .analyticsScreen("Gallery", ["drawings": store.attempts.count])
            .navigationDestination(for: UUID.self) { id in
                if let attempt = store.attempts.first(where: { $0.id == id }) {
                    GalleryDetail(attempt: attempt, image: store.image(for: attempt))
                }
            }
        }
    }
}

private struct GalleryCell: View {
    let attempt: AttemptRecord
    let image: UIImage?

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Group {
                if let image {
                    Image(uiImage: image).resizable().scaledToFit()
                } else {
                    Rectangle().fill(Color(.tertiarySystemFill)).aspectRatio(1, contentMode: .fit)
                }
            }
            .clipShape(RoundedRectangle(cornerRadius: 12))
            Text(Catalog.lesson(id: attempt.lessonID)?.title ?? "Lesson").font(.subheadline.weight(.semibold))
            Text(attempt.date, format: .dateTime.month().day().hour().minute())
                .font(.caption).foregroundStyle(.secondary)
        }
        .accessibilityElement(children: .combine)
    }
}

private struct GalleryDetail: View {
    let attempt: AttemptRecord
    let image: UIImage?

    private var title: String { Catalog.lesson(id: attempt.lessonID)?.title ?? "Diagram" }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Color.clear.frame(height: 0)
                    .analyticsScreen("Gallery drawing", ["lesson_id": attempt.lessonID])
                if let image {
                    Image(uiImage: image)
                        .resizable().scaledToFit()
                        .clipShape(RoundedRectangle(cornerRadius: 16))
                }
                Text(attempt.date, format: .dateTime.weekday(.wide).month().day().hour().minute())
                    .foregroundStyle(.secondary)
                VStack(alignment: .leading, spacing: 6) {
                    if let m = attempt.match { Label("Match \(m)/1000", systemImage: "scope") }
                    if let s = attempt.smoothness { Label("Smoothness \(s)/300", systemImage: "scribble") }
                    if let f = attempt.firstTry { Label("First try \(f)/50", systemImage: "1.circle") }
                    if let d = attempt.duration { Label("Time \(ResultsView.time(d))", systemImage: "clock") }
                    Label("Science \(attempt.scienceCorrect)/\(attempt.scienceTotal)", systemImage: "atom")
                }
                .font(.subheadline)
                Label(attempt.independent ? "Done from memory" : "Practiced",
                      systemImage: attempt.independent ? "checkmark.circle" : "circle.lefthalf.filled")
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(Theme.indigo)
                if let lesson = Catalog.lesson(id: attempt.lessonID) {
                    LessonNotes(lesson: lesson).padding(.top, 8)
                }
            }
            .padding()
        }
        .navigationTitle(title)
        .toolbar {
            if let image {
                ShareLink(item: Image(uiImage: image), preview: SharePreview(title, image: Image(uiImage: image)))
            }
        }
    }
}
