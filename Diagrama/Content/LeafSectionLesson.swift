import SwiftUI

/// A dicot leaf in transverse section, as seen fresh and unstained under a light microscope.
enum LeafSectionLesson {
    /// Densely packed chloroplasts make the palisade layer the deepest green.
    private static let palisadeColor = Color(red: 0.27, green: 0.57, blue: 0.20)
    /// Fewer chloroplasts and air spaces make the spongy layer a paler green.
    private static let spongyColor = Color(red: 0.56, green: 0.76, blue: 0.41)
    /// Guard cells contain chloroplasts, unlike the rest of the epidermis.
    private static let guardColor = Color(red: 0.33, green: 0.63, blue: 0.25)

    private static let palisadeCells: [Polyline] = (0..<10).map { k in
        Shapes.roundedRect(87 + CGFloat(k) * 84, 282, 70, 186, r: 26, cornerSegments: 4)
    }

    private static let spongyCells: [Polyline] = [
        (130, 530), (190, 630), (440, 520), (480, 625), (560, 560), (760, 530), (830, 620), (880, 520), (760, 650),
    ].map { Shapes.circle($0.0, $0.1, 26) }

    private static func epidermisWalls(y: CGFloat, skip: ClosedRange<CGFloat>? = nil) -> [Polyline] {
        stride(from: CGFloat(150), through: 850, by: 100)
            .filter { x in !(skip?.contains(x) ?? false) }
            .map { Shapes.line(CGPoint(x: $0, y: y), CGPoint(x: $0, y: y + 55)) }
    }

    static let structures: [Structure] = [
        Structure(id: "spongy", name: "spongy layer", outlines: [Shapes.roundedRect(80, 475, 840, 215, r: 4)],
                  fill: spongyColor, details: spongyCells, colorName: "spongy mesophyll"),
        Structure(id: "upper", name: "upper epidermis", outlines: [Shapes.roundedRect(80, 220, 840, 55, r: 8)],
                  fill: nil, details: epidermisWalls(y: 220), pen: .fineLiner),
        Structure(id: "palisade", name: "palisade layer", outlines: [Shapes.roundedRect(80, 275, 840, 200, r: 4)],
                  fill: palisadeColor, details: palisadeCells, colorName: "palisade mesophyll"),
        Structure(
            id: "vein", name: "vascular bundle", outlines: [Shapes.ellipse(300, 575, 85, 75)], fill: nil,
            details: [
                Shapes.line(CGPoint(x: 220, y: 580), CGPoint(x: 380, y: 580)),
                Shapes.circle(268, 548, 15), Shapes.circle(304, 536, 15), Shapes.circle(338, 552, 13),
                Shapes.circle(280, 610, 9), Shapes.circle(308, 618, 9), Shapes.circle(334, 606, 9),
            ],
            focus: CGRect(x: 205, y: 490, width: 190, height: 170)
        ),
        Structure(id: "lower", name: "lower epidermis", outlines: [Shapes.roundedRect(80, 690, 840, 55, r: 8)],
                  fill: nil, details: epidermisWalls(y: 690, skip: 600...740), pen: .fineLiner),
        Structure(id: "guard", name: "guard cells", outlines: [Shapes.ellipse(641, 717, 25, 22), Shapes.ellipse(695, 717, 25, 22)],
                  fill: guardColor, pen: .fineLiner, focus: CGRect(x: 600, y: 680, width: 140, height: 75)),
    ]

