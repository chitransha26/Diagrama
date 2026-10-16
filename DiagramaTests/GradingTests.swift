import CoreGraphics
import Foundation
import Testing
@testable import Diagrama

struct ChemistryValidatorTests {
    private let target = WaterLesson.water

    private func water(lonePairsOnO: Int = 2) -> Molecule {
        var m = Molecule(atoms: [.O, .H, .H])
        m.cycleBond(0, 1)
        m.cycleBond(0, 2)
        m.lonePairs[0] = lonePairsOnO
        return m
    }

    @Test func correctWaterPasses() {
        #expect(ChemistryValidator.issues(in: water(), target: target).isEmpty)
    }

    @Test func missingLonePairsFailWithElectronCount() {
        let issues = ChemistryValidator.issues(in: water(lonePairsOnO: 1), target: target)
        #expect(issues.contains { $0.contains("8 valence electrons") && $0.contains("shows 6") })
        #expect(issues.contains { $0.contains("Oxygen should be surrounded by 8") })
    }

    @Test func hydrogenHydrogenBondFails() {
        var m = water()
        m.cycleBond(1, 2)
        let issues = ChemistryValidator.issues(in: m, target: target)
        #expect(issues.contains { $0.contains("Hydrogen can form only one single bond") })
        #expect(issues.contains { $0.contains("not bonded in water") })
    }

    @Test func doubleBondToHydrogenFailsEvenWithRightElectronTotal() {
        var m = Molecule(atoms: [.O, .H, .H])
        m.cycleBond(0, 1)
        m.cycleBond(0, 1) // O=H
        m.cycleBond(0, 2)
        m.lonePairs[0] = 1 // 2*3 + 2*1 = 8 electrons, but chemically invalid
        #expect(m.electronsShown == 8)
        #expect(!ChemistryValidator.issues(in: m, target: target).isEmpty)
    }

    @Test func lonePairOnHydrogenFails() {
        var m = water()
        m.lonePairs[1] = 1
        let issues = ChemistryValidator.issues(in: m, target: target)
        #expect(issues.contains { $0.contains("can't have a lone pair") })
    }

    @Test func unconnectedAtomIsNamed() {
        var m = Molecule(atoms: [.O, .H, .H])
        m.cycleBond(0, 1)
        m.lonePairs[0] = 3
        let issues = ChemistryValidator.issues(in: m, target: target)
        #expect(issues.first == "Hydrogen 2 isn't bonded to anything. Every atom in water must be connected.")
    }

    @Test func bondCyclesBackToNone() {
        var m = Molecule(atoms: [.O, .H])
        for _ in 0..<4 { m.cycleBond(0, 1) }
        #expect(m.bonds.isEmpty)
    }

    @Test func formalCharges() {
        let m = water()
        #expect(m.atoms.indices.allSatisfy { m.formalCharge($0) == 0 })
    }
}

struct StrokeScorerTests {
    private let circle = Shapes.circle(500, 500, 200)

    @Test func exactTraceScoresFully() {
        let r = StrokeScorer.score(strokes: [circle.resampled(spacing: 5)], guides: [circle], tolerance: 20)
        #expect(r.precision > 0.99)
        #expect(r.coverage > 0.99)
    }

    @Test func halfTraceCoversAboutHalf() {
        let half = (0...50).map { circle.point(at: CGFloat($0) / 100) }
        let r = StrokeScorer.score(strokes: [half], guides: [circle], tolerance: 20)
        #expect(r.precision > 0.99)
        #expect(abs(r.coverage - 0.5) < 0.08)
        #expect(!StrokeScorer.isComplete(r))
    }

    @Test func offsetDrawingIsFlaggedOffGuide() {
        let shifted = circle.resampled(spacing: 5).map { CGPoint(x: $0.x + 80, y: $0.y) }
        let r = StrokeScorer.score(strokes: [shifted], guides: [circle], tolerance: 20)
        #expect(r.precision < 0.6)
        #expect(!r.offGuidePoints.isEmpty)
    }

    @Test func fullTraceIsComplete() {
        let r = StrokeScorer.score(strokes: [circle.resampled(spacing: 5)], guides: [circle], tolerance: 20)
        #expect(StrokeScorer.isComplete(r))
    }

    @Test func smallGapKeepsStepOpen() {
        // Trace the circle but leave about 50 units untraced: the drawing would look broken.
        let partial = (0...92).map { circle.point(at: CGFloat($0) / 100) }
        let r = StrokeScorer.score(strokes: [partial], guides: [circle], tolerance: 20)
        #expect(r.coverage > 0.9)
        #expect(!StrokeScorer.isComplete(r))
        #expect(!r.untraced.isEmpty)
    }

