import SwiftUI

struct DiagramMarker {
    enum State { case neutral, selected, correct, wrong }
    let number: Int
    let point: CGPoint
    var state: State = .neutral
}

/// Draws a lesson's revealed structures, plus the current guide and feedback, on white paper.
/// The learner's own ink is layered on top separately.
struct DiagramView: View {
    let lesson: Lesson
    /// Structure IDs whose outlines are drawn, plus "id.details" for their inner detail.
    var revealed: Set<String>
    /// Filled outlines as "id#index". Nil fills every revealed part that has a color.
    var filled: Set<String>? = nil
    /// Outlines ("id#index") to tint faintly in their color, showing which pieces to fill.
    var hinted: Set<String> = []
    /// How strongly to draw the template lines. Faint when the learner's ink sits on top.
    var templateOpacity: Double = 0.8
    var guides: [Polyline] = []
    var offGuide: [CGPoint] = []
    /// Parts of the guide not yet traced, marked so the learner can find and finish them.
    var untraced: [CGPoint] = []
    var markers: [DiagramMarker] = []
    /// False draws on a transparent background, for overlays.
    var paper = true

    var body: some View {
        Canvas { ctx, size in
            if paper {
                ctx.fill(Path(CGRect(origin: .zero, size: size)), with: .color(Theme.paper))
            }
            let s = size.width / DiagramSpace.size
            ctx.scaleBy(x: s, y: s)

            let visible = lesson.structures.filter { revealed.contains($0.id) }
            // Fills first, then every line on top, so a fill can never hide a line drawn earlier.
            for st in visible {
                guard let color = st.fill else { continue }
                for (i, o) in st.outlines.enumerated() where o.closed {
                    let key = "\(st.id)#\(i)"
                    if filled?.contains(key) ?? true {
                        ctx.fill(o.path, with: .color(color))
                    } else if hinted.contains(key) {
                        ctx.fill(o.path, with: .color(color.opacity(0.25)))
                    }
                }
            }
            for st in visible {
                for o in st.outlines {
                    ctx.stroke(o.path, with: .color(Theme.ink.opacity(templateOpacity)), lineWidth: 2 / s)
                }
                if revealed.contains(TracePart.details.key(st.id)) {
                    for d in st.details {
                        ctx.stroke(d.path, with: .color(Theme.ink.opacity(templateOpacity * 0.6)), lineWidth: 1.4 / s)
                    }
                }
            }

            // Printed words belong to the page, so overlays (paper: false) don't repeat them.
            for t in lesson.printed where paper {
                ctx.draw(Text(t.text).font(.system(size: t.size, weight: .medium)).foregroundStyle(Theme.ink), at: t.at)
            }

            for g in guides {
                ctx.stroke(g.path, with: .color(Theme.guide),
                           style: StrokeStyle(lineWidth: 3 / s, lineCap: .round, dash: [9 / s, 7 / s]))
            }

            // Off-guide ink is marked with hollow rings, so it reads without relying on color.
            for (i, p) in offGuide.enumerated() where i % 4 == 0 {
                let r = 7 / s
                ctx.stroke(Path(ellipseIn: CGRect(x: p.x - r, y: p.y - r, width: 2 * r, height: 2 * r)),
                           with: .color(Theme.coral), lineWidth: 2 / s)
            }

            for p in untraced {
                let r = 4 / s
                ctx.fill(Path(ellipseIn: CGRect(x: p.x - r, y: p.y - r, width: 2 * r, height: 2 * r)), with: .color(Theme.cyan))
            }

            for m in markers {
                drawMarker(m, in: &ctx, scale: s)
            }
        }
        .accessibilityElement()
        .accessibilityLabel(accessibilityText)
    }

    private func drawMarker(_ m: DiagramMarker, in ctx: inout GraphicsContext, scale s: CGFloat) {
        let r = 13 / s
        let rect = CGRect(x: m.point.x - r, y: m.point.y - r, width: 2 * r, height: 2 * r)
        let circle = Path(ellipseIn: rect)
        switch m.state {
        case .neutral:
            ctx.fill(circle, with: .color(.white))
            ctx.stroke(circle, with: .color(Theme.indigo), lineWidth: 2.5 / s)
        case .selected:
            ctx.fill(circle, with: .color(Theme.indigo))
        case .correct:
            ctx.fill(circle, with: .color(Theme.ink))
        case .wrong:
            ctx.fill(circle, with: .color(.white))
            ctx.stroke(circle, with: .color(Theme.coral), style: StrokeStyle(lineWidth: 3 / s, dash: [4 / s, 3 / s]))
        }
        let textColor: Color = (m.state == .selected || m.state == .correct) ? .white : Theme.ink
        ctx.draw(Text("\(m.number)").font(.system(size: 14 / s, weight: .bold)).foregroundStyle(textColor), at: m.point)
    }

