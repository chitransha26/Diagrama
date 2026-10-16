import SwiftUI

enum ElementStyle {
    static func fill(_ e: Element) -> Color {
        switch e {
        case .O: Color(red: 0.90, green: 0.22, blue: 0.20)
        case .H: .white
        case .C: Color(white: 0.25)
        case .N: Color(red: 0.20, green: 0.35, blue: 0.90)
        }
    }

    static func text(_ e: Element) -> Color { e == .H ? Theme.ink : .white }
}

/// Draws a Lewis structure. When interactive, bonds and atoms can be tapped.
struct MoleculeCanvas: View {
    let molecule: Molecule
    let positions: [CGPoint]
    var selected: Int? = nil
    var interactive = false
    var onTapAtom: (Int) -> Void = { _ in }
    var onTapBond: (Int, Int) -> Void = { _, _ in }

    private let atomRadius: CGFloat = 70

    private var pairs: [BondKey] {
        molecule.atoms.indices.flatMap { i in (i + 1..<molecule.atoms.count).map { BondKey(i, $0) } }
    }

    var body: some View {
        GeometryReader { geo in
            let s = geo.size.width / DiagramSpace.size
            ZStack {
                Canvas { ctx, size in
                    ctx.fill(Path(CGRect(origin: .zero, size: size)), with: .color(Theme.paper))
                    ctx.scaleBy(x: s, y: s)
                    drawBonds(in: &ctx)
                    drawAtoms(in: &ctx)
                }
                .accessibilityHidden(true)

                if interactive {
                    ForEach(molecule.atoms.indices, id: \.self) { i in
                        Button {
                            onTapAtom(i)
                        } label: {
                            Color.clear
                                .frame(width: 2 * atomRadius * s, height: 2 * atomRadius * s)
                                .contentShape(Circle())
                        }
                        .position(x: positions[i].x * s, y: positions[i].y * s)
                        .accessibilityLabel("\(molecule.atomName(i).capitalized), \(molecule.lonePairs[i]) lone pairs")
                        .accessibilityHint("Select to change its lone pairs")
                    }
                    ForEach(pairs, id: \.self) { key in
                        bondHandle(key, scale: s)
                    }
                }
            }
        }
        .aspectRatio(1, contentMode: .fit)
    }

    private func bondHandle(_ key: BondKey, scale s: CGFloat) -> some View {
        let mid = positions[key.a].lerp(to: positions[key.b], 0.5)
        let order = molecule.bondOrder(key.a, key.b)
        let names = ["no bond", "single bond", "double bond", "triple bond"]
        return Button {
            onTapBond(key.a, key.b)
        } label: {
            Text(order == 0 ? "+" : "\(order)")
                .font(.system(size: 15, weight: .bold))
                .foregroundStyle(order == 0 ? Theme.indigo : .white)
                .frame(width: 30, height: 30)
                .background(Circle().fill(order == 0 ? Color.white : Theme.indigo))
                .overlay(Circle().stroke(Theme.indigo, lineWidth: 2))
                .frame(width: 44, height: 44)
                .contentShape(Rectangle())
        }
        .position(x: mid.x * s, y: mid.y * s)
        .accessibilityLabel("Bond between \(molecule.atomName(key.a)) and \(molecule.atomName(key.b)): \(names[order])")
        .accessibilityHint("Tap to change the bond")
    }

    private func drawBonds(in ctx: inout GraphicsContext) {
        for (key, order) in molecule.bonds where order > 0 {
            let a = positions[key.a], b = positions[key.b]
            let len = a.distance(to: b)
            guard len > 0 else { continue }
            let n = CGPoint(x: -(b.y - a.y) / len, y: (b.x - a.x) / len)
            let offsets: [CGFloat] = switch order {
            case 1: [0]
            case 2: [-11, 11]
            default: [-18, 0, 18]
            }
            for o in offsets {
                var p = Path()
                p.move(to: CGPoint(x: a.x + n.x * o, y: a.y + n.y * o))
                p.addLine(to: CGPoint(x: b.x + n.x * o, y: b.y + n.y * o))
                ctx.stroke(p, with: .color(Theme.ink), style: StrokeStyle(lineWidth: 7, lineCap: .round))
            }
        }
    }

