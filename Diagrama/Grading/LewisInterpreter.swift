import CoreGraphics

/// Reads a freehand Lewis structure, drawn around printed atom symbols, as a bond graph.
/// Lines whose ends sit at two atoms are bonds (two lines make a double bond); short dabs
/// near an atom are electrons, paired into lone pairs. The graph is then graded by
/// `ChemistryValidator`, so where exactly things are drawn never matters (PRD §18).
enum LewisInterpreter {
    /// A stroke shorter than this (in diagram units) is a dot.
    static let dotSize: CGFloat = 32
    /// How close a line's end or a dot must be to an atom's centre to belong to it.
    static let atomReach: CGFloat = 150

    struct Reading {
        var molecule: Molecule
        /// Problems with the drawing itself, before any chemistry is checked.
        var notes: [String]
    }

    static func read(strokes: [[CGPoint]], atoms: [Element], positions: [CGPoint]) -> Reading {
        var molecule = Molecule(atoms: atoms)
        var dots = Array(repeating: 0, count: atoms.count)
        var notes: [String] = []
        var strayLines = 0, strayDots = 0

        func nearestAtom(_ p: CGPoint) -> Int? {
            let best = positions.indices.min { p.distance(to: positions[$0]) < p.distance(to: positions[$1]) }
            guard let i = best, p.distance(to: positions[i]) <= atomReach else { return nil }
            return i
        }

        for stroke in strokes where !stroke.isEmpty {
            let box = CGRect.enclosing(stroke)
            if max(box.width, box.height) < dotSize {
                if let i = nearestAtom(CGPoint(x: box.midX, y: box.midY)) { dots[i] += 1 } else { strayDots += 1 }
                continue
            }
            guard let first = stroke.first, let last = stroke.last,
                  let a = nearestAtom(first), let b = nearestAtom(last), a != b else {
                strayLines += 1
                continue
            }
            molecule.bonds[BondKey(a, b), default: 0] += 1
        }

        for key in molecule.bonds.keys where molecule.bonds[key]! > 3 {
            molecule.bonds[key] = 3
        }
        for i in atoms.indices {
            molecule.lonePairs[i] = dots[i] / 2
            if dots[i] % 2 == 1 {
                notes.append("There's an odd number of dots around \(molecule.atomName(i)). Electrons in a lone pair come in twos.")
            }
        }
        if strayLines > 0 {
            notes.append(strayLines == 1
                ? "One line doesn't run from one atom to another. Start and end each bond at an atom."
                : "\(strayLines) lines don't run from one atom to another. Start and end each bond at an atom.")
        }
        if strayDots > 0 {
            notes.append("Some dots aren't next to any atom. Put lone pairs right beside the atom they belong to.")
        }
        return Reading(molecule: molecule, notes: notes)
    }
}
