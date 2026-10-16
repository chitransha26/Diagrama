import SwiftUI

struct AttemptRecord: Codable, Identifiable {
    var id = UUID()
    let lessonID: String
    let date: Date
    /// ArtWorkout-style drawing scores; nil for lessons without tracing.
    var match: Int?
    var smoothness: Int?
    var firstTry: Int?
    var duration: TimeInterval?
    let scienceCorrect: Int
    let scienceTotal: Int
    /// Finished the from-memory step without help.
    let independent: Bool
    var imageFile: String?
}

/// Learning status, kept separate from drawing scores (PRD §05, §13).
enum LessonStatus {
    case notStarted, practiced, independent, retained

    var title: String {
        switch self {
        case .notStarted: "Not started"
        case .practiced: "Practiced"
        case .independent: "Done from memory"
        case .retained: "Mastered"
        }
    }

    var symbol: String {
        switch self {
        case .notStarted: "circle"
        case .practiced: "circle.lefthalf.filled"
        case .independent: "checkmark.circle"
        case .retained: "checkmark.seal.fill"
        }
    }
}

/// Saves attempts and gallery images on the device. Supabase sync will hook in here.
@Observable
final class ProgressStore {
    private(set) var attempts: [AttemptRecord] = []
    private(set) var requests: [String] = []

    /// A later independent attempt this long after the first one counts as retained mastery
    /// (PRD §05: a delayed check around seven days).
    static let retentionInterval: TimeInterval = 6 * 24 * 60 * 60

    private struct SavedState: Codable {
        var attempts: [AttemptRecord]
        var requests: [String]
    }

    private let directory: URL

    init(directory: URL? = nil) {
        let base = directory ?? FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("Diagrama", isDirectory: true)
        self.directory = base
        try? FileManager.default.createDirectory(at: galleryDirectory, withIntermediateDirectories: true)
        if let data = try? Data(contentsOf: stateFile),
           let state = try? JSONDecoder().decode(SavedState.self, from: data) {
            attempts = state.attempts
            requests = state.requests
        }
    }

    private var stateFile: URL { directory.appendingPathComponent("progress.json") }
    private var galleryDirectory: URL { directory.appendingPathComponent("Gallery", isDirectory: true) }

    func add(_ record: AttemptRecord, image: UIImage?) {
        var record = record
        if let data = image?.pngData() {
            let name = "\(record.id.uuidString).png"
            if (try? data.write(to: galleryDirectory.appendingPathComponent(name))) != nil {
                record.imageFile = name
            }
        }
        attempts.append(record)
        save()
    }

    func request(_ topic: String) {
        let t = topic.trimmingCharacters(in: .whitespaces)
        guard !t.isEmpty, !requests.contains(where: { $0.caseInsensitiveCompare(t) == .orderedSame }) else { return }
        requests.append(t)
        save()
    }

    func image(for record: AttemptRecord) -> UIImage? {
        guard let name = record.imageFile else { return nil }
        return UIImage(contentsOfFile: galleryDirectory.appendingPathComponent(name).path)
    }

    func status(for lessonID: String) -> LessonStatus {
        let mine = attempts.filter { $0.lessonID == lessonID }
        let independent = mine.filter(\.independent).map(\.date).sorted()
        if let first = independent.first, let last = independent.last,
           last.timeIntervalSince(first) >= Self.retentionInterval {
            return .retained
        }
        if !independent.isEmpty { return .independent }
        return mine.isEmpty ? .notStarted : .practiced
    }

    private func save() {
        let state = SavedState(attempts: attempts, requests: requests)
        if let data = try? JSONEncoder().encode(state) {
            try? data.write(to: stateFile, options: .atomic)
        }
    }
}