    private var accessibilityText: String {
        let names = lesson.structures.filter { revealed.contains($0.id) }.map(\.name)
        return names.isEmpty ? "Blank drawing area" : "Diagram showing " + names.joined(separator: ", ")
    }
}

/// Shows where to start and plays a demo stroke along the guide (PRD §01: "view a demonstrated step").
struct GuideDemo: View {
    let guide: Polyline
    var progress: CGFloat

    var body: some View {
        ZStack {
            GuideShape(polyline: guide)
                .trim(from: 0, to: progress)
                .stroke(Theme.cyan.opacity(0.7), style: StrokeStyle(lineWidth: 5, lineCap: .round))
            PenTip(polyline: guide, progress: progress)
                .fill(Theme.cyan)
        }
        .allowsHitTesting(false)
        .accessibilityHidden(true)
    }
}

private struct GuideShape: Shape {
    let polyline: Polyline

    func path(in rect: CGRect) -> Path {
        let s = rect.width / DiagramSpace.size
        return polyline.path.applying(CGAffineTransform(scaleX: s, y: s))
    }
}

private struct PenTip: Shape {
    let polyline: Polyline
    var progress: CGFloat

    var animatableData: CGFloat {
        get { progress }
        set { progress = newValue }
    }

    func path(in rect: CGRect) -> Path {
        let s = rect.width / DiagramSpace.size
        let p = polyline.point(at: progress)
        return Path(ellipseIn: CGRect(x: p.x * s - 9, y: p.y * s - 9, width: 18, height: 18))
    }
}

/// The learner's finished layers, stacked over the diagram. When zoomed, only the visible
/// part is re-rendered from the vector ink, so earlier lines stay sharp.
struct InkLayers: View {
    let session: LessonSession
    var viewport: Viewport = .whole

    var body: some View {
        GeometryReader { geo in
            let unit = geo.size.width / DiagramSpace.size
            let visible = CGRect(origin: viewport.origin,
                                 size: CGSize(width: DiagramSpace.size / viewport.zoom, height: DiagramSpace.size / viewport.zoom))
            ZStack(alignment: .topLeading) {
                ForEach(session.layers.indices, id: \.self) { i in
                    if viewport.zoom == 1 {
                        Image(uiImage: session.layers[i].image).resizable()
                    } else {
                        Image(uiImage: session.layerImage(i, crop: visible, pointsWide: visible.width * unit))
                            .resizable()
                            .frame(width: visible.width * unit, height: visible.height * unit)
                            .offset(x: visible.minX * unit, y: visible.minY * unit)
                    }
                }
            }
            .frame(width: geo.size.width, height: geo.size.height, alignment: .topLeading)
        }
        .allowsHitTesting(false)
        .accessibilityHidden(true)
    }
}

/// A session's diagram as the learner drew it: template, fills, and their ink.
struct LearnerDiagram: View {
    let session: LessonSession
    var markers: [DiagramMarker] = []
    var hinted: Set<String> = []

    var body: some View {
        ZStack {
            DiagramView(lesson: session.lesson, revealed: session.revealed, filled: session.filled,
                        hinted: hinted, templateOpacity: session.layers.isEmpty ? 0.8 : 0.25)
            InkLayers(session: session)
            if !markers.isEmpty {
                // Markers go above the learner's ink so they're never hidden.
                DiagramView(lesson: session.lesson, revealed: [], markers: markers, paper: false)
                    .allowsHitTesting(false)
            }
        }
    }
}

/// Which part of the diagram square a step shows. Small parts are zoomed in, as ArtWorkout does.
struct Viewport {
    let zoom: CGFloat
    let origin: CGPoint

    static let whole = Viewport(zoom: 1, origin: .zero)
    static let maxZoom: CGFloat = 4

    init(zoom: CGFloat, origin: CGPoint) {
        self.zoom = zoom
        self.origin = origin
    }

    init(focus: CGRect?) {
        guard let f = focus else { self = .whole; return }
        self.init(center: CGPoint(x: f.midX, y: f.midY), zoom: min(Viewport.maxZoom, DiagramSpace.size / max(f.width, f.height, 1)))
    }