    static let lesson = Lesson(
        id: "leaf-section",
        title: "Leaf cross-section",
        level: "High school & AP Biology",
        subject: .botany,
        minutes: 14,
        keywords: ["leaf", "transverse section", "mesophyll", "palisade", "spongy", "stoma", "stomata", "guard cell", "xylem", "phloem", "vein", "photosynthesis"],
        colorMode: .lightMicroscope,
        legend: [
            LegendEntry(name: "Palisade mesophyll", color: palisadeColor, meaning: "Deepest green: packed with chloroplasts"),
            LegendEntry(name: "Spongy mesophyll", color: spongyColor, meaning: "Paler green: fewer chloroplasts, plus air spaces"),
            LegendEntry(name: "Guard cells", color: guardColor, meaning: "Green: they have chloroplasts, unlike other epidermis cells"),
            LegendEntry(name: "Epidermis", color: nil, meaning: "Colorless, so light passes through"),
            LegendEntry(name: "Vascular bundle", color: nil, meaning: "Colorless unless stained (xylem stains red with safranin)"),
        ],
        structures: structures,
        steps: [
            LessonStep(title: "Upper epidermis", instruction: "Trace the top layer. This thin, clear skin lets light through to the cells below.",
                       kind: .trace(structure: "upper", part: .outline),
                       note: PartNote(text: "A single layer of clear cells that protects the leaf and lets light through. A waxy cuticle on top cuts water loss.", remember: "Clear like a window, so light reaches the cells below.")),
            LessonStep(title: "Epidermis cells", instruction: "Draw the walls between the epidermis cells.",
                       kind: .trace(structure: "upper", part: .details),
                       note: PartNote(text: "Epidermis cells fit tightly together with no gaps, sealing the leaf against germs and drying out.")),
            LessonStep(title: "Palisade layer", instruction: "Trace the palisade layer. Most photosynthesis happens here.",
                       kind: .trace(structure: "palisade", part: .outline),
                       note: PartNote(text: "Where most photosynthesis happens. It sits just under the top surface, where the light is strongest.", remember: "Palisade means a fence of upright posts.")),
            LessonStep(title: "Palisade cells", instruction: "Draw the tall, tightly packed palisade cells.",
                       kind: .trace(structure: "palisade", part: .details),
                       note: PartNote(text: "Tall, column-shaped cells packed with chloroplasts. Standing upright lets many fit side by side to catch the light.")),
            LessonStep(title: "Spongy layer", instruction: "Trace the spongy layer below the palisade.",
                       kind: .trace(structure: "spongy", part: .outline),
                       note: PartNote(text: "Loosely packed cells with air spaces between them. Carbon dioxide spreads through these spaces to reach the cells that need it.", remember: "Spongy like a sponge: full of holes for air.")),
            LessonStep(title: "Spongy cells", instruction: "Draw the loosely packed spongy cells. The gaps between them are air spaces for gases.",
                       kind: .trace(structure: "spongy", part: .details),
                       note: PartNote(text: "Round, irregular cells. The gaps between them form air channels linking the stomata to the palisade layer.")),
            LessonStep(title: "Vein", instruction: "Trace the vascular bundle, the leaf's vein.",
                       kind: .trace(structure: "vein", part: .outline),
                       note: PartNote(text: "The vascular bundle is the leaf's plumbing. It brings water in, carries sugar out, and helps hold the leaf up.")),
            LessonStep(title: "Xylem and phloem", instruction: "Draw the xylem vessels on top (they carry water) and the smaller phloem below (it carries sugar).",
                       kind: .trace(structure: "vein", part: .details),
                       note: PartNote(text: "Xylem tubes carry water and minerals up from the roots. Phloem carries the sugar made in the leaf to the rest of the plant.", remember: "Phloem carries food: both start with an “f” sound.")),
            LessonStep(title: "Lower epidermis", instruction: "Trace the bottom layer of the leaf.",
                       kind: .trace(structure: "lower", part: .outline),
                       note: PartNote(text: "The underside skin of the leaf. Most stomata are here, on the cooler, shadier side, which reduces water loss.")),
            LessonStep(title: "Lower epidermis cells", instruction: "Draw the walls between the lower epidermis cells.",
                       kind: .trace(structure: "lower", part: .details),
                       note: PartNote(text: "Like the upper surface, these cells fit tightly together, except where pairs of guard cells leave a pore.")),
            LessonStep(title: "Guard cells", instruction: "Draw the two guard cells. The gap between them is a stoma, which lets CO₂ in and water vapor out.",
                       kind: .trace(structure: "guard", part: .outline),
                       note: PartNote(text: "Two curved cells that open and close the stoma between them. Open lets carbon dioxide in for photosynthesis; closed saves water.", remember: "Guard cells guard the gate of the leaf.")),
            LessonStep(title: "Color", instruction: "In a fresh leaf, the green comes from chloroplasts. The epidermis and vein are colorless.",
                       kind: .color(structures: ["palisade", "spongy", "guard"])),
            LessonStep(title: "Layer order", instruction: "Tap the layers in order, from the top surface of the leaf to the bottom.", kind: .order(OrderStep(
                items: ["Upper epidermis", "Palisade mesophyll", "Spongy mesophyll", "Lower epidermis"],
                why: "Light enters from the top, so the palisade layer, which does most photosynthesis, sits just under the upper epidermis. Most stomata are in the lower epidermis.",
                hint: "Think about which layer light reaches first."
            ))),
            LessonStep(title: "Label the leaf", instruction: "Pick the right name for each numbered marker.", kind: .label(LabelStep(
                targets: [
                    LabelTarget(id: 1, point: CGPoint(x: 500, y: 247), answer: "Upper epidermis",
                                role: "A transparent protective layer that lets light reach the cells below."),
                    LabelTarget(id: 2, point: CGPoint(x: 717, y: 375), answer: "Palisade mesophyll", synonyms: ["Palisade layer"],
                                role: "Tall, tightly packed cells full of chloroplasts: the main site of photosynthesis.",
                                mistakes: ["Spongy mesophyll": "Spongy cells are loosely packed with air spaces. These tall, tightly packed cells are palisade."]),
                    LabelTarget(id: 3, point: CGPoint(x: 660, y: 580), answer: "Spongy mesophyll", synonyms: ["Spongy layer"],
                                role: "Loosely packed cells whose air spaces let CO₂ and water vapor diffuse through the leaf.",
                                mistakes: ["Palisade mesophyll": "Palisade cells are the tall, packed ones higher up. This loose layer with air spaces is spongy mesophyll."]),
                    LabelTarget(id: 4, point: CGPoint(x: 304, y: 536), answer: "Xylem",
                                role: "Carries water and minerals up from the roots.",
                                mistakes: ["Phloem": "Phloem carries sugar and usually sits on the lower side of a leaf vein. These larger tubes on the upper side are xylem, which carry water."]),
                    LabelTarget(id: 5, point: CGPoint(x: 308, y: 618), answer: "Phloem",
                                role: "Carries sugars made in the leaf to the rest of the plant.",
                                mistakes: ["Xylem": "Xylem sits on the upper side of the vein. This smaller group on the lower side is phloem, which carries sugar."]),
                    LabelTarget(id: 6, point: CGPoint(x: 668, y: 717), answer: "Stoma", synonyms: ["Stomata", "Stomate"],
                                role: "A pore between two guard cells that lets CO₂ in and water vapor out.",
                                mistakes: ["Lower epidermis": "The marker is on the gap between the two guard cells: that pore is a stoma, in the lower epidermis."]),
                ],
                vocabulary: ["Upper epidermis", "Palisade mesophyll", "Spongy mesophyll", "Lower epidermis", "Xylem", "Phloem", "Stoma", "Cuticle", "Root hair"],
                commonMistakes: [
                    "Root hair": "Root hairs grow on roots, not leaves. They absorb water from the soil.",
                    "Cuticle": "The cuticle is the waxy coating on top of the epidermis. It's too thin to mark at this scale.",
                ]
            ))),
            LessonStep(title: "Predict", instruction: "Think about how the parts work together.", kind: .choice(ChoiceStep(
                question: "On a hot, dry afternoon the guard cells close the stomata. What happens next?",
                options: [
                    ChoiceOption(text: "Less carbon dioxide enters, so photosynthesis slows", correct: true,
                                 feedback: "Yes. Closing the stomata saves water, but it also cuts off the CO₂ that the palisade cells need."),
                    ChoiceOption(text: "More carbon dioxide enters the leaf",
                                 feedback: "CO₂ gets in through open stomata. With them closed, less gets in."),
                    ChoiceOption(text: "The leaf loses water faster",
                                 feedback: "Closing stomata reduces water loss. That's why plants close them when it's dry."),
                    ChoiceOption(text: "The xylem starts carrying sugar",
                                 feedback: "Xylem carries water and minerals; sugar travels in phloem. Closing stomata doesn't change that."),
                ],
                showsDiagram: true
            ))),
            LessonStep(title: "From memory", instruction: "No guides this time. Draw the palisade layer and the vein below it. Any size is fine.",
                       kind: .recall(structures: ["palisade", "vein"])),
        ]
    )
}