    @Test func skippingOneOfManyPartsKeepsStepOpen() {
        // Eight short lines, like the thylakoids: drawing seven is still not finished.
        let lines = (0..<8).map { i in Shapes.line(CGPoint(x: 100, y: 100 + CGFloat(i) * 60), CGPoint(x: 160, y: 100 + CGFloat(i) * 60)) }
        let drawn = lines.dropLast().map { $0.resampled(spacing: 4) }
        let r = StrokeScorer.score(strokes: drawn, guides: lines, tolerance: 12)
        #expect(r.coverage > 0.8)
        #expect(!StrokeScorer.isComplete(r))
        #expect(r.guideCoverage.last == 0)
    }

    @Test func oneLineBetweenTwoCloseGuidesTracesOnlyOne() {
        let top = Shapes.line(CGPoint(x: 100, y: 100), CGPoint(x: 300, y: 100))
        let bottom = Shapes.line(CGPoint(x: 100, y: 118), CGPoint(x: 300, y: 118))
        let middle = [Shapes.line(CGPoint(x: 100, y: 109), CGPoint(x: 300, y: 109)).resampled(spacing: 4)]
        let r = StrokeScorer.score(strokes: middle, guides: [top, bottom], tolerance: 12)
        #expect(!StrokeScorer.isComplete(r))
    }

    @Test func pencilToleranceIsTighterThanFinger() {
        #expect(StrokeScorer.tolerance(isPencil: true, scale: 0.4) < StrokeScorer.tolerance(isPencil: false, scale: 0.4))
    }

    @Test func smoothLinesScoreHigherThanShakyOnes() {
        let steady = [(0..<100).map { CGPoint(x: CGFloat($0) * 3, y: 100) }]
        let shaky = [(0..<100).map { CGPoint(x: CGFloat($0) * 3, y: 100 + ($0 % 2 == 0 ? 3 : -3)) }]
        #expect(StrokeScorer.smoothness(strokes: steady) > 0.95)
        #expect(StrokeScorer.smoothness(strokes: shaky) < 0.2)
    }

    @Test func recallIgnoresPositionAndSize() {
        let guides = [Shapes.roundedRect(90, 140, 820, 720, r: 70), Shapes.circle(220, 330, 72)]
        // The same drawing at half size, moved to a corner.
        let small = guides.map { g in g.resampled(spacing: 5).map { CGPoint(x: $0.x * 0.5 + 40, y: $0.y * 0.5 + 60) } }
        let r = StrokeScorer.scoreRecall(strokes: small, guides: guides, tolerance: 20)
        #expect(StrokeScorer.recallPassed(r))
    }

    @Test func recallRejectsWrongShape() {
        let guides = [Shapes.roundedRect(90, 140, 820, 720, r: 70), Shapes.circle(220, 330, 72)]
        let scribble = [(0..<40).map { CGPoint(x: CGFloat($0) * 20, y: $0 % 2 == 0 ? 100 : 800) }]
        let r = StrokeScorer.scoreRecall(strokes: scribble, guides: guides, tolerance: 20)
        #expect(!StrokeScorer.recallPassed(r))
    }
}

struct LabelGraderTests {
    private let membrane = LabelTarget(
        id: 1, point: .zero, answer: "Cell membrane", synonyms: ["Plasma membrane"], role: "",
        mistakes: ["Cell wall": "specific"]
    )
    private let step = LabelStep(targets: [], vocabulary: [], commonMistakes: ["Centriole": "common"])

    @Test func acceptsSynonymsAndIgnoresCase() {
        #expect(LabelGrader.isCorrect("plasma membrane", for: membrane))
        #expect(LabelGrader.isCorrect(" Cell Membrane ", for: membrane))
        #expect(!LabelGrader.isCorrect("Cell wall", for: membrane))
    }

    @Test func explainsSpecificThenCommonMistakes() {
        #expect(LabelGrader.explanation(for: "Cell wall", target: membrane, step: step) == "specific")
        #expect(LabelGrader.explanation(for: "Centriole", target: membrane, step: step) == "common")
    }
}

