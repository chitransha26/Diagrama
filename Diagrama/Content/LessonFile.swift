import SwiftUI

/// Lessons written as data (JSON files in Content/Lessons), so the catalog can grow without
/// app code. Geometry is in the 1000 × 1000 diagram space; shapes can be simple primitives or
/// SVG path data from any vector art source.
struct LessonFile: Decodable {
    let id: String
    let title: String
    let grade: String
    let subject: Subject
    let standard: String
    let minutes: Int
    var level: String?
    var keywords: [String]?
    /// "microscope" (real colors of an unstained sample), "ink" (no color), or "illustration"
    /// (simplified real-world colors, explained by the legend).
    var colorMode: String?
    var legend: [LegendFile]?
    var structures: [StructureFile]?
    let steps: [StepFile]
    var printed: [PrintedFile]?
    /// Structures to draw from memory; all of them if omitted.
    var recall: [String]?

    struct PrintedFile: Decodable {
        let text: String
        let at: [CGFloat]
        var size: CGFloat?
    }

    struct LegendFile: Decodable {
        let name: String
        var color: String?
        let meaning: String
    }

    struct StructureFile: Decodable {
        let id: String
        let name: String
        let outlines: [ShapeFile]
        var fill: String?
        var details: [ShapeFile]?
        var colorName: String?
        var pen: String?
        var focus: [CGFloat]?
        var focusEach: Bool?
        var groups: [[Int]]?
    }

    /// One of: {"circle": [cx, cy, r]}, {"ellipse": [cx, cy, rx, ry]},
    /// {"rect": [x, y, w, h, cornerRadius?]}, {"line": [x1, y1, x2, y2, …]} (open),
    /// {"polygon": [x1, y1, …]} (closed), or {"path": "M … Z"} (SVG; may hold several subpaths).
    struct ShapeFile: Decodable {
        let polylines: [Polyline]

        private enum Key: String, CodingKey { case circle, ellipse, rect, line, polygon, path }

        init(from decoder: Decoder) throws {
            let c = try decoder.container(keyedBy: Key.self)
            func nums(_ k: Key, _ count: ClosedRange<Int>) throws -> [CGFloat] {
                let v = try c.decode([CGFloat].self, forKey: k)
                guard count.contains(v.count) else {
                    throw DecodingError.dataCorruptedError(forKey: k, in: c, debugDescription: "\(k.rawValue) needs \(count) numbers")
                }
                return v
            }
            if c.contains(.circle) {
                let v = try nums(.circle, 3...3); polylines = [Shapes.circle(v[0], v[1], v[2])]
            } else if c.contains(.ellipse) {
                let v = try nums(.ellipse, 4...4); polylines = [Shapes.ellipse(v[0], v[1], v[2], v[3])]
            } else if c.contains(.rect) {
                let v = try nums(.rect, 4...5); polylines = [Shapes.roundedRect(v[0], v[1], v[2], v[3], r: v.count > 4 ? v[4] : 0.01)]
            } else if c.contains(.line) || c.contains(.polygon) {
                let closed = c.contains(.polygon)
                let v = try nums(closed ? .polygon : .line, 4...10_000)
                let pts = stride(from: 0, to: v.count - 1, by: 2).map { CGPoint(x: v[$0], y: v[$0 + 1]) }
                polylines = [Polyline(points: pts, closed: closed)]
            } else if c.contains(.path) {
                polylines = try SVGPath.polylines(try c.decode(String.self, forKey: .path))
            } else {
                throw DecodingError.dataCorrupted(.init(codingPath: decoder.codingPath, debugDescription: "Unknown shape"))
            }
        }
    }

    struct NoteFile: Decodable {
        let text: String
        var remember: String?
    }

    struct TargetFile: Decodable {
        let n: Int
        let at: [CGFloat]
        let answer: String
        var synonyms: [String]?
        let role: String
        var mistakes: [String: String]?
    }

    struct OptionFile: Decodable {
        let text: String
        var correct: Bool?
        let feedback: String
    }

    struct MoleculeFile: Decodable {
        let name: String
        let atoms: [Element]
        /// [atomA, atomB, bondOrder]
        let bonds: [[Int]]
        var charge: Int?
    }

    struct StepFile: Decodable {
        let type: String
        let title: String
        let instruction: String
        var note: NoteFile?
        // trace / recall / color
        var structure: String?
        var part: String?
        var structures: [String]?
        // identify
        var name: String?
        var mistakes: [String: String]?
        var insideDetailsMistake: String?
        // label
        var targets: [TargetFile]?
        var vocabulary: [String]?
        var commonMistakes: [String: String]?
        // choice
        var question: String?
        var options: [OptionFile]?
        var showsDiagram: Bool?
        // order
        var items: [String]?
        var why: String?
        var hint: String?
        // lewis
        var molecule: MoleculeFile?
        var positions: [[CGFloat]]?
    }
}

extension LessonFile {
    enum Problem: Error, CustomStringConvertible {
        case invalid(String)
        var description: String { if case .invalid(let s) = self { return s }; return "" }
    }

