import SwiftUI

/// A leaf cell (like Elodea) as seen fresh and unstained under a light microscope.
enum PlantCellLesson {
    /// Chlorophyll green: the only clearly colored part of an unstained plant cell.
    private static let chloroplastColor = Color(red: 0.30, green: 0.62, blue: 0.22)

    private static let chloroplastCenters: [CGPoint] = [
        CGPoint(x: 225, y: 600), CGPoint(x: 220, y: 475), CGPoint(x: 470, y: 785), CGPoint(x: 690, y: 785),
    ]

    static let structures: [Structure] = [
        Structure(id: "wall", name: "cell wall", outlines: [Shapes.roundedRect(90, 140, 820, 720, r: 70)],
                  fill: nil, pen: .boldPen),
        Structure(id: "membrane", name: "cell membrane", outlines: [Shapes.roundedRect(116, 166, 768, 668, r: 52)],
                  fill: nil, colorName: "cytoplasm", pen: .fineLiner),
        Structure(id: "vacuole", name: "central vacuole", outlines: [Shapes.roundedRect(330, 230, 500, 500, r: 150)],
                  fill: nil),
        Structure(
            id: "nucleus", name: "nucleus", outlines: [Shapes.circle(220, 330, 72)], fill: nil,
            details: [Shapes.circle(236, 316, 22)],
            pen: .fineLiner, focus: CGRect(x: 130, y: 240, width: 180, height: 180)
        ),
        Structure(
            id: "chloroplast", name: "chloroplasts",
            outlines: chloroplastCenters.map { Shapes.ellipse($0.x, $0.y, 58, 30) },
            fill: chloroplastColor,
            details: chloroplastCenters.flatMap { c in
                [-10, 10].map { dy in
                    Shapes.line(CGPoint(x: c.x - 32, y: c.y + CGFloat(dy)), CGPoint(x: c.x + 32, y: c.y + CGFloat(dy)))
                }
            },
            pen: .fineLiner, focusEach: true
        ),
    ]

