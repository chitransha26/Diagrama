import SwiftUI

struct ResultsView: View {
    let session: LessonSession
    let onDone: () -> Void

    @Environment(ProgressStore.self) private var store
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var snapshot: UIImage?
    @State private var celebrate = false

    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                Image(systemName: "sparkles")
                    .analyticsScreen("Results")
                    .font(.system(size: 54))
                    .foregroundStyle(Theme.cyan, Theme.lime)
                    .scaleEffect(celebrate ? 1 : 0.4)
                    .opacity(celebrate ? 1 : 0)
                Text("Lesson complete").font(.largeTitle.bold())

                if let snapshot {
                    Image(uiImage: snapshot)
                        .resizable()
                        .scaledToFit()
                        .frame(maxWidth: 320)
                        .clipShape(RoundedRectangle(cornerRadius: 16))
                        .overlay(RoundedRectangle(cornerRadius: 16).stroke(Theme.ink.opacity(0.12)))
                        .accessibilityLabel("Your finished diagram")
                }

                LazyVGrid(columns: [GridItem(.flexible(), spacing: 12), GridItem(.flexible(), spacing: 12)], spacing: 12) {
                    if let match = session.match, let smooth = session.smoothness, let first = session.firstTry {
                        ScoreCard(title: "Match", symbol: "scope", value: "\(match)", outOf: 1000,
                                  caption: "How closely your lines followed the guides")
                        ScoreCard(title: "Smoothness", symbol: "scribble", value: "\(smooth)", outOf: 300,
                                  caption: "How steady your lines were")
                        ScoreCard(title: "First try", symbol: "1.circle", value: "\(first)", outOf: 50,
                                  caption: "Steps done without undo, erasing or restarting")
                    }
                    ScoreCard(title: "Time", symbol: "clock", value: Self.time(session.duration), outOf: nil,
                              caption: "Time spent on the lesson")
                    ScoreCard(title: "Science", symbol: "atom", value: "\(session.scienceFirstTry)", outOf: session.scienceTotal,
                              caption: "Questions and checks right on the first try")
                }

                statusCard

                if !session.review.isEmpty {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Worth reviewing").font(.headline)
                        ForEach(session.review, id: \.self) { topic in
                            Label(topic, systemImage: "arrow.counterclockwise")
                                .font(.subheadline)
                        }
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                }

                LessonNotes(lesson: session.lesson)

                ContinueButton(title: "Done", action: onDone)
            }
            .padding()
        }
        .onAppear(perform: save)
    }

    private var statusCard: some View {
        let independent = session.recallPassed
        return HStack(alignment: .top, spacing: 12) {
            Image(systemName: independent ? "checkmark.circle" : "circle.lefthalf.filled")
                .font(.title2)
                .foregroundStyle(Theme.indigo)
            VStack(alignment: .leading, spacing: 4) {
                Text(independent ? "Done from memory" : "Practiced").font(.headline)
                Text(independent
                     ? "You rebuilt it without help. Come back in about a week and do it again to show you've kept it."
                     : "Finish the from-memory step without help to count it as done from memory.")
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(RoundedRectangle(cornerRadius: 14).fill(Color(.secondarySystemBackground)))
    }

    private func save() {
        guard snapshot == nil else { return }
        let image = renderSnapshot()
        snapshot = image
        store.add(session.makeRecord(), image: image)
        if reduceMotion {
            celebrate = true
        } else {
            withAnimation(.spring(response: 0.5, dampingFraction: 0.55)) { celebrate = true }
        }
    }

    @MainActor private func renderSnapshot() -> UIImage? {
        let content = LearnerDiagram(session: session)
        let renderer = ImageRenderer(content: content.frame(width: 600, height: 600))
        renderer.scale = 2
        return renderer.uiImage
    }
}

extension ResultsView {
    static func time(_ t: TimeInterval) -> String {
        String(format: "%02d:%02d", Int(t) / 60, Int(t) % 60)
    }
}

private struct ScoreCard: View {
    let title: String
    let symbol: String
    let value: String
    let outOf: Int?
    let caption: String

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Label(title, systemImage: symbol).font(.subheadline.weight(.semibold)).foregroundStyle(Theme.indigo)
            HStack(alignment: .firstTextBaseline, spacing: 2) {
                Text(value).font(.system(size: 30, weight: .bold, design: .rounded)).monospacedDigit()
                if let outOf {
                    Text(verbatim: "/\(outOf)").font(.subheadline.weight(.semibold)).foregroundStyle(.secondary)
                }
            }
            Text(caption).font(.caption).foregroundStyle(.secondary).fixedSize(horizontal: false, vertical: true)
        }
        .padding()
        .frame(maxWidth: .infinity, minHeight: 130, alignment: .topLeading)
        .background(RoundedRectangle(cornerRadius: 14).fill(Color(.secondarySystemBackground)))
        .accessibilityElement(children: .combine)
    }
}
