import CoreGraphics
import Foundation

/// Turns SVG path data ("M 10 10 L 90 10 C …") into the polylines lessons trace, so lesson
/// art can come from any vector source. Supports M L H V C S Q T A Z, absolute and relative.
/// Each subpath becomes its own polyline.
enum SVGPath {
    struct ParseError: Error, CustomStringConvertible {
        let description: String
    }

    static func polylines(_ d: String, spacing: CGFloat = 6) throws -> [Polyline] {
        var tokens = Tokenizer(d)
        var result: [Polyline] = []
        var points: [CGPoint] = []
        var current = CGPoint.zero, start = CGPoint.zero
        var lastControl: CGPoint?
        var command: Character = "M"

        func flush(closed: Bool) {
            if points.count > 1 {
                var pts = points
                if closed, let f = pts.first, let l = pts.last, f.distance(to: l) < 0.5 { pts.removeLast() }
                result.append(Polyline(points: pts, closed: closed))
            }
            points = []
        }

        func add(_ p: CGPoint) {
            if let l = points.last, l.distance(to: p) < 0.01 { return }
            points.append(p)
        }

        func curve(_ steps: Int, _ f: (CGFloat) -> CGPoint) {
            for i in 1...max(steps, 1) { add(f(CGFloat(i) / CGFloat(max(steps, 1)))) }
        }

        while let next = tokens.peek() {
            if case .command(let c) = next {
                tokens.next()
                command = c
                if c == "Z" || c == "z" {
                    flush(closed: true)
                    current = start
                    lastControl = nil
                    continue
                }
            }
            let rel = command.isLowercase
            let base = rel ? current : .zero
            func pt() throws -> CGPoint {
                let x = try tokens.number(), y = try tokens.number()
                return CGPoint(x: base.x + x, y: base.y + y)
            }
            switch command.uppercased().first! {
            case "M":
                flush(closed: false)
                current = try pt(); start = current
                add(current)
                command = rel ? "l" : "L"   // further pairs are line-tos
                lastControl = nil
            case "L":
                current = try pt(); add(current); lastControl = nil
            case "H":
                let x = try tokens.number(); current = CGPoint(x: rel ? current.x + x : x, y: current.y); add(current); lastControl = nil
            case "V":
                let y = try tokens.number(); current = CGPoint(x: current.x, y: rel ? current.y + y : y); add(current); lastControl = nil
            case "C", "S":
                let c1: CGPoint
                if command.uppercased() == "C" { c1 = try pt() } else {
                    c1 = lastControl.map { CGPoint(x: 2 * current.x - $0.x, y: 2 * current.y - $0.y) } ?? current
                }
                let c2 = try pt(), end = try pt(), p0 = current
                let length: CGFloat = p0.distance(to: c1) + c1.distance(to: c2) + c2.distance(to: end)
                curve(Int(length / spacing) + 2) { t in cubic(p0, c1, c2, end, t) }
                current = end; lastControl = c2
            case "Q", "T":
                let c: CGPoint
                if command.uppercased() == "Q" { c = try pt() } else {
                    c = lastControl.map { CGPoint(x: 2 * current.x - $0.x, y: 2 * current.y - $0.y) } ?? current
                }
                let end = try pt(), p0 = current
                let length: CGFloat = p0.distance(to: c) + c.distance(to: end)
                curve(Int(length / spacing) + 2) { t in quadratic(p0, c, end, t) }
                current = end; lastControl = c
            case "A":
                let rx = abs(try tokens.number()), ry = abs(try tokens.number())
                let rotation = try tokens.number() * .pi / 180
                let large = try tokens.number() != 0, sweep = try tokens.number() != 0
                let end = try pt()
                arc(from: current, to: end, rx: rx, ry: ry, phi: rotation, large: large, sweep: sweep, spacing: spacing).forEach(add)
                current = end; lastControl = nil
            default:
                throw ParseError(description: "Unsupported path command \(command)")
            }
        }
        flush(closed: false)
        return result
    }

    private static func cubic(_ p0: CGPoint, _ c1: CGPoint, _ c2: CGPoint, _ p3: CGPoint, _ t: CGFloat) -> CGPoint {
        let u: CGFloat = 1 - t
        let a: CGFloat = u * u * u, b: CGFloat = 3 * u * u * t, c: CGFloat = 3 * u * t * t, d: CGFloat = t * t * t
        let x: CGFloat = a * p0.x + b * c1.x + c * c2.x + d * p3.x
        let y: CGFloat = a * p0.y + b * c1.y + c * c2.y + d * p3.y
        return CGPoint(x: x, y: y)
    }