    init(center: CGPoint, zoom: CGFloat) {
        let visible = DiagramSpace.size / zoom
        let clamp = { (v: CGFloat) in max(0, min(DiagramSpace.size - visible, v)) }
        self.init(zoom: zoom, origin: CGPoint(x: clamp(center.x - visible / 2), y: clamp(center.y - visible / 2)))
    }
}

/// Lays out full-diagram content at the viewport's zoom, cropped to a square of `side`.
struct ZoomedStage<Content: View>: View {
    let viewport: Viewport
    let side: CGFloat
    @ViewBuilder var content: (_ fullSide: CGFloat) -> Content

    var body: some View {
        let full = side * viewport.zoom
        let unit = full / DiagramSpace.size
        content(full)
            .frame(width: full, height: full)
            .offset(x: -viewport.origin.x * unit, y: -viewport.origin.y * unit)
            // The zoomed picture is bigger than its box. It's display-only, so its cropped-off
            // part must never catch taps meant for the toolbar and buttons around the box.
            .allowsHitTesting(false)
            .frame(width: side, height: side, alignment: .topLeading)
            .clipped()
    }
}

/// A square area for drawing, sized to fit the space it's given.
struct SquareStage<Content: View>: View {
    @ViewBuilder var content: (CGFloat) -> Content

    var body: some View {
        GeometryReader { geo in
            let side = min(geo.size.width, geo.size.height)
            content(side)
                .frame(width: side, height: side)
                .clipShape(RoundedRectangle(cornerRadius: 16))
                .overlay(RoundedRectangle(cornerRadius: 16).stroke(Theme.ink.opacity(0.12)))
                .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
    }
}

/// A name tag pinned beside the part being drawn, where the learner's eyes already are.
/// Sits above the part, or below it when there's more room there, and stays inside the
/// visible area when the view is zoomed.
struct PartNameTag: View {
    let name: String
    /// The part's bounds, in diagram space.
    let target: CGRect
    let viewport: Viewport

    private let height: CGFloat = 36

    var body: some View {
        GeometryReader { geo in
            let unit = geo.size.width / DiagramSpace.size
            let side = DiagramSpace.size / viewport.zoom
            let visible = CGRect(x: viewport.origin.x * unit, y: viewport.origin.y * unit, width: side * unit, height: side * unit)
            let box = CGRect(x: target.minX * unit, y: target.minY * unit, width: target.width * unit, height: target.height * unit)
            let roomAbove = box.minY - visible.minY
            let above = roomAbove >= height + 14 || roomAbove >= visible.maxY - box.maxY
            let halfWidth = CGFloat(name.count) * 4.5 + 16
            let x = min(max(box.midX, visible.minX + halfWidth + 6), visible.maxX - halfWidth - 6)
            // Leave a gap so the tag never covers the blue start dot on the guide.
            let gap: CGFloat = 12
            let y = above
                ? max(box.minY - height / 2 - gap, visible.minY + height / 2 + 2)
                : min(box.maxY + height / 2 + gap, visible.maxY - height / 2 - 2)
            tag(pointingDown: above)
                .position(x: x, y: y)
        }
        .allowsHitTesting(false)
        .accessibilityElement()
        .accessibilityLabel("You're drawing \(name)")
    }

    private func tag(pointingDown: Bool) -> some View {
        VStack(spacing: 0) {
            if !pointingDown { pointer.rotationEffect(.degrees(180)) }
            Text(name)
                .font(.subheadline.bold())
                .foregroundStyle(.white)
                .lineLimit(1)
                .padding(.horizontal, 12)
                .padding(.vertical, 5)
                .background(Capsule().fill(Theme.indigo))
            if pointingDown { pointer }
        }
        .shadow(color: .black.opacity(0.15), radius: 3, y: 1)
    }

    private var pointer: some View {
        PointerTriangle().fill(Theme.indigo).frame(width: 12, height: 6)
    }
}

private struct PointerTriangle: Shape {
    func path(in rect: CGRect) -> Path {
        var p = Path()
        p.move(to: CGPoint(x: rect.minX, y: rect.minY))
        p.addLine(to: CGPoint(x: rect.maxX, y: rect.minY))
        p.addLine(to: CGPoint(x: rect.midX, y: rect.maxY))
        p.closeSubpath()
        return p
    }
}
