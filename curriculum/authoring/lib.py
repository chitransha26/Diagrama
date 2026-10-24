"""Helpers for writing lesson files. Each lesson script builds a dict and calls save()."""
import json
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "Diagrama", "Content", "Lessons")


def r(v):
    return round(v, 1)


def arc_arrow(cx, cy, radius, a0, a1, head=26):
    """A clockwise arc on a circle from angle a0 to a1 (degrees, 0 = right, 90 = down),
    plus an arrowhead at the end. Returns two shapes: the arc and the head."""
    t0, t1 = math.radians(a0), math.radians(a1)
    p0 = (cx + radius * math.cos(t0), cy + radius * math.sin(t0))
    p1 = (cx + radius * math.cos(t1), cy + radius * math.sin(t1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    arc = {"path": f"M {r(p0[0])} {r(p0[1])} A {radius} {radius} 0 {large} 1 {r(p1[0])} {r(p1[1])}"}
    tangent = (-math.sin(t1), math.cos(t1))
    return [arc, head_at(p1, tangent, head)]


def straight_arrow(x1, y1, x2, y2, head=26):
    d = math.hypot(x2 - x1, y2 - y1)
    return [{"line": [x1, y1, x2, y2]}, head_at((x2, y2), ((x2 - x1) / d, (y2 - y1) / d), head)]


def head_at(tip, direction, size=26):
    bx, by = -direction[0], -direction[1]
    pts = []
    for sign in (1, -1):
        a = math.radians(28 * sign)
        dx = bx * math.cos(a) - by * math.sin(a)
        dy = bx * math.sin(a) + by * math.cos(a)
        pts.append((tip[0] + dx * size, tip[1] + dy * size))
    return {"line": [r(pts[0][0]), r(pts[0][1]), r(tip[0]), r(tip[1]), r(pts[1][0]), r(pts[1][1])]}


def mirror_path(d, axis_x):
    """Mirrors an absolute-coordinate SVG path (M/L/C/Q/Z only) across x = axis_x."""
    out, nums = [], []
    tokens = d.replace(",", " ").split()
    is_x = True
    for t in tokens:
        if t.isalpha():
            out.append(t)
            is_x = True
        else:
            v = float(t)
            out.append(str(r(2 * axis_x - v)) if is_x else t)
            is_x = not is_x
    return " ".join(out)


def _points(shape, step=4):
    """Samples a lesson shape (line, polygon, circle, ellipse, rect, or M/L/C/Z path) as points."""
    if "line" in shape or "polygon" in shape:
        v = shape.get("line") or shape.get("polygon")
        pts = list(zip(v[::2], v[1::2]))
        if "polygon" in shape: pts.append(pts[0])
        return _densify(pts, step)
    if "circle" in shape or "ellipse" in shape:
        cx, cy, rx, ry = (shape["circle"] + [shape["circle"][2]]) if "circle" in shape else shape["ellipse"]
        n = max(12, int(2 * math.pi * max(rx, ry) / step))
        return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    if "rect" in shape:
        x, y, w, h = shape["rect"][:4]
        return _densify([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], step)
    tokens = shape["path"].replace(",", " ").split()
    pts, cur, start, i = [], (0, 0), (0, 0), 0
    while i < len(tokens):
        c = tokens[i]; i += 1
        if c == "M": cur = start = (float(tokens[i]), float(tokens[i + 1])); i += 2; pts.append(cur)
        elif c == "L": nxt = (float(tokens[i]), float(tokens[i + 1])); i += 2; pts += _densify([cur, nxt], step)[1:]; cur = nxt
        elif c == "C":
            p1, p2, p3 = [(float(tokens[i + k]), float(tokens[i + k + 1])) for k in (0, 2, 4)]; i += 6
            for t in [j / 40 for j in range(1, 41)]:
                u = 1 - t
                pts.append((u**3 * cur[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                            u**3 * cur[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
            cur = p3
        elif c == "A":  # elliptical arc: sampled on its true curve below
            rx, ry, rot, large, sweep, x, y = (float(t) for t in tokens[i:i + 7]); i += 7
            pts += _arc(cur, (x, y), rx, ry, int(large), int(sweep)); cur = (x, y)
        elif c == "Z": pts += _densify([cur, start], step)[1:]; cur = start
        else: raise ValueError(f"check_spacing can't read path command {c}")
    return pts


def _arc(p0, p1, rx, ry, large, sweep, n=40):
    """Points along an SVG arc with no rotation (the only kind lessons use)."""
    x1, y1 = (p0[0] - p1[0]) / 2, (p0[1] - p1[1]) / 2
    lam = (x1 / rx) ** 2 + (y1 / ry) ** 2
    if lam > 1: rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = max(0, rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1)
    coef = math.sqrt(num / (rx * rx * y1 * y1 + ry * ry * x1 * x1)) * (-1 if large == sweep else 1)
    cxp, cyp = coef * rx * y1 / ry, -coef * ry * x1 / rx
    cx, cy = cxp + (p0[0] + p1[0]) / 2, cyp + (p0[1] + p1[1]) / 2
    t0 = math.atan2((y1 - cyp) / ry, (x1 - cxp) / rx)
    t1 = math.atan2((-y1 - cyp) / ry, (-x1 - cxp) / rx)
    dt = t1 - t0
    if sweep and dt < 0: dt += 2 * math.pi
    if not sweep and dt > 0: dt -= 2 * math.pi
    return [(cx + rx * math.cos(t0 + dt * k / n), cy + ry * math.sin(t0 + dt * k / n)) for k in range(1, n + 1)]


def _densify(pts, step):
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        n = max(1, int(math.dist(a, b) / step))
        out += [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(1, n + 1)]
    return out


def check_spacing(lesson, gap=12, allowed=0.3):
    """Fails if, within one tracing step, a guide runs alongside another closer than `gap` units for
    more than `allowed` of its length. Ink near both counts for only the nearer one, so the other could
    never be finished. Only guides traced in the same step compete, and small parts are zoomed in, so
    the gap shrinks with the part's size. Crossing lines are fine: they're close only for a moment."""
    problems = []
    for s in lesson["structures"]:
        for kind in ("outlines", "details"):
            shapes = [(f"{s['id']}.{kind}[{k}]", _points(shape)) for k, shape in enumerate(s.get(kind, []))]
            for name_a, a in shapes:
                xs, ys = [p[0] for p in a], [p[1] for p in a]
                g = min(gap, 0.1 * max(max(xs) - min(xs), max(ys) - min(ys)))
                for name_b, b in shapes:
                    if name_a == name_b: continue
                    near = sum(1 for p in a if any(math.dist(p, q) < g for q in b)) / len(a)
                    if near > allowed: problems.append(f"{name_a} runs within {g:.0f} of {name_b} for {near:.0%} of its length")
    assert not problems, lesson["id"] + ":\n  " + "\n  ".join(problems)


def save(lesson):
    check_spacing(lesson)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"lesson-{lesson['id']}.json")
    with open(path, "w") as f:
        json.dump(lesson, f, indent=1, ensure_ascii=False)
    print("wrote", os.path.relpath(path))