    private static func quadratic(_ p0: CGPoint, _ c: CGPoint, _ p2: CGPoint, _ t: CGFloat) -> CGPoint {
        let u: CGFloat = 1 - t
        let a: CGFloat = u * u, b: CGFloat = 2 * u * t, d: CGFloat = t * t
        return CGPoint(x: a * p0.x + b * c.x + d * p2.x, y: a * p0.y + b * c.y + d * p2.y)
    }

    /// Samples an SVG elliptical arc (endpoint parameterization, per the SVG spec).
    private static func arc(from p1: CGPoint, to p2: CGPoint, rx: CGFloat, ry: CGFloat, phi: CGFloat,
                            large: Bool, sweep: Bool, spacing: CGFloat) -> [CGPoint] {
        guard rx > 0, ry > 0, p1 != p2 else { return [p2] }
        var rx = rx, ry = ry
        let cosP = cos(phi), sinP = sin(phi)
        let dx = (p1.x - p2.x) / 2, dy = (p1.y - p2.y) / 2
        let x1 = cosP * dx + sinP * dy, y1 = -sinP * dx + cosP * dy
        let lambda = (x1 * x1) / (rx * rx) + (y1 * y1) / (ry * ry)
        if lambda > 1 { rx *= sqrt(lambda); ry *= sqrt(lambda) }
        let num = rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1
        let den = rx * rx * y1 * y1 + ry * ry * x1 * x1
        var coef = sqrt(max(0, num / den))
        if large == sweep { coef = -coef }
        let cx1 = coef * rx * y1 / ry, cy1 = -coef * ry * x1 / rx
        let cx = cosP * cx1 - sinP * cy1 + (p1.x + p2.x) / 2
        let cy = sinP * cx1 + cosP * cy1 + (p1.y + p2.y) / 2
        func angle(_ ux: CGFloat, _ uy: CGFloat, _ vx: CGFloat, _ vy: CGFloat) -> CGFloat {
            let a = atan2(ux * vy - uy * vx, ux * vx + uy * vy)
            return a
        }
        let t1 = angle(1, 0, (x1 - cx1) / rx, (y1 - cy1) / ry)
        var dt = angle((x1 - cx1) / rx, (y1 - cy1) / ry, (-x1 - cx1) / rx, (-y1 - cy1) / ry)
        if !sweep && dt > 0 { dt -= 2 * .pi } else if sweep && dt < 0 { dt += 2 * .pi }
        let steps = max(2, Int(abs(dt) * max(rx, ry) / spacing))
        return (1...steps).map { i in
            let t = t1 + dt * CGFloat(i) / CGFloat(steps)
            let x = rx * cos(t), y = ry * sin(t)
            return CGPoint(x: cx + cosP * x - sinP * y, y: cy + sinP * x + cosP * y)
        }
    }

    private enum Token { case command(Character), number(CGFloat) }

    private struct Tokenizer {
        private let chars: [Character]
        private var i = 0
        private var lookahead: Token?

        init(_ s: String) { chars = Array(s) }

        mutating func peek() -> Token? {
            if lookahead == nil { lookahead = read() }
            return lookahead
        }

        @discardableResult mutating func next() -> Token? {
            let t = peek(); lookahead = nil; return t
        }

        mutating func number() throws -> CGFloat {
            guard case .number(let n) = next() else { throw ParseError(description: "Expected a number in path data") }
            return n
        }

        private mutating func read() -> Token? {
            while i < chars.count, chars[i] == " " || chars[i] == "," || chars[i].isNewline || chars[i] == "\t" { i += 1 }
            guard i < chars.count else { return nil }
            let c = chars[i]
            if c.isLetter && c != "e" && c != "E" { i += 1; return .command(c) }
            var s = ""
            if c == "-" || c == "+" { s.append(c); i += 1 }
            var seenDot = false, seenExp = false
            while i < chars.count {
                let d = chars[i]
                if d.isNumber { s.append(d) }
                else if d == "." && !seenDot && !seenExp { seenDot = true; s.append(d) }
                else if (d == "e" || d == "E") && !seenExp { seenExp = true; s.append(d)
                    if i + 1 < chars.count, chars[i + 1] == "-" || chars[i + 1] == "+" { i += 1; s.append(chars[i]) } }
                else { break }
                i += 1
            }
            return .number(CGFloat(Double(s) ?? 0))
        }
    }
}
