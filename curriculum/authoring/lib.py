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


def save(lesson):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"lesson-{lesson['id']}.json")
    with open(path, "w") as f:
        json.dump(lesson, f, indent=1, ensure_ascii=False)
    print("wrote", os.path.relpath(path))