    func lesson() throws -> Lesson {
        let mode: ColorMode = switch colorMode ?? "ink" {
        case "microscope": .lightMicroscope
        case "illustration": .illustration
        default: .inkOnly
        }
        let built = try (structures ?? []).map { s in
            Structure(
                id: s.id, name: s.name, outlines: s.outlines.flatMap(\.polylines),
                fill: try s.fill.map(Self.color), details: (s.details ?? []).flatMap(\.polylines),
                colorName: s.colorName, pen: Self.pen(s.pen),
                focus: s.focus.flatMap { $0.count == 4 ? CGRect(x: $0[0], y: $0[1], width: $0[2], height: $0[3]) : nil },
                focusEach: s.focusEach ?? false, groups: s.groups
            )
        }
        return Lesson(
            id: id, title: title, level: level ?? GradeBand(grade: grade).rawValue, subject: subject,
            minutes: minutes, keywords: keywords ?? [], colorMode: mode,
            legend: try (legend ?? []).map { LegendEntry(name: $0.name, color: try $0.color.map(Self.color), meaning: $0.meaning) },
            structures: built, steps: try steps.map(step), grade: grade, standard: standard,
            printed: (printed ?? []).map { PrintedText(text: $0.text, at: CGPoint(x: $0.at[0], y: $0.at[1]), size: $0.size ?? 46) },
            recallStructures: recall ?? []
        )
    }

    private func step(_ f: StepFile) throws -> LessonStep {
        func need<T>(_ v: T?, _ field: String) throws -> T {
            guard let v else { throw Problem.invalid("\(id): step “\(f.title)” needs \(field)") }
            return v
        }
        let kind: StepKind
        switch f.type {
        case "trace":
            kind = .trace(structure: try need(f.structure, "structure"), part: f.part == "details" ? .details : .outline)
        case "color":
            kind = .color(structures: try need(f.structures, "structures"))
        case "recall":
            kind = .recall(structures: try need(f.structures, "structures"))
        case "identify":
            kind = .identify(IdentifyStep(name: try need(f.name, "name"), structureID: try need(f.structure, "structure"),
                                          mistakes: f.mistakes ?? [:], insideDetailsMistake: f.insideDetailsMistake))
        case "label":
            kind = .label(LabelStep(
                targets: try need(f.targets, "targets").map {
                    LabelTarget(id: $0.n, point: CGPoint(x: $0.at[0], y: $0.at[1]), answer: $0.answer,
                                synonyms: $0.synonyms ?? [], role: $0.role, mistakes: $0.mistakes ?? [:])
                },
                vocabulary: try need(f.vocabulary, "vocabulary"), commonMistakes: f.commonMistakes ?? [:]))
        case "choice":
            kind = .choice(ChoiceStep(question: try need(f.question, "question"),
                                      options: try need(f.options, "options").map { ChoiceOption(text: $0.text, correct: $0.correct ?? false, feedback: $0.feedback) },
                                      showsDiagram: f.showsDiagram ?? false))
        case "order":
            kind = .order(OrderStep(items: try need(f.items, "items"), why: try need(f.why, "why"), hint: try need(f.hint, "hint")))
        case "lewis":
            let m = try need(f.molecule, "molecule")
            var bonds: [BondKey: Int] = [:]
            for b in m.bonds where b.count == 3 { bonds[BondKey(b[0], b[1])] = b[2] }
            kind = .drawLewis(LewisStep(
                target: MoleculeTarget(name: m.name, atoms: m.atoms, bonds: bonds, charge: m.charge ?? 0),
                positions: try need(f.positions, "positions").map { CGPoint(x: $0[0], y: $0[1]) }))
        default:
            throw Problem.invalid("\(id): unknown step type \(f.type)")
        }
        return LessonStep(title: f.title, instruction: f.instruction, kind: kind,
                          note: f.note.map { PartNote(text: $0.text, remember: $0.remember) })
    }

    private static func pen(_ name: String?) -> Pen {
        switch name {
        case "fine": .fineLiner
        case "bold": .boldPen
        case "pencil": .pencil
        default: .pen
        }
    }

    /// "#RRGGBB"
    static func color(_ hex: String) throws -> Color {
        let h = hex.trimmingCharacters(in: CharacterSet(charactersIn: "#"))
        guard h.count == 6, let v = UInt32(h, radix: 16) else { throw Problem.invalid("Bad color \(hex)") }
        return Color(red: Double((v >> 16) & 0xFF) / 255, green: Double((v >> 8) & 0xFF) / 255, blue: Double(v & 0xFF) / 255)
    }

    /// Loads every lesson file bundled with the app. A broken file is reported, not skipped
    /// silently; tests fail on any problem.
    static func bundled() -> (lessons: [Lesson], problems: [String]) {
        let urls = (Bundle.main.urls(forResourcesWithExtension: "json", subdirectory: nil) ?? [])
            .filter { $0.lastPathComponent.hasPrefix("lesson-") }
            .sorted { $0.lastPathComponent < $1.lastPathComponent }
        var lessons: [Lesson] = [], problems: [String] = []
        for url in urls {
            do {
                let file = try JSONDecoder().decode(LessonFile.self, from: Data(contentsOf: url))
                lessons.append(try file.lesson())
            } catch {
                problems.append("\(url.lastPathComponent): \(error)")
            }
        }
        return (lessons, problems)
    }
}