struct ContentTests {
    @Test func everyLessonReferencesRealStructures() {
        for lesson in Catalog.lessons {
            let ids = Set(lesson.structures.map(\.id))
            for step in lesson.steps {
                switch step.kind {
                case .trace(let s, let part):
                    #expect(ids.contains(s), "\(lesson.id)")
                    if part == .details { #expect(!lesson.structure(s).details.isEmpty, "\(lesson.id): \(s) has no details") }
                case .color(let s):
                    #expect(ids.isSuperset(of: s), "\(lesson.id)")
                    for id in s { #expect(lesson.structure(id).fill != nil, "\(lesson.id): \(id) is clear, so it can't be filled") }
                case .recall(let s): #expect(ids.isSuperset(of: s), "\(lesson.id)")
                case .label(let l):
                    for t in l.targets { #expect(l.vocabulary.contains(t.answer), "\(lesson.id) missing \(t.answer)") }
                case .choice(let c): #expect(c.options.filter(\.correct).count == 1, "\(lesson.id): \(c.question)")
                case .identify(let i): #expect(ids.contains(i.structureID), "\(lesson.id)")
                case .drawLewis(let l): #expect(l.positions.count == l.target.atoms.count)
                case .order(let o): #expect(o.items.count > 1)
                }
            }
        }
    }

    @Test func everyStructureIsDrawnBeforeItIsFilledOrLabeled() {
        for lesson in Catalog.lessons where !lesson.structures.isEmpty {
            var drawn: Set<String> = []
            for step in lesson.steps {
                switch step.kind {
                case .trace(let s, let part): drawn.insert(part.key(s))
                case .color(let s): #expect(drawn.isSuperset(of: s), "\(lesson.id): coloring before drawing")
                default: break
                }
            }
            // The learner draws every structure and every detail themselves.
            for s in lesson.structures {
                #expect(drawn.contains(s.id), "\(lesson.id): \(s.id) never drawn")
                if !s.details.isEmpty { #expect(drawn.contains(s.id + ".details"), "\(lesson.id): \(s.id) details never drawn") }
            }
        }
    }

    @Test func zoomKeepsFocusVisible() {
        for lesson in Catalog.lessons {
            for s in lesson.structures {
                guard let f = s.focus else { continue }
                let v = Viewport(focus: f)
                let visible = CGRect(origin: v.origin, size: CGSize(width: 1000 / v.zoom, height: 1000 / v.zoom))
                for o in s.outlines + s.details {
                    #expect(visible.contains(o.bounds), "\(lesson.id): \(s.id) is cut off when zoomed")
                }
            }
        }
    }

    @Test func everyDrawingStepHasANote() {
        for lesson in Catalog.lessons {
            for step in lesson.steps {
                if step.isDrawing {
                    #expect(step.note != nil, "\(lesson.id): \(step.title) has no note")
                    let length = (step.note?.text.count ?? 0) + (step.note?.remember?.count ?? 0)
                    #expect(length <= 180, "\(lesson.id): \(step.title) note is too long for the card")
                }
            }
        }
    }

    @Test func searchFindsSynonyms() {
        #expect(Catalog.lessons.filter { $0.matches("plasma membrane") }.map(\.id) == ["plant-cell"])
        #expect(Catalog.lessons.filter { $0.matches("H2O") }.map(\.id) == ["water-lewis"])
    }
}

struct ProgressStoreTests {
    private func tempStore() -> ProgressStore {
        ProgressStore(directory: FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString))
    }

    private func record(_ independent: Bool, daysAgo: Double) -> AttemptRecord {
        AttemptRecord(lessonID: "plant-cell", date: Date().addingTimeInterval(-daysAgo * 86_400),
                      match: 900, smoothness: 250, firstTry: 40, duration: 300,
                      scienceCorrect: 5, scienceTotal: 7, independent: independent)
    }

    @Test func statusProgression() {
        let store = tempStore()
        #expect(store.status(for: "plant-cell") == .notStarted)
        store.add(record(false, daysAgo: 10), image: nil)
        #expect(store.status(for: "plant-cell") == .practiced)
        store.add(record(true, daysAgo: 9), image: nil)
        #expect(store.status(for: "plant-cell") == .independent)
        store.add(record(true, daysAgo: 0), image: nil)
        #expect(store.status(for: "plant-cell") == .retained)
    }

    @Test func persistsAcrossLaunches() {
        let dir = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        ProgressStore(directory: dir).add(record(true, daysAgo: 0), image: nil)
        #expect(ProgressStore(directory: dir).attempts.count == 1)
    }
}

struct LewisInterpreterTests {
    private let atoms: [Element] = [.O, .H, .H]
    private let positions = [CGPoint(x: 470, y: 560), CGPoint(x: 720, y: 380), CGPoint(x: 250, y: 400)]

    private func line(_ a: CGPoint, _ b: CGPoint) -> [CGPoint] {
        (0...20).map { a.lerp(to: b, CGFloat($0) / 20) }
    }

    private func dot(_ p: CGPoint) -> [CGPoint] {
        [p, CGPoint(x: p.x + 3, y: p.y + 2)]
    }

    /// Bonds drawn from just outside one symbol to just outside the other.
    private func bond(_ i: Int, _ j: Int) -> [CGPoint] {
        let a = positions[i], b = positions[j]
        return line(a.lerp(to: b, 0.25), a.lerp(to: b, 0.75))
    }

    private var lonePairs: [[CGPoint]] {
        let o = positions[0]
        return [dot(CGPoint(x: o.x - 15, y: o.y + 90)), dot(CGPoint(x: o.x + 15, y: o.y + 90)),
                dot(CGPoint(x: o.x - 90, y: o.y + 15)), dot(CGPoint(x: o.x - 90, y: o.y - 15))]
    }

    private func grade(_ strokes: [[CGPoint]]) -> [String] {
        let r = LewisInterpreter.read(strokes: strokes, atoms: atoms, positions: positions)
        return r.notes + ChemistryValidator.issues(in: r.molecule, target: WaterLesson.water)
    }

    @Test func correctDrawingPasses() {
        #expect(grade([bond(0, 1), bond(0, 2)] + lonePairs).isEmpty)
    }

    @Test func strokeDirectionDoesNotMatter() {
        let reversed = [Array(bond(0, 1).reversed()), bond(0, 2)] + lonePairs
        #expect(grade(reversed).isEmpty)
    }

    @Test func missingLonePairIsCaught() {
        let issues = grade([bond(0, 1), bond(0, 2)] + lonePairs.prefix(2))
        #expect(issues.contains { $0.contains("8 valence electrons") })
    }

    @Test func oddDotIsNamed() {
        let issues = grade([bond(0, 1), bond(0, 2)] + lonePairs.prefix(3))
        #expect(issues.first?.contains("odd number of dots around oxygen") == true)
    }

    @Test func twoLinesMakeADoubleBond() {
        let r = LewisInterpreter.read(strokes: [bond(0, 1), bond(0, 1)], atoms: atoms, positions: positions)
        #expect(r.molecule.bondOrder(0, 1) == 2)
    }

    @Test func hydrogenToHydrogenLineIsWrong() {
        let issues = grade([bond(0, 1), bond(0, 2), bond(1, 2)] + lonePairs)
        #expect(issues.contains { $0.contains("not bonded in water") })
    }

    @Test func strayLineIsReported() {
        let stray = line(CGPoint(x: 60, y: 900), CGPoint(x: 300, y: 900))
        let r = LewisInterpreter.read(strokes: [bond(0, 1), bond(0, 2), stray] + lonePairs, atoms: atoms, positions: positions)
        #expect(r.notes.contains { $0.contains("doesn't run from one atom to another") })
    }

    @Test func guidedLessonGuidesFormACorrectStructure() {
        // The traced bonds and lone pairs in the guided steps must themselves read as correct water.
        let lesson = WaterLesson.lesson
        let strokes = (lesson.structure("bonds").outlines + lesson.structure("lonePairs").outlines).map(\.points)
        let r = LewisInterpreter.read(strokes: strokes, atoms: atoms,
                                      positions: [CGPoint(x: 500, y: 400), CGPoint(x: 300, y: 580), CGPoint(x: 700, y: 580)])
        #expect(r.notes.isEmpty)
        #expect(ChemistryValidator.issues(in: r.molecule, target: WaterLesson.water).isEmpty)
    }
}

struct IdentifyTests {
    private let lesson = PlantCellLesson.lesson
    private let drawn: Set<String> = ["wall", "membrane", "vacuole", "nucleus", "chloroplast"]

    @Test func cytoplasmIsTheSpaceAroundTheOrganelles() {
        // Between the membrane and the vacuole: cytoplasm (the membrane region).
        #expect(lesson.hit(at: CGPoint(x: 220, y: 720), among: drawn)?.structure.id == "membrane")
        // Inside the vacuole, nucleus or a chloroplast: not cytoplasm.
        #expect(lesson.hit(at: CGPoint(x: 580, y: 480), among: drawn)?.structure.id == "vacuole")
        #expect(lesson.hit(at: CGPoint(x: 220, y: 330), among: drawn)?.structure.id == "nucleus")
        #expect(lesson.hit(at: CGPoint(x: 225, y: 600), among: drawn)?.structure.id == "chloroplast")
        // Outside the cell.
        #expect(lesson.hit(at: CGPoint(x: 40, y: 40), among: drawn) == nil)
    }
}
