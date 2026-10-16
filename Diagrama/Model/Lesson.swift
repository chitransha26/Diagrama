import SwiftUI

enum Subject: String, CaseIterable, Identifiable {
    case cellBiology = "Cell biology"
    case botany = "Botany"
    case chemistry = "Chemistry"

    var id: String { rawValue }

    var symbol: String {
        switch self {
        case .cellBiology: "circle.hexagongrid"
        case .botany: "leaf"
        case .chemistry: "atom"
        }
    }

    /// UI accent for the subject. Never used to color specimens.
    var tint: Color {
        switch self {
        case .cellBiology: Theme.cyan
        case .botany: Theme.lime
        case .chemistry: Theme.coral
        }
    }
}

/// What the colors in a diagram mean (PRD §06). Every lesson declares one.
enum ColorMode {
    /// Colors as seen in a fresh, unstained sample under a light microscope.
    case lightMicroscope
    /// Plain ink, for representations with no real-world color (e.g. Lewis structures).
    case inkOnly

    var title: String {
        switch self {
        case .lightMicroscope: "Microscope colors"
        case .inkOnly: "Ink only"
        }
    }

    var explanation: String {
        switch self {
        case .lightMicroscope:
            "These are the colors you'd see in a fresh, unstained sample under a light microscope. Most parts are nearly clear; the green comes from chloroplasts."
        case .inkOnly:
            "Lewis structures are drawn in plain ink. Atoms have no real color, so nothing is colored in this lesson."
        }
    }
}

struct LegendEntry: Identifiable {
    let name: String
    /// Nil means the part is clear (colorless).
    let color: Color?
    let meaning: String
    var id: String { name }
}

/// A part of a diagram the learner draws and labels.
struct Structure: Identifiable {
    let id: String
    let name: String
    /// Learners trace every outline (e.g. all four chloroplasts).
    let outlines: [Polyline]
    /// The part's real color in the lesson's color mode. Nil means clear, so it isn't filled.
    let fill: Color?
    /// Inner detail (cell walls, thylakoids, xylem) traced in its own step.
    var details: [Polyline] = []
    /// What the fill color stands for, when that differs from the outline
    /// (the cell membrane's fill is the cytoplasm inside it).
    var colorName: String? = nil
    /// The tool the app hands the learner for tracing this part.
    var pen: Pen = .pen
    /// Region to zoom into while tracing a small part, in diagram space.
    var focus: CGRect? = nil
    /// Zoom into each outline in turn (with the details inside it), for small repeated
    /// parts such as chloroplasts.
    var focusEach = false
    /// With `focusEach`, outlines drawn together in one zoomed view (e.g. the three strokes
    /// of each letter H). Defaults to one outline per view.
    var groups: [[Int]]? = nil

    /// The guides for a trace step, split into the pieces drawn one zoomed view at a time.
    func segments(_ part: TracePart) -> [(guides: [Polyline], focus: CGRect?)] {
        let all = part == .outline ? outlines : details
        guard focusEach else { return [(all, focus)] }
        return (groups ?? outlines.indices.map { [$0] }).map { group in
            let members = group.map { outlines[$0] }
            let box = members.map(\.bounds).reduce(CGRect.null) { $0.union($1) }
            let guides = part == .outline ? members : details.filter { box.contains(CGPoint(x: $0.bounds.midX, y: $0.bounds.midY)) }
            return (guides, box.insetBy(dx: -60, dy: -60))
        }
    }

    var outline: Polyline { outlines[0] }
    var fillName: String { colorName ?? name }
}

struct Lesson: Identifiable {
    let id: String
    let title: String
    let level: String
    let subject: Subject
    let minutes: Int
    /// Extra search terms, including synonyms (e.g. "plasma membrane").
    let keywords: [String]
    let colorMode: ColorMode
    let legend: [LegendEntry]
    let structures: [Structure]
    let steps: [LessonStep]

    func structure(_ id: String) -> Structure {
        guard let s = structures.first(where: { $0.id == id }) else {
            preconditionFailure("Lesson \(self.id) has no structure \(id)")
        }
        return s
    }

    /// The topmost visible structure (and which of its outlines) under a point in diagram space.
    func hit(at point: CGPoint, among visible: Set<String>) -> (structure: Structure, outline: Int)? {
        for s in structures.reversed() where visible.contains(s.id) {
            if let i = s.outlines.lastIndex(where: { $0.path.contains(point) }) {
                return (s, i)
            }
        }
        return nil
    }

    func matches(_ query: String) -> Bool {
        let q = query.trimmingCharacters(in: .whitespaces).lowercased()
        guard !q.isEmpty else { return true }
        let haystack = [title, level, subject.rawValue] + keywords + structures.map(\.name)
        return haystack.contains { $0.lowercased().contains(q) }
    }
}

struct LessonStep: Identifiable {
    let id = UUID()
    let title: String
    let instruction: String
    let kind: StepKind
    /// What the part just drawn is and does, shown when the learner finishes drawing it.
    var note: PartNote? = nil
}

/// A short study note about a drawn part: its function, and a tip to help remember it.
struct PartNote {
    let text: String
    var remember: String? = nil
}

enum StepKind {
    /// Trace a structure's outlines or its inner details over a guide.
    case trace(structure: String, part: TracePart)
    /// Fill each listed structure in turn; the app picks the scientifically accurate color.
    case color(structures: [String])
    case label(LabelStep)
    case choice(ChoiceStep)
    case order(OrderStep)
    /// Draw a Lewis structure's bonds and lone pairs freehand around printed atom symbols.
    case drawLewis(LewisStep)
    /// Draw the listed structures from memory, with no guide.
    case recall(structures: [String])
}

enum TracePart {
    case outline, details

    /// The key added to a session's `revealed` set once this part is drawn.
    func key(_ structureID: String) -> String {
        self == .outline ? structureID : structureID + ".details"
    }
}

struct LabelTarget: Identifiable {
    /// The number shown on the marker.
    let id: Int
    let point: CGPoint
    let answer: String
    var synonyms: [String] = []
    /// Why the structure matters, shown once it is labeled correctly.
    let role: String
    /// Explanations for specific wrong answers, keyed by the wrong term.
    var mistakes: [String: String] = [:]
}

struct LabelStep {
    let targets: [LabelTarget]
    let vocabulary: [String]
    /// Explanations for wrong terms that apply to every target.
    var commonMistakes: [String: String] = [:]
}

struct ChoiceOption: Identifiable {
    let id = UUID()
    let text: String
    var correct = false
    let feedback: String
}

struct ChoiceStep {
    let question: String
    let options: [ChoiceOption]
    var showsDiagram = false
}

struct OrderStep {
    /// Items in the correct order.
    let items: [String]
    let why: String
    /// Nudge shown after a wrong order.
    let hint: String
}

struct LewisStep {
    let target: MoleculeTarget
    /// Where each printed atom symbol sits, in diagram space. Grading uses only which atoms
    /// the learner's lines and dots belong to, never their exact positions.
    let positions: [CGPoint]
}
