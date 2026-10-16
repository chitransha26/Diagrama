import PencilKit

/// The drawing tool for a part of a diagram. The app picks it automatically for each step,
/// as ArtWorkout does; learners never choose tools.
struct Pen: Equatable {
    enum Kind { case fineLiner, pen, boldPen, pencil }

    let kind: Kind
    /// Line width in diagram units, so lines keep their proportions on every screen size.
    let width: CGFloat

    static let fineLiner = Pen(kind: .fineLiner, width: 5)
    static let pen = Pen(kind: .pen, width: 11)
    static let boldPen = Pen(kind: .boldPen, width: 18)
    static let pencil = Pen(kind: .pencil, width: 12)

    var name: String {
        switch kind {
        case .fineLiner: "Fine liner"
        case .pen: "Pen"
        case .boldPen: "Bold pen"
        case .pencil: "Pencil"
        }
    }

    var symbol: String {
        switch kind {
        case .fineLiner: "pencil.tip"
        case .pen: "pencil"
        case .boldPen: "paintbrush.pointed"
        case .pencil: "pencil.and.scribble"
        }
    }

    func tool(scale: CGFloat) -> PKInkingTool {
        let type: PKInkingTool.InkType = switch kind {
        case .fineLiner: .monoline
        case .pen, .boldPen: .pen
        case .pencil: .pencil
        }
        return PKInkingTool(type, color: UIColor(Theme.ink), width: max(1.5, width * scale))
    }
}