    private func drawAtoms(in ctx: inout GraphicsContext) {
        for (i, e) in molecule.atoms.enumerated() {
            let c = positions[i]
            let circle = Path(ellipseIn: CGRect(x: c.x - atomRadius, y: c.y - atomRadius, width: 2 * atomRadius, height: 2 * atomRadius))
            if selected == i {
                let r = atomRadius + 16
                ctx.stroke(Path(ellipseIn: CGRect(x: c.x - r, y: c.y - r, width: 2 * r, height: 2 * r)),
                           with: .color(Theme.cyan), lineWidth: 8)
            }
            ctx.fill(circle, with: .color(ElementStyle.fill(e)))
            ctx.stroke(circle, with: .color(Theme.ink), lineWidth: 4)
            ctx.draw(Text(e.rawValue).font(.system(size: 60, weight: .bold, design: .rounded)).foregroundStyle(ElementStyle.text(e)), at: c)
            if molecule.atoms.filter({ $0 == e }).count > 1 {
                let n = molecule.atoms[...i].filter { $0 == e }.count
                ctx.draw(Text("\(n)").font(.system(size: 26, weight: .semibold)).foregroundStyle(ElementStyle.text(e)),
                         at: CGPoint(x: c.x + 34, y: c.y + 32))
            }
            for angle in lonePairAngles(i) {
                let center = CGPoint(x: c.x + 108 * cos(angle), y: c.y + 108 * sin(angle))
                for side in [-1.0, 1.0] {
                    let d = CGPoint(x: center.x - sin(angle) * 15 * side, y: center.y + cos(angle) * 15 * side)
                    ctx.fill(Path(ellipseIn: CGRect(x: d.x - 8, y: d.y - 8, width: 16, height: 16)), with: .color(Theme.ink))
                }
            }
        }
    }

    /// Places lone pairs in the directions farthest from bonds and from each other.
    private func lonePairAngles(_ i: Int) -> [CGFloat] {
        var taken: [CGFloat] = molecule.atoms.indices
            .filter { $0 != i && molecule.bondOrder(i, $0) > 0 }
            .map { atan2(positions[$0].y - positions[i].y, positions[$0].x - positions[i].x) }
        let candidates = (0..<8).map { -CGFloat.pi / 2 + CGFloat($0) * .pi / 4 }
        var chosen: [CGFloat] = []
        for _ in 0..<molecule.lonePairs[i] {
            var best = candidates[0], bestGap: CGFloat = -1
            for c in candidates where !chosen.contains(c) {
                let gap = taken.map { abs(atan2(sin(c - $0), cos(c - $0))) }.min() ?? .pi
                if gap > bestGap { best = c; bestGap = gap }
            }
            chosen.append(best)
            taken.append(best)
        }
        return chosen
    }
}

/// Build a Lewis structure; graded on the bond graph and electron counts (PRD §18).
struct BuildStepView: View {
    @Bindable var session: LessonSession
    let step: BuildStep

    @State private var molecule: Molecule
    @State private var selected: Int? = 0
    @State private var issues: [String] = []
    @State private var checks = 0
    @State private var passed = false

    init(session: LessonSession, step: BuildStep) {
        self.session = session
        self.step = step
        _molecule = State(initialValue: Molecule(atoms: step.target.atoms))
    }

    var body: some View {
        ScrollView {
            VStack(spacing: 14) {
                MoleculeCanvas(
                    molecule: molecule, positions: step.positions, selected: passed ? nil : selected,
                    interactive: !passed,
                    onTapAtom: { selected = $0 },
                    onTapBond: { molecule.cycleBond($0, $1); issues = [] }
                )
                .clipShape(RoundedRectangle(cornerRadius: 16))
                .overlay(RoundedRectangle(cornerRadius: 16).stroke(Theme.ink.opacity(0.12)))
                .frame(maxWidth: 460)

                if let i = selected, !passed {
                    Stepper(value: Binding(
                        get: { molecule.lonePairs[i] },
                        set: { molecule.lonePairs[i] = $0; issues = [] }
                    ), in: 0...4) {
                        Text("Lone pairs on \(molecule.atomName(i)): **\(molecule.lonePairs[i])**")
                    }
                    .padding(12)
                    .background(RoundedRectangle(cornerRadius: 12).fill(Color(.secondarySystemBackground)))
                }

                if !step.isRecall && !passed {
                    FeedbackRow(kind: .info, text: "Electrons drawn: \(molecule.electronsShown) of \(step.target.valenceElectrons). Each bond uses 2, each lone pair 2.")
                }

                if passed {
                    FeedbackRow(kind: .correct, text: "Correct. Every atom has a full outer shell, and all \(step.target.valenceElectrons) valence electrons are placed.")
                } else {
                    ForEach(issues.prefix(2), id: \.self) { issue in
                        FeedbackRow(kind: .wrong, text: issue)
                    }
                }

                if passed {
                    ContinueButton {
                        session.finalMolecule = MoleculeSnapshot(molecule: molecule, positions: step.positions)
                        session.advance()
                    }
                } else {
                    ContinueButton(title: "Check") { check() }
                }
            }
            .padding(.bottom)
        }
    }

    private func check() {
        let found = ChemistryValidator.issues(in: molecule, target: step.target)
        checks += 1
        if checks == 1 {
            session.recordScience(correct: found.isEmpty, topic: "Lewis structure of \(step.target.name)")
        }
        issues = found
        if found.isEmpty {
            withAnimation { passed = true }
            if step.isRecall { session.recallPassed = true }
        }
    }
}
