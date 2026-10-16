import CoreGraphics
import SwiftUI

/// Every diagram is authored in a 1000 × 1000 square ("diagram space") and scaled to the screen.
enum DiagramSpace {
    static let size: CGFloat = 1000
}

/// A shape stored as a dense polyline, so the same points drive both drawing and grading.
struct Polyline: Equatable {
    var points: [CGPoint]
    var closed: Bool

    /// Points including the closing segment back to the start.
    private var vertices: [CGPoint] {
        guard closed, let first = points.first else { return points }
        return points + [first]
    }

    var path: Path {
        var p = Path()
        guard let first = points.first else { return p }
        p.move(to: first)
        for pt in points.dropFirst() { p.addLine(to: pt) }
        if closed { p.closeSubpath() }
        return p
    }

    var length: CGFloat {
        let v = vertices
        guard v.count > 1 else { return 0 }
        return (1..<v.count).reduce(0) { $0 + v[$1 - 1].distance(to: v[$1]) }
    }

    /// The point a given fraction (0...1) of the way along the line.
    func point(at fraction: CGFloat) -> CGPoint {
        let v = vertices
        guard v.count > 1 else { return v.first ?? .zero }
        let target = max(0, min(1, fraction)) * length
        var walked: CGFloat = 0
        for i in 1..<v.count {
            let d = v[i - 1].distance(to: v[i])
            if d > 0, walked + d >= target {
                return v[i - 1].lerp(to: v[i], (target - walked) / d)
            }
            walked += d
        }
        return v[v.count - 1]
    }

    /// Evenly spaced samples along the line.
    func resampled(spacing: CGFloat) -> [CGPoint] {
        let total = length
        guard total > 0, spacing > 0 else { return points }
        let count = max(2, Int(total / spacing))
        return (0..<count).map { point(at: CGFloat($0) / CGFloat(closed ? count : count - 1)) }
    }

    /// Shortest distance from a point to the line.
    func distance(from p: CGPoint) -> CGFloat {
        let v = vertices
        guard v.count > 1 else { return v.first.map { p.distance(to: $0) } ?? .infinity }
        var best = CGFloat.infinity
        for i in 1..<v.count {
            best = min(best, p.distance(toSegment: v[i - 1], v[i]))
        }
        return best
    }

    var bounds: CGRect { CGRect.enclosing(points) }
}

extension CGPoint {
    func distance(to o: CGPoint) -> CGFloat { hypot(x - o.x, y - o.y) }

    func lerp(to o: CGPoint, _ t: CGFloat) -> CGPoint {
        CGPoint(x: x + (o.x - x) * t, y: y + (o.y - y) * t)
    }

    func distance(toSegment a: CGPoint, _ b: CGPoint) -> CGFloat {
        let dx = b.x - a.x, dy = b.y - a.y
        let len2 = dx * dx + dy * dy
        guard len2 > 0 else { return distance(to: a) }
        let t = max(0, min(1, ((x - a.x) * dx + (y - a.y) * dy) / len2))
        return distance(to: CGPoint(x: a.x + t * dx, y: a.y + t * dy))
    }
}

extension CGRect {
    static func enclosing(_ pts: [CGPoint]) -> CGRect {
        guard let f = pts.first else { return .null }
        var minX = f.x, maxX = f.x, minY = f.y, maxY = f.y
        for p in pts {
            minX = min(minX, p.x); maxX = max(maxX, p.x)
            minY = min(minY, p.y); maxY = max(maxY, p.y)
        }
        return CGRect(x: minX, y: minY, width: maxX - minX, height: maxY - minY)
    }
}

/// Builders for the outlines used in lessons. Closed shapes run clockwise on screen.
enum Shapes {
    static func ellipse(_ cx: CGFloat, _ cy: CGFloat, _ rx: CGFloat, _ ry: CGFloat, segments: Int = 72) -> Polyline {
        let pts = (0..<segments).map { i -> CGPoint in
            let a = -CGFloat.pi / 2 + 2 * .pi * CGFloat(i) / CGFloat(segments)
            return CGPoint(x: cx + rx * cos(a), y: cy + ry * sin(a))
        }
        return Polyline(points: pts, closed: true)
    }

    static func circle(_ cx: CGFloat, _ cy: CGFloat, _ r: CGFloat) -> Polyline {
        ellipse(cx, cy, r, r, segments: 36)
    }

    /// Rounded rectangle starting at the top-left of the top edge.
    static func roundedRect(_ x: CGFloat, _ y: CGFloat, _ w: CGFloat, _ h: CGFloat, r: CGFloat, cornerSegments: Int = 8) -> Polyline {
        let r = min(r, w / 2, h / 2)
        let corners: [(CGPoint, CGFloat)] = [
            (CGPoint(x: x + w - r, y: y + r), -.pi / 2),
            (CGPoint(x: x + w - r, y: y + h - r), 0),
            (CGPoint(x: x + r, y: y + h - r), .pi / 2),
            (CGPoint(x: x + r, y: y + r), .pi),
        ]
        var pts: [CGPoint] = [CGPoint(x: x + r, y: y)]
        for (c, start) in corners {
            for i in 0...cornerSegments {
                let a = start + (.pi / 2) * CGFloat(i) / CGFloat(cornerSegments)
                pts.append(CGPoint(x: c.x + r * cos(a), y: c.y + r * sin(a)))
            }
        }
        pts.removeLast() // ends where it started
        return Polyline(points: pts, closed: true)
    }

    static func line(_ pts: CGPoint...) -> Polyline {
        Polyline(points: pts, closed: false)
    }
}
