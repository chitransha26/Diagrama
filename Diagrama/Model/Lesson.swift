import SwiftUI

enum Subject: String, CaseIterable, Identifiable, Decodable {
    case life = "Life science"
    case zoology = "Zoology"
    case chemistry = "Chemistry"
    case physics = "Physics"
    case earthSpace = "Earth & space"

    var id: String { rawValue }

    var symbol: String {
        switch self {
        case .life: "leaf"
        case .zoology: "pawprint"
        case .chemistry: "atom"
        case .physics: "bolt"
        case .earthSpace: "globe.americas"
        }
    }

    /// UI accent for the subject. Never used to color specimens.
    var tint: Color {
        switch self {
        case .life: Theme.lime
        case .zoology: Theme.coral
        case .chemistry: Theme.cyan
        case .physics: Theme.indigo
        case .earthSpace: Theme.cyan
        }
    }
}

/// School grade bands, following NGSS.
enum GradeBand: String, CaseIterable, Identifiable {
    case elementary = "Grades 3–5"
    case middle = "Middle school"
    case high = "High school"

    var id: String { rawValue }

    var sortOrder: Int { GradeBand.allCases.firstIndex(of: self)! }

    /// "3"–"5" are elementary, "6"–"8" middle school, anything else (e.g. "9-10", "AP Bio") high school.
    init(grade: String) {
        switch Int(grade) {
        case .some(...5): self = .elementary
        case .some(6...8): self = .middle
        default: self = .high
        }
    }
}

/// What the colors in a diagram mean (PRD §06). Every lesson declares one.
enum ColorMode {
    /// Colors as seen in a fresh, unstained sample under a light microscope.
    case lightMicroscope
    /// Plain ink, for representations with no real-world color (e.g. Lewis structures).
    case inkOnly
    /// Simplified real-world colors of whole organisms and objects, as seen by eye.
    case illustration

    var title: String {
        switch self {
        case .lightMicroscope: "Microscope colors"
        case .inkOnly: "Ink only"
        case .illustration: "Real colors"
        }
    }

    var explanation: String {
        switch self {
        case .lightMicroscope:
            "These are the colors you'd see in a fresh, unstained sample under a light microscope. Most parts are nearly clear; the green comes from chloroplasts."
        case .illustration:
            "Colors are simplified versions of how these things look in real life. The legend explains each one."
        case .inkOnly:
            "This diagram is drawn in plain ink. What it shows has no real color, so nothing is colored in this lesson."
        }
    }
}

/// Where a lesson's facts were checked.
struct Source: Hashable {
    let title: String
    var url: URL?
}

