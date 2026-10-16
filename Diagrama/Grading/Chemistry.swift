import Foundation

enum Element: String, Decodable {
    case H, C, N, O, F, P, S, Cl

    var name: String {
        switch self {
        case .H: "hydrogen"
        case .C: "carbon"
        case .N: "nitrogen"
        case .O: "oxygen"
        case .F: "fluorine"
        case .P: "phosphorus"
        case .S: "sulfur"
        case .Cl: "chlorine"
        }
    }

    var valenceElectrons: Int {
        switch self {
        case .H: 1
        case .C: 4
        case .N, .P: 5
        case .O, .S: 6
        case .F, .Cl: 7
        }
    }

    /// Electrons needed for a full outer shell: a duet for hydrogen, an octet otherwise.
    var fullShell: Int { self == .H ? 2 : 8 }
}

struct BondKey: Hashable {
    let a: Int
    let b: Int

    init(_ x: Int, _ y: Int) {
        a = min(x, y)
        b = max(x, y)
    }
}

/// A Lewis structure as a graph: atoms, bond orders and lone pairs. Grading works on
/// this graph, never on pixels, so a rotated or moved drawing grades the same (PRD §18).
struct Molecule: Equatable {
    var atoms: [Element]
    var bonds: [BondKey: Int] = [:]
    var lonePairs: [Int]

    init(atoms: [Element]) {
        self.atoms = atoms
        self.lonePairs = Array(repeating: 0, count: atoms.count)
    }

    func bondOrder(_ i: Int, _ j: Int) -> Int { bonds[BondKey(i, j)] ?? 0 }

    func bondOrderSum(_ i: Int) -> Int {
        bonds.filter { $0.key.a == i || $0.key.b == i }.values.reduce(0, +)
    }

    func electronsAround(_ i: Int) -> Int { 2 * bondOrderSum(i) + 2 * lonePairs[i] }

    var electronsShown: Int { 2 * bonds.values.reduce(0, +) + 2 * lonePairs.reduce(0, +) }

    func formalCharge(_ i: Int) -> Int {
        atoms[i].valenceElectrons - 2 * lonePairs[i] - bondOrderSum(i)
    }

    /// "oxygen", or "hydrogen 1" when an element appears more than once.
    func atomName(_ i: Int) -> String {
        let e = atoms[i]
        guard atoms.filter({ $0 == e }).count > 1 else { return e.name }
        let n = atoms[...i].filter { $0 == e }.count
        return "\(e.name) \(n)"
    }

    mutating func cycleBond(_ i: Int, _ j: Int) {
        let next = (bondOrder(i, j) + 1) % 4
        bonds[BondKey(i, j)] = next == 0 ? nil : next
    }
}

struct MoleculeTarget {
    let name: String
    let atoms: [Element]
    let bonds: [BondKey: Int]
    var charge = 0

    var valenceElectrons: Int { atoms.map(\.valenceElectrons).reduce(0, +) - charge }

    /// e.g. "6 from oxygen, 1 from each of the 2 hydrogens"
    var electronBreakdown: String {
        var seen: [Element] = []
        for a in atoms where !seen.contains(a) { seen.append(a) }
        return seen.map { e in
            let n = atoms.filter { $0 == e }.count
            return n == 1 ? "\(e.valenceElectrons) from \(e.name)" : "\(e.valenceElectrons) from each of the \(n) \(e.name)s"
        }.joined(separator: ", ")
    }
}

enum ChemistryValidator {
    /// Returns the scientific problems with a structure, most fundamental first.
    /// An empty list means the structure is correct.
    static func issues(in m: Molecule, target t: MoleculeTarget) -> [String] {
        var issues: [String] = []
        let name = m.atomName

        // Hydrogen forms exactly one single bond and has no lone pairs.
        for i in m.atoms.indices where m.atoms[i] == .H {
            let s = m.bondOrderSum(i)
            if s == 0 {
                issues.append("\(name(i).capitalized) isn't bonded to anything. Every atom in \(t.name) must be connected.")
            } else if s > 1 {
                issues.append("Hydrogen can form only one single bond, but \(name(i)) has \(s) bonds' worth.")
            }
            if m.lonePairs[i] > 0 {
                issues.append("Hydrogen holds only 2 electrons in total, so \(name(i)) can't have a lone pair.")
            }
        }

        // Connectivity: the right atoms bonded to each other.
        for key in t.bonds.keys.sorted(by: { ($0.a, $0.b) < ($1.a, $1.b) }) where m.bondOrder(key.a, key.b) == 0 {
            issues.append("\(name(key.a).capitalized) and \(name(key.b)) should be bonded to each other.")
        }
        for key in m.bonds.keys.sorted(by: { ($0.a, $0.b) < ($1.a, $1.b) }) where t.bonds[key] == nil {
            issues.append("\(name(key.a).capitalized) and \(name(key.b)) are not bonded in \(t.name).")
        }

        // Bond order where the connection itself is right.
        for (key, order) in t.bonds {
            let shown = m.bondOrder(key.a, key.b)
            if shown > 0, shown != order, m.atoms[key.a] != .H, m.atoms[key.b] != .H {
                issues.append("The bond between \(name(key.a)) and \(name(key.b)) should be \(orderName(order)), not \(orderName(shown)).")
            }
        }

        // Total electrons.
        if m.electronsShown != t.valenceElectrons {
            issues.append("\(t.name.capitalized) has \(t.valenceElectrons) valence electrons in total (\(t.electronBreakdown)). Your structure shows \(m.electronsShown).")
        }

        // Full shells for atoms other than hydrogen (hydrogen is covered above).
        for i in m.atoms.indices where m.atoms[i] != .H {
            let around = m.electronsAround(i)
            if around != m.atoms[i].fullShell {
                issues.append("\(name(i).capitalized) should be surrounded by 8 electrons (bonds plus lone pairs). It has \(around).")
            }
        }

        // Formal charges, only once everything else is right.
        if issues.isEmpty {
            for i in m.atoms.indices where m.formalCharge(i) != 0 {
                let fc = m.formalCharge(i)
                issues.append("\(name(i).capitalized) has a formal charge of \(fc > 0 ? "+" : "")\(fc). In neutral \(t.name) every atom should be 0.")
            }
        }
        return issues
    }

    private static func orderName(_ order: Int) -> String {
        switch order {
        case 1: "a single bond"
        case 2: "a double bond"
        case 3: "a triple bond"
        default: "no bond"
        }
    }
}