    static let lesson = Lesson(
        id: "plant-cell",
        title: "Plant cell",
        level: "Middle & high school · NGSS MS-LS1-2",
        subject: .cellBiology,
        minutes: 10,
        keywords: ["cell", "organelle", "plasma membrane", "cell wall", "vacuole", "chloroplast", "thylakoid", "nucleus", "nucleolus", "cytoplasm", "elodea"],
        colorMode: .lightMicroscope,
        legend: [
            LegendEntry(name: "Chloroplasts", color: chloroplastColor, meaning: "Green from chlorophyll: the only clearly colored part"),
            LegendEntry(name: "Cell wall", color: nil, meaning: "Colorless cellulose; you see its edge"),
            LegendEntry(name: "Cytoplasm", color: nil, meaning: "Nearly colorless fluid"),
            LegendEntry(name: "Central vacuole", color: nil, meaning: "Mostly water"),
            LegendEntry(name: "Nucleus", color: nil, meaning: "Colorless and hard to see without a stain"),
        ],
        structures: structures,
        steps: [
            LessonStep(title: "Cell wall", instruction: "Trace the outer boundary. In plants this rigid wall gives the cell its boxy shape.",
                       kind: .trace(structure: "wall", part: .outline)),
            LessonStep(title: "Cell membrane", instruction: "Trace just inside the wall. The membrane controls what enters and leaves the cell.",
                       kind: .trace(structure: "membrane", part: .outline)),
            LessonStep(title: "Central vacuole", instruction: "Trace the large vacuole. Full of water, it pushes outward and keeps the cell firm.",
                       kind: .trace(structure: "vacuole", part: .outline)),
            LessonStep(title: "Nucleus", instruction: "Trace the nucleus. It holds the cell's DNA.",
                       kind: .trace(structure: "nucleus", part: .outline)),
            LessonStep(title: "Nucleolus", instruction: "Draw the nucleolus inside the nucleus. It makes the parts of ribosomes.",
                       kind: .trace(structure: "nucleus", part: .details)),
            LessonStep(title: "Chloroplasts", instruction: "Trace all four chloroplasts. This is where photosynthesis happens.",
                       kind: .trace(structure: "chloroplast", part: .outline)),
            LessonStep(title: "Thylakoids", instruction: "Draw the stacked membranes inside each chloroplast. They capture light energy.",
                       kind: .trace(structure: "chloroplast", part: .details)),
            LessonStep(title: "Color", instruction: "In a fresh, unstained cell only the chloroplasts have color. The green is chlorophyll.",
                       kind: .color(structures: ["chloroplast"])),
            LessonStep(title: "Label the cell", instruction: "Pick the right name for each numbered marker.", kind: .label(LabelStep(
                targets: [
                    LabelTarget(id: 1, point: CGPoint(x: 103, y: 450), answer: "Cell wall",
                                role: "Rigid layer of cellulose that supports the cell and stops it bursting.",
                                mistakes: ["Cell membrane": "The membrane is the thin layer just inside. Marker 1 is on the thicker outer layer: the wall.",
                                           "Plasma membrane": "The membrane is the thin layer just inside. Marker 1 is on the thicker outer layer: the wall."]),
                    LabelTarget(id: 2, point: CGPoint(x: 116, y: 690), answer: "Cell membrane", synonyms: ["Plasma membrane"],
                                role: "Controls what enters and leaves. In plants it is pressed against the inside of the wall.",
                                mistakes: ["Cell wall": "The wall is the outer layer. This marker is on the thin line just inside it: the membrane."]),
                    LabelTarget(id: 3, point: CGPoint(x: 580, y: 480), answer: "Central vacuole",
                                role: "Stores water and dissolved substances. Its pressure keeps the cell firm (turgid)."),
                    LabelTarget(id: 4, point: CGPoint(x: 195, y: 360), answer: "Nucleus",
                                role: "Contains the DNA and controls the cell's activities.",
                                mistakes: ["Nucleolus": "The nucleolus is the small dot inside. This marker is on the larger structure around it: the nucleus."]),
                    LabelTarget(id: 5, point: CGPoint(x: 225, y: 600), answer: "Chloroplast",
                                role: "Captures light energy to make sugar by photosynthesis.",
                                mistakes: ["Mitochondrion": "Mitochondria release energy from food (respiration). This green, stacked structure captures light: it's a chloroplast."]),
                    LabelTarget(id: 6, point: CGPoint(x: 245, y: 205), answer: "Cytoplasm",
                                role: "Jelly-like fluid where many of the cell's reactions happen."),
                ],
                vocabulary: ["Cell wall", "Cell membrane", "Plasma membrane", "Central vacuole", "Nucleus", "Nucleolus", "Chloroplast", "Cytoplasm", "Mitochondrion", "Centriole"],
                commonMistakes: [
                    "Centriole": "Centrioles are found in animal cells. Most plant cells don't have them.",
                    "Mitochondrion": "Plant cells do have mitochondria, but they're too small to show at this scale and none is marked here.",
                ]
            ))),
            LessonStep(title: "Explain", instruction: "Use what you've drawn.", kind: .choice(ChoiceStep(
                question: "A plant cell sits in fresh water and keeps taking in water. What stops it from bursting?",
                options: [
                    ChoiceOption(text: "The cell wall", correct: true,
                                 feedback: "Right. The swelling vacuole presses the membrane against the rigid wall, which pushes back. This firmness is called turgor."),
                    ChoiceOption(text: "The cell membrane",
                                 feedback: "The membrane is thin and flexible. An animal cell, which has only a membrane, can burst in fresh water."),
                    ChoiceOption(text: "The nucleus", feedback: "The nucleus holds DNA. It doesn't resist water pressure."),
                    ChoiceOption(text: "The chloroplasts", feedback: "Chloroplasts make sugar using light. They don't hold the cell's shape."),
                ],
                showsDiagram: true
            ))),
            LessonStep(title: "From memory", instruction: "No guides this time. Draw the cell wall and the nucleus in the right place. Any size is fine.",
                       kind: .recall(structures: ["wall", "nucleus"])),
        ]
    )
}
