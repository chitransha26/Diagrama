import SwiftUI

enum WaterLesson {
    static let water = MoleculeTarget(
        name: "water",
        atoms: [.O, .H, .H],
        bonds: [BondKey(0, 1): 1, BondKey(0, 2): 1]
    )

    static let lesson = Lesson(
        id: "water-lewis",
        title: "Water: Lewis structure",
        level: "High school & AP Chemistry",
        subject: .chemistry,
        minutes: 5,
        keywords: ["water", "H2O", "lewis", "lewis dot", "electron dot", "lone pair", "covalent bond", "octet", "valence"],
        colorMode: .elementConvention,
        legend: [
            LegendEntry(name: "Oxygen", color: ElementStyle.fill(.O), meaning: "Red by convention, not an error"),
            LegendEntry(name: "Hydrogen", color: ElementStyle.fill(.H), meaning: "White by convention"),
        ],
        structures: [],
        steps: [
            LessonStep(title: "Count electrons", instruction: "Before building, count what you have to work with.", kind: .choice(ChoiceStep(
                question: "How many valence electrons does one oxygen atom have?",
                options: [
                    ChoiceOption(text: "6", correct: true,
                                 feedback: "Right. Oxygen is in group 16, so it has 6 valence electrons. With 1 from each hydrogen, water has 8 in total."),
                    ChoiceOption(text: "8", feedback: "8 is the number oxygen needs around it (an octet), not the number it brings."),
                    ChoiceOption(text: "2", feedback: "Oxygen usually forms 2 bonds, but it has 6 valence electrons."),
                    ChoiceOption(text: "16", feedback: "Oxygen is in group 16, but that's not its electron count. Its valence electrons: 6."),
                ]
            ))),
            LessonStep(title: "Build water", instruction: "Tap + between atoms to add a bond. Select an atom to give it lone pairs. Make every atom complete.",
                       kind: .build(BuildStep(target: water, positions: [
                           CGPoint(x: 500, y: 420), CGPoint(x: 290, y: 610), CGPoint(x: 710, y: 610),
                       ]))),
            LessonStep(title: "Why bent?", instruction: "Connect the structure to the molecule's shape.", kind: .choice(ChoiceStep(
                question: "Water's H–O–H angle is about 104.5°, not 180°. Why?",
                options: [
                    ChoiceOption(text: "Oxygen's two lone pairs push the bonds closer together", correct: true,
                                 feedback: "Yes. Four electron groups surround oxygen, and the lone pairs repel more strongly, squeezing the angle below 109.5°."),
                    ChoiceOption(text: "The hydrogen atoms attract each other",
                                 feedback: "Both hydrogens carry a slight positive charge, so they repel each other."),
                    ChoiceOption(text: "Because the Lewis structure was drawn bent",
                                 feedback: "A Lewis structure shows connections and electrons, not 3-D shape. Drawn in a straight line it would still be a correct Lewis structure."),
                    ChoiceOption(text: "Oxygen can only form one bond", feedback: "Oxygen forms two bonds here, one to each hydrogen."),
                ]
            ))),
            LessonStep(title: "From memory", instruction: "Build water again. The atoms have moved and the electron counter is hidden.",
                       kind: .build(BuildStep(target: water, positions: [
                           CGPoint(x: 470, y: 560), CGPoint(x: 720, y: 390), CGPoint(x: 250, y: 380),
                       ], isRecall: true))),
        ]
    )
}

enum Catalog {
    static let lessons: [Lesson] = [PlantCellLesson.lesson, LeafSectionLesson.lesson, WaterLesson.lesson]

    static func lesson(id: String) -> Lesson? { lessons.first { $0.id == id } }
}