/// Words printed on the worksheet, like axis labels: always shown, never traced.
struct PrintedText {
    let text: String
    let at: CGPoint
    var size: CGFloat = 46
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
        guard focusEach else {
            if let focus { return [(all, focus)] }
            return Self.autoSegments(all)
        }
        return (groups ?? outlines.indices.map { [$0] }).map { group in
            let members = group.map { outlines[$0] }
            let box = members.map(\.bounds).reduce(CGRect.null) { $0.union($1) }
            let guides = part == .outline ? members : details.filter { box.contains(CGPoint(x: $0.bounds.midX, y: $0.bounds.midY)) }
            return (guides, box.insetBy(dx: -60, dy: -60))
        }
    }

    var outline: Polyline { outlines[0] }
    /// The outlines that can be colored in: closed shapes only, not lines such as the
    /// twig a chrysalis hangs from.
    var fillable: [Int] { outlines.indices.filter { outlines[$0].closed } }
    var fillName: String { colorName ?? name }

    /// A part smaller than this (diagram units) is zoomed into automatically.
    static let smallPart: CGFloat = 220
    /// Nearby small parts share one zoomed view, up to this size.
    static let zoomWindow: CGFloat = 300
    /// Smallest comfortable size for a closed shape and for a stroke, in diagram units at
    /// zoom 1 on a small iPhone (24 pt and 14 pt on a 350 pt canvas).
    static let closedMinimum: CGFloat = 69
    static let openMinimum: CGFloat = 40

    /// Splits guides into views without any per-lesson setup: parts big enough to trace
    /// comfortably are drawn unzoomed together; small parts (an eye, an arrowhead, a dot)
    /// are zoomed into, with neighbours sharing a view. Order follows the guides' order.
    static func autoSegments(_ guides: [Polyline]) -> [(guides: [Polyline], focus: CGRect?)] {
        guard !guides.isEmpty else { return [(guides, nil)] }
        // 1. Cluster guides that touch or nearly touch (an arrow's line and head, an eye and mouth).
        var parent = Array(guides.indices)
        func find(_ i: Int) -> Int { parent[i] == i ? i : find(parent[i]) }
        let padded = guides.map { $0.bounds.insetBy(dx: -15, dy: -15) }
        for i in guides.indices {
            for j in guides.indices where j > i && padded[i].intersects(padded[j]) {
                parent[find(j)] = find(i)
            }
        }
        var clusters: [[Int]] = []
        var index: [Int: Int] = [:]
        for i in guides.indices {
            let root = find(i)
            if let c = index[root] { clusters[c].append(i) } else { index[root] = clusters.count; clusters.append([i]) }
        }
        func box(_ c: [Int]) -> CGRect { c.map { guides[$0].bounds }.reduce(CGRect.null) { $0.union($1) } }
        /// The zoom a cluster needs so its smallest part is comfortable for a finger.
        func neededZoom(_ c: [Int]) -> CGFloat {
            c.map { i -> CGFloat in
                let g = guides[i]
                guard !StrokeScorer.isDot(g) else { return 1 }
                let size = max(g.bounds.width, g.bounds.height)
                return (g.closed ? closedMinimum : openMinimum) / max(size, 1)
            }.max() ?? 1
        }
        func zoomFor(_ b: CGRect) -> CGFloat { min(Viewport.maxZoom, DiagramSpace.size / (max(b.width, b.height) + 100)) }
        let small = clusters.filter { max(box($0).width, box($0).height) < smallPart || neededZoom($0) > 1 }
        guard !small.isEmpty else { return [(guides, nil)] }
        // 2. Merge neighbouring small clusters into shared zoom windows, as long as the shared
        //    view still zooms in enough for every part in it.
        var windows: [[Int]] = []
        for c in small {
            if let w = windows.indices.first(where: {
                let merged = windows[$0] + c
                let u = box(merged)
                return max(u.width, u.height) <= zoomWindow && zoomFor(u) >= neededZoom(merged)
            }) {
                windows[w] += c
            } else {
                windows.append(c)
            }
        }
        let smallSet = Set(small.flatMap { $0 })
        // 3. Big parts first, unzoomed; then each zoom window, in drawing order.
        var result: [(order: Int, guides: [Polyline], focus: CGRect?)] = []
        let big = clusters.flatMap { $0 }.filter { !smallSet.contains($0) }.sorted()
        if !big.isEmpty { result.append((big[0], big.map { guides[$0] }, nil)) }
        for w in windows {
            let members = w.sorted()
            result.append((members[0], members.map { guides[$0] }, box(members).insetBy(dx: -50, dy: -50)))
        }
        return result.sorted { $0.order < $1.order }.map { ($0.guides, $0.focus) }
    }
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
    var steps: [LessonStep]
    /// School grade, e.g. "4", "7" or "10-11".
    var grade = "7"
    /// The standard this lesson supports, e.g. "MS-LS1-2" (NGSS) or "AP Biology".
    var standard = ""
    var printed: [PrintedText] = []
    /// Structures to draw in the from-memory step. Empty means all of them.
    var recallStructures: [String] = []
    /// Where the lesson's facts were verified. Every lesson must have at least one.
    var sources: [Source] = []

    /// Every lesson with drawing ends with two screens after its questions: copy the finished
    /// diagram while looking at it, then draw it from memory. Lessons that already have a memory
    /// step get the copy screen just before it.
    func withMemorySteps() -> Lesson {
        guard steps.contains(where: { if case .trace = $0.kind { return true }; return false }) else { return self }
        var lesson = self
        let copyText = "Look at the picture and draw it again in the space below. Any size is fine."
        if let i = steps.firstIndex(where: { switch $0.kind { case .recall, .drawLewis: true; default: false } }) {
            if i > 0, case .copy = steps[i - 1].kind { return self }
            switch steps[i].kind {
            case .recall(let ids):
                lesson.steps.insert(LessonStep(title: "Copy it", instruction: copyText, kind: .copy(structures: ids)), at: i)
            case .drawLewis(let s):
                var copying = s
                copying.copying = true
                copying.positions = s.positions.map { CGPoint(x: DiagramSpace.size - $0.x, y: $0.y) }
                lesson.steps.insert(LessonStep(
                    title: "Copy it",
                    instruction: "Look at the picture and draw the same bonds and lone pairs around these atoms.",
                    kind: .drawLewis(copying)), at: i)
            default: break
            }
        } else {
            let ids = recallStructures.isEmpty ? structures.map(\.id) : recallStructures
            lesson.steps += [
                LessonStep(title: "Copy it", instruction: copyText, kind: .copy(structures: ids)),
                LessonStep(title: "From memory",
                           instruction: "Now draw it from memory, without looking. Any size and position is fine. Press Check when you're done.",
                           kind: .recall(structures: ids)),
            ]
        }
        return lesson
    }

    var band: GradeBand { GradeBand(grade: grade) }

    func structure(_ id: String) -> Structure {
        guard let s = structures.first(where: { $0.id == id }) else {
            preconditionFailure("Lesson \(self.id) has no structure \(id)")
        }
        return s
    }

    /// The topmost visible structure (and which of its outlines) under a point in diagram space.
    func hit(at point: CGPoint, among visible: Set<String>) -> (structure: Structure, outline: Int)? {
        for s in structures.reversed() where visible.contains(s.id) {
            if let i = s.outlines.indices.last(where: { s.outlines[$0].closed && s.outlines[$0].path.contains(point) }) {
                return (s, i)
            }
        }
        return nil
    }

    func matches(_ query: String) -> Bool {
        let q = query.trimmingCharacters(in: .whitespaces).lowercased()
        guard !q.isEmpty else { return true }
        let haystack = [title, level, subject.rawValue, standard] + keywords + structures.map(\.name)
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

    /// Steps that work on the learner's drawing keep all guidance under the canvas.
    var isDrawing: Bool {
        switch kind {
        case .trace, .identify, .color, .recall, .drawLewis, .copy: true
        default: false
        }
    }
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
    /// Find a region that can't be traced (like the cytoplasm) by tapping it in the drawing.
    case identify(IdentifyStep)
    /// Draw a Lewis structure's bonds and lone pairs freehand around printed atom symbols.
    case drawLewis(LewisStep)
    /// Draw the listed structures from memory, with no guide.
    case recall(structures: [String])
    /// Recreate the listed structures on a blank canvas while looking at the finished diagram.
    case copy(structures: [String])
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

struct IdentifyStep {
    let name: String
    /// A tap counts when its topmost drawn structure is this one (e.g. the membrane, for
    /// the cytoplasm inside it but outside every organelle).
    let structureID: String
    /// Explanations for tapping other structures, keyed by structure ID.
    var mistakes: [String: String] = [:]
    /// When set, taps inside the structure's own closed details (e.g. the cells, when looking
    /// for the air spaces between them) are wrong, and get this explanation.
    var insideDetailsMistake: String? = nil
}

struct LewisStep {
    let target: MoleculeTarget
    /// Where each printed atom symbol sits, in diagram space. Grading uses only which atoms
    /// the learner's lines and dots belong to, never their exact positions.
    var positions: [CGPoint]
    /// Shows the finished structure above the canvas to copy from.
    var copying = false
}
