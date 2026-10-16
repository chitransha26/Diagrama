import SwiftUI

/// Water's Lewis structure, drawn the way a person draws it on paper: symbols first, then
/// bonds, then lone pairs. Learners trace over printed symbols rather than handwriting them.
enum WaterLesson {
    static let water = MoleculeTarget(
        name: "water",
        atoms: [.O, .H, .H],
        bonds: [BondKey(0, 1): 1, BondKey(0, 2): 1]
    )

    private static let oxygen = CGPoint(x: 500, y: 400)
    private static let hydrogens = [CGPoint(x: 300, y: 580), CGPoint(x: 700, y: 580)]

    /// Strokes of a printed "H", in the order people write it: left side, right side, crossbar.
    private static func letterH(_ c: CGPoint) -> [Polyline] {
        [
            Shapes.line(CGPoint(x: c.x - 30, y: c.y - 50), CGPoint(x: c.x - 30, y: c.y + 50)),
            Shapes.line(CGPoint(x: c.x + 30, y: c.y - 50), CGPoint(x: c.x + 30, y: c.y + 50)),
            Shapes.line(CGPoint(x: c.x - 30, y: c.y), CGPoint(x: c.x + 30, y: c.y)),
        ]
    }

    /// A bond line from atom to atom, stopping short of both symbols.
    private static func bond(_ a: CGPoint, _ b: CGPoint) -> Polyline {
        let len = a.distance(to: b)
        let u = CGPoint(x: (b.x - a.x) / len, y: (b.y - a.y) / len)
        return Shapes.line(CGPoint(x: a.x + u.x * 70, y: a.y + u.y * 70), CGPoint(x: b.x - u.x * 65, y: b.y - u.y * 65))
    }

    /// Two dots on the side of oxygen facing `angle`, away from the bonds.
    private static func lonePair(angle: CGFloat) -> [Polyline] {
        let center = CGPoint(x: oxygen.x + 92 * cos(angle), y: oxygen.y + 92 * sin(angle))
        let perp = CGPoint(x: -sin(angle), y: cos(angle))
        return [-15, 15].map { d in Shapes.circle(center.x + perp.x * d, center.y + perp.y * d, 7) }
    }

    static let structures: [Structure] = [
        Structure(id: "oxygen", name: "oxygen symbol", outlines: [Shapes.ellipse(oxygen.x, oxygen.y, 38, 50)],
                  fill: nil, focus: CGRect(x: oxygen.x - 40, y: oxygen.y - 50, width: 80, height: 100)),
        Structure(id: "hydrogens", name: "hydrogen symbols", outlines: hydrogens.flatMap(letterH),
                  fill: nil, focusEach: true, groups: [[0, 1, 2], [3, 4, 5]]),
        Structure(id: "bonds", name: "bonds", outlines: hydrogens.map { bond(oxygen, $0) }, fill: nil),
        Structure(id: "lonePairs", name: "lone pairs", outlines: lonePair(angle: -3 * .pi / 4) + lonePair(angle: -.pi / 4),
                  fill: nil, pen: .boldPen, focus: CGRect(x: 400, y: 300, width: 200, height: 80)),
    ]

    static let lesson = Lesson(
        id: "water-lewis",
        title: "Water: Lewis structure",
        level: "High school chemistry",
        subject: .chemistry,
        minutes: 6,
        keywords: ["water", "H2O", "lewis", "lewis dot", "electron dot", "lone pair", "covalent bond", "octet", "valence"],
        colorMode: .inkOnly,
        legend: [],
        structures: structures,
        steps: [
            LessonStep(title: "Count electrons", instruction: "Before drawing, count what you have to work with.", kind: .choice(ChoiceStep(
                question: "How many valence electrons does one oxygen atom have?",
                options: [
                    ChoiceOption(text: "6", correct: true,
                                 feedback: "Right. Oxygen is in group 16, so it has 6 valence electrons. With 1 from each hydrogen, water has 8 in total."),
                    ChoiceOption(text: "8", feedback: "8 is the number oxygen needs around it (an octet), not the number it brings."),
                    ChoiceOption(text: "2", feedback: "Oxygen usually forms 2 bonds, but it has 6 valence electrons."),
                    ChoiceOption(text: "16", feedback: "Oxygen is in group 16, but that's not its electron count. Its valence electrons: 6."),
                ]
            ))),
            LessonStep(title: "Oxygen", instruction: "Trace the O. Oxygen goes in the middle because it can form two bonds.",
                       kind: .trace(structure: "oxygen", part: .outline),
                       note: PartNote(text: "Oxygen has 6 valence electrons and needs 2 more to fill its outer shell, so it forms 2 bonds. That's why it goes in the center.", remember: "O for oxygen; it's in group 16.")),
            LessonStep(title: "Hydrogens", instruction: "Trace each H. Hydrogen can form only one bond, so it goes on the outside.",
                       kind: .trace(structure: "hydrogens", part: .outline),
                       note: PartNote(text: "Hydrogen has 1 electron and needs just 1 more, so it forms only one bond and always sits on the outside.")),
            LessonStep(title: "Bonds", instruction: "Draw a line from the O to each H. Each line is a pair of shared electrons.",
                       kind: .trace(structure: "bonds", part: .outline),
                       note: PartNote(text: "Each line is a covalent bond: a pair of electrons shared between two atoms, one from each.", remember: "One line = two shared electrons.")),
            LessonStep(title: "Lone pairs", instruction: "Add oxygen's two lone pairs, two dots each. Now oxygen has 8 electrons around it.",
                       kind: .trace(structure: "lonePairs", part: .outline),
                       note: PartNote(text: "These 4 electrons belong to oxygen alone. With 2 bonds and 2 lone pairs, oxygen has a full octet of 8.", remember: "Lone pairs push the hydrogens together, so water is bent.")),
            LessonStep(title: "Why bent?", instruction: "Connect your drawing to the molecule's shape.", kind: .choice(ChoiceStep(
                question: "Water's H–O–H angle is about 104.5°, not 180°. Why?",
                options: [
                    ChoiceOption(text: "Oxygen's two lone pairs push the bonds closer together", correct: true,
                                 feedback: "Yes. Four electron groups surround oxygen, and the lone pairs repel more strongly, squeezing the angle below 109.5°."),
                    ChoiceOption(text: "The hydrogen atoms attract each other",
                                 feedback: "Both hydrogens carry a slight positive charge, so they repel each other."),
                    ChoiceOption(text: "Because the Lewis structure was drawn bent",
                                 feedback: "A Lewis structure shows connections and electrons, not 3-D shape. Drawn in a straight line it would still be a correct Lewis structure."),
                    ChoiceOption(text: "Oxygen can only form one bond", feedback: "Oxygen forms two bonds here, one to each hydrogen."),
                ],
                showsDiagram: true
            ))),
            LessonStep(title: "From memory", instruction: "The atoms have moved. Draw a line for each bond and two dots for each lone pair, then press Check.",
                       kind: .drawLewis(LewisStep(target: water, positions: [
                           CGPoint(x: 470, y: 560), CGPoint(x: 720, y: 380), CGPoint(x: 250, y: 400),
                       ]))),
        ],
        grade: "10-11",
        standard: "HS-PS1-1",
        sources: [
            Source(title: "NGSS HS-PS1-1: Use the periodic table to predict properties of elements based on their outermost electrons"),
            Source(title: "AP Chemistry, Unit 2: Lewis diagrams"),
            Source(title: "OpenStax Chemistry 2e, 7.3: Lewis symbols and structures",
                   url: URL(string: "https://openstax.org/books/chemistry-2e/pages/7-3-lewis-symbols-and-structures")),
            Source(title: "OpenStax Chemistry 2e, 7.6: Molecular structure and polarity",
                   url: URL(string: "https://openstax.org/books/chemistry-2e/pages/7-6-molecular-structure-and-polarity")),
        ]
    )
}

enum Catalog {
    static let loaded = LessonFile.bundled()

    static let lessons: [Lesson] = ([PlantCellLesson.lesson, LeafSectionLesson.lesson, WaterLesson.lesson] + loaded.lessons)
        .map { $0.withMemorySteps() }
        .sorted { ($0.band.sortOrder, $0.grade, $0.title) < ($1.band.sortOrder, $1.grade, $1.title) }

    static func lesson(id: String) -> Lesson? { lessons.first { $0.id == id } }
}
