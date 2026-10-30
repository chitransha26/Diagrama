"""Grade 6 space science · the Earth-sun-moon system: moon phases, seasons and eclipses (MS-ESS1-1), and gravity
in the solar system and the Milky Way (MS-ESS1-2).

Facts checked against OpenStax Astronomy 2e (searched with curriculum/tools/openstax.py): 1.6, 3.3, 4.2, 4.5, 4.7,
7.1, 24.6, 25.1, 25.2 and 25.3.
"""
import math

from lib import save, straight_arrow, head_at, r


def ngss(code, text):
    return {"title": f"NGSS {code}: {text}"}


def astro(section, slug, title):
    return {"title": f"OpenStax Astronomy 2e, {section} {title}", "url": f"https://openstax.org/books/astronomy-2e/pages/{slug}"}


ESS1_1 = ngss("MS-ESS1-1", "Develop and use a model of the Earth-sun-moon system to describe the cyclic patterns of lunar phases, "
                           "eclipses of the sun and moon, and seasons")
ESS1_2 = ngss("MS-ESS1-2", "Develop and use a model to describe the role of gravity in the motions within galaxies and the solar system")
GRAVITY = astro("3.3", "3-3-newtons-universal-law-of-gravitation", "Newton's Universal Law of Gravitation")


def half(cx, cy, radius, side):
    """A closed half-disc split by a vertical line: side 1 is the right half, 0 the left."""
    return {"path": f"M {r(cx)} {r(cy - radius)} A {radius} {radius} 0 0 {side} {r(cx)} {r(cy + radius)} Z"}


def orbit_gap(cx, cy, radius, gaps, gap, arrows=True):
    """An orbit circle broken where planets or moons sit (screen angles in degrees, 0 = right, 90 = down), so the
    line doesn't run through them. Each arc runs counterclockwise on screen, with an arrowhead at its end."""
    shapes, gaps = [], sorted(g % 360 for g in gaps)
    for k, a in enumerate(gaps):
        b = gaps[(k + 1) % len(gaps)] + (360 if k + 1 == len(gaps) else 0)
        # counterclockwise on screen means decreasing screen angle, so run from the next gap back to this one
        start, end = math.radians(b - gap), math.radians(a + gap)
        p0 = (cx + radius * math.cos(start), cy + radius * math.sin(start))
        p1 = (cx + radius * math.cos(end), cy + radius * math.sin(end))
        large = 1 if (b - a - 2 * gap) > 180 else 0
        shapes.append({"path": f"M {r(p0[0])} {r(p0[1])} A {radius} {radius} 0 {large} 0 {r(p1[0])} {r(p1[1])}"})
        if arrows: shapes.append(head_at(p1, (math.sin(end), -math.cos(end)), 22))
    return shapes


def at(cx, cy, radius, angle):
    t = math.radians(angle)
    return r(cx + radius * math.cos(t)), r(cy + radius * math.sin(t))


# ---------------------------------------------------------------- Phases of the moon
PHASES = ["New moon", "Waxing crescent", "First quarter", "Waxing gibbous", "Full moon", "Waning gibbous", "Third quarter",
          "Waning crescent"]
MR, OR = 34, 300  # moon radius, orbit radius
moons = [at(500, 500, OR, -45 * k) for k in range(8)]  # counterclockwise from the sun's side (right)
phases = {
    "id": "g6-moon-phases", "title": "Phases of the moon", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS1-1", "minutes": 10, "colorMode": "illustration",
    "sources": [ESS1_1, astro("4.5", "4-5-phases-and-motions-of-the-moon", "Phases and Motions of the Moon")],
    "keywords": ["moon", "phases", "lunar phases", "new moon", "full moon", "crescent", "gibbous", "first quarter",
                 "third quarter", "waxing", "waning", "orbit", "Earth-sun-moon system"],
    "printed": [{"text": "Sunlight", "at": [930, 90], "size": 30}, {"text": "Not to scale", "at": [140, 940], "size": 28}],
    "legend": [
        {"name": "Sunlit half", "color": "#EDE6D3", "meaning": "The half of the moon facing the sun"},
        {"name": "Dark half", "color": "#3B3F4A", "meaning": "The half facing away from the sun"},
        {"name": "Earth", "color": "#3B7DD8", "meaning": "Our planet, seen from far above the North Pole"},
    ],
    "structures": [
        {"id": "light", "name": "sunlight", "outlines": straight_arrow(990, 150, 900, 150) + straight_arrow(990, 500, 900, 500)
                                                          + straight_arrow(990, 850, 900, 850)},
        {"id": "earth", "name": "Earth", "colorName": "Earth", "fill": "#3B7DD8", "pen": "bold", "outlines": [{"circle": [500, 500, 60]}]},
        {"id": "orbit", "name": "moon's orbit", "outlines": orbit_gap(500, 500, OR, [45 * k for k in range(8)], 9)},
        {"id": "lit", "name": "sunlit halves", "colorName": "sunlit halves", "fill": "#EDE6D3",
         "outlines": [half(x, y, MR, 1) for x, y in moons]},
        {"id": "dark", "name": "dark halves", "colorName": "dark halves", "fill": "#3B3F4A",
         "outlines": [half(x, y, MR, 0) for x, y in moons]},
    ],
    "steps": [
        {"type": "trace", "title": "Sunlight", "structure": "light", "instruction": "Draw the three arrows of sunlight coming from the right.",
         "note": {"text": "The sun is far off to the right. Its light comes from about the same direction all month.",
                  "remember": "Sunlight comes from one side."}},
        {"type": "trace", "title": "Earth", "structure": "earth", "instruction": "Trace Earth in the middle.",
         "note": {"text": "We're looking down from far above Earth's North Pole."}},
        {"type": "trace", "title": "Moon's orbit", "structure": "orbit", "instruction": "Trace the moon's path around Earth, with its arrows.",
         "note": {"text": "The moon orbits Earth counterclockwise, seen from above. Its phases repeat about every 29.5 days.",
                  "remember": "One cycle of phases: about 29.5 days."}},
        {"type": "trace", "title": "Sunlit halves", "structure": "lit", "instruction": "Trace the half of each moon that faces the sun.",
         "note": {"text": "The moon makes no light of its own. It shines by reflected sunlight, and the sun always lights half of it.",
                  "remember": "Half the moon is always lit."}},
        {"type": "trace", "title": "Dark halves", "structure": "dark", "instruction": "Trace the half of each moon facing away from the sun.",
         "note": {"text": "The phase we see depends on how much of the sunlit half faces Earth."}},
        {"type": "color", "title": "Color", "structures": ["lit", "dark", "earth"],
         "instruction": "Color the sunlit halves, the dark halves and Earth."},
        {"type": "label", "title": "Name the phases", "instruction": "Imagine standing on Earth facing each moon. Which phase do you see?",
         "showsDiagram": True,
         "targets": [
             {"n": 1, "at": list(moons[0]), "answer": "New moon", "role": "Between Earth and the sun.",
              "mistakes": {"Full moon": "Its lit half faces the sun, away from us. We see the dark side, so it's a new moon."}},
             {"n": 2, "at": list(moons[2]), "answer": "First quarter", "role": "A quarter of the way around.",
              "mistakes": {"Third quarter": "This is the first quarter: the moon is one quarter of the way around after new moon."}},
             {"n": 3, "at": list(moons[4]), "answer": "Full moon", "role": "Opposite the sun.",
              "mistakes": {"New moon": "Here the lit half faces Earth too, so we see the whole bright face: a full moon."}},
             {"n": 4, "at": list(moons[6]), "answer": "Third quarter", "role": "Three quarters of the way around.",
              "mistakes": {"First quarter": "This is three quarters of the way around after new moon: the third quarter."}}],
         "vocabulary": PHASES},
        {"type": "order", "title": "The cycle", "items": PHASES,
         "instruction": "Tap the phases in order, starting from new moon.",
         "why": "After new moon, we see more of the sunlit half each night (waxing) until full moon, then less (waning).",
         "hint": "Waxing means growing. It comes before full moon."},
        {"type": "choice", "title": "What causes phases?", "instruction": "Use the model.", "showsDiagram": True,
         "question": "What causes the phases of the moon?",
         "options": [
             {"text": "We see different amounts of the moon's sunlit half as it orbits Earth", "correct": True,
              "feedback": "Yes. The sun always lights half the moon. Where the moon is in its orbit decides how much of that half we see."},
             {"text": "Earth's shadow covers part of the moon", "feedback": "A common idea, but no. Earth's shadow only reaches the moon in a lunar eclipse."},
             {"text": "Clouds cover part of the moon", "feedback": "Clouds are in our air, not on the moon. Phases come from the moon's position in its orbit."},
             {"text": "The moon makes less light some nights", "feedback": "The moon makes no light at all. It reflects sunlight, and half of it is always lit."}]},
        {"type": "choice", "title": "Predict", "instruction": "Think about where the full moon is.", "showsDiagram": True,
         "question": "A full moon is opposite the sun in the sky. When does it rise?",
         "options": [
             {"text": "At sunset", "correct": True,
              "feedback": "Right. Opposite the sun, it rises as the sun sets and stays up all night, setting at sunrise."},
             {"text": "At sunrise", "feedback": "That's the new moon, which sits in the same direction as the sun."},
             {"text": "At noon", "feedback": "The first quarter moon rises around noon. The full moon rises at sunset."},
             {"text": "At midnight", "feedback": "The third quarter moon rises around midnight. The full moon rises at sunset."}]},
    ],
}

# ---------------------------------------------------------------- Why we have seasons
TILT = math.radians(23.5)
NORTH = (-math.sin(TILT), -math.cos(TILT))  # the axis tips its north end toward the left, all year
ER = 64


def earth_parts(cx, cy):
    axis = [r(cx - NORTH[0] * 100), r(cy - NORTH[1] * 100), r(cx + NORTH[0] * 100), r(cy + NORTH[1] * 100)]
    eq = (-NORTH[1], NORTH[0])  # perpendicular to the axis
    equator = [r(cx - eq[0] * ER), r(cy - eq[1] * ER), r(cx + eq[0] * ER), r(cy + eq[1] * ER)]
    return {"circle": [cx, cy, ER]}, [{"line": axis}, {"line": equator}]


def ellipse_point(t):
    return r(500 + 380 * math.cos(t)), r(500 - 110 * math.sin(t))


june, june_lines = earth_parts(880, 500)
dec, dec_lines = earth_parts(120, 500)
g = 0.55  # radians of the orbit left out on each side of each Earth
seasons = {
    "id": "g6-seasons", "title": "Why we have seasons", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS1-1", "minutes": 9,
    "sources": [ESS1_1, astro("4.2", "4-2-the-seasons", "The Seasons"), astro("2.1", "2-1-the-sky-above", "The Sky Above (23.5° tilt)")],
    "keywords": ["seasons", "tilt", "axis", "23.5 degrees", "summer", "winter", "solstice", "equinox", "hemisphere",
                 "direct sunlight", "orbit", "Earth-sun-moon system"],
    "printed": [{"text": "N", "at": [r(880 + NORTH[0] * 128), r(500 + NORTH[1] * 128)], "size": 34},
                {"text": "N", "at": [r(120 + NORTH[0] * 128), r(500 + NORTH[1] * 128)], "size": 34},
                {"text": "Not to scale", "at": [500, 900], "size": 28}],
    "structures": [
        {"id": "sun", "name": "sun", "pen": "bold", "outlines": [{"circle": [500, 500, 70]}]},
        {"id": "orbit", "name": "Earth's orbit", "outlines": [
            {"path": f"M {' '.join(map(str, ellipse_point(g)))} A 380 110 0 0 0 {' '.join(map(str, ellipse_point(math.pi - g)))}"},
            {"path": f"M {' '.join(map(str, ellipse_point(math.pi + g)))} A 380 110 0 0 0 {' '.join(map(str, ellipse_point(-g)))}"}]},
        {"id": "june", "name": "Earth in June", "outlines": [june], "details": june_lines},
        {"id": "dec", "name": "Earth in December", "outlines": [dec], "details": dec_lines},
        {"id": "light", "name": "sunlight", "outlines": straight_arrow(590, 500, 796, 500) + straight_arrow(410, 500, 204, 500)},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "Seasons are changes in how much heat we get from the sun through the year."}},
        {"type": "trace", "title": "Orbit", "structure": "orbit", "instruction": "Trace Earth's orbit, seen at a slant from the side.",
         "note": {"text": "Earth's distance from the sun changes by only about 3%. That's too little to cause the seasons.",
                  "remember": "Distance doesn't cause seasons."}},
        {"type": "trace", "title": "Earth in June", "structure": "june", "instruction": "Trace Earth on the right of the sun.",
         "note": {"text": "This is Earth in June. Six months later it's on the far side of its orbit."}},
        {"type": "trace", "title": "Axis and equator", "structure": "june", "part": "details",
         "instruction": "Draw the tilted axis through the poles, then the equator.",
         "note": {"text": "Earth's axis is tilted about 23.5°. In June, the north end leans toward the sun.",
                  "remember": "The tilt causes the seasons."}},
        {"type": "trace", "title": "Earth in December", "structure": "dec", "instruction": "Trace Earth on the left of the sun.",
         "note": {"text": "This is Earth in December, halfway around its orbit."}},
        {"type": "trace", "title": "Same tilt", "structure": "dec", "part": "details",
         "instruction": "Draw the axis and equator, tilted the same way as before.",
         "note": {"text": "The axis keeps pointing the same direction in space all year. Now the north end leans away from the sun."}},
        {"type": "trace", "title": "Sunlight", "structure": "light", "instruction": "Draw the two arrows of sunlight.",
         "note": {"text": "The half leaning toward the sun gets more direct light and longer days, so it heats up more.",
                  "remember": "Direct light + long days = summer."}},
        {"type": "label", "title": "Which season?", "instruction": "Pick the season in the Northern Hemisphere for each Earth.",
         "showsDiagram": True,
         "targets": [
             {"n": 1, "at": [880, 500], "answer": "Summer", "role": "North end leans toward the sun.",
              "mistakes": {"Winter": "The north end leans toward the sun here, so the north gets direct light and long days: summer."}},
             {"n": 2, "at": [120, 500], "answer": "Winter", "role": "North end leans away from the sun.",
              "mistakes": {"Summer": "Here the north leans away, so its sunlight is spread out and days are short: winter."}}],
         "vocabulary": ["Summer", "Winter", "Spring", "Autumn"]},
        {"type": "choice", "title": "Explain", "instruction": "Use the model.", "showsDiagram": True,
         "question": "What causes Earth's seasons?",
         "options": [
             {"text": "The tilt of Earth's axis as Earth orbits the sun", "correct": True,
              "feedback": "Yes. Through the year, each hemisphere takes turns leaning toward the sun, getting more direct light."},
             {"text": "Earth getting closer to the sun in summer", "feedback": "Earth is actually closest to the sun in January, during northern winter."},
             {"text": "The sun getting hotter in summer", "feedback": "The sun's output barely changes. The tilt changes how directly its light hits us."},
             {"text": "Earth's spin speeding up", "feedback": "Earth's spin gives day and night, not seasons. The tilt causes the seasons."}]},
        {"type": "choice", "title": "Other hemisphere", "instruction": "Think about the Southern Hemisphere.", "showsDiagram": True,
         "question": "It's June. What season is it in Australia, in the Southern Hemisphere?",
         "options": [
             {"text": "Winter", "correct": True,
              "feedback": "Right. In June the south end leans away from the sun, so the seasons are opposite."},
             {"text": "Summer, like in the north", "feedback": "If distance caused the seasons, both halves would match. They're opposite, because of the tilt."},
             {"text": "Spring", "feedback": "Spring and autumn come when Earth leans neither toward nor away, in March and September."},
             {"text": "There are no seasons there", "feedback": "The Southern Hemisphere has seasons too, just opposite to the north's."}]},
    ],
}

# ---------------------------------------------------------------- Solar and lunar eclipses
# Top row: the moon's shadow. Its edges are tangent to the sun and the moon, meeting at a tip on Earth's surface.
SY, LY = 250, 700
umbra_tip = 730
solar_umbra = [{"line": [480, SY - 32, umbra_tip, SY]}, {"line": [480, SY + 32, umbra_tip, SY]}]  # two lines: a sharp V's corner overshoots
# Bottom row: Earth's much longer shadow, from tangent lines to the sun and Earth.
slope = 10 / 370
lunar_top = [480, LY - 70, 920, r(LY - 80 + slope * 810)]
lunar_bottom = [480, LY + 70, 920, r(LY + 80 - slope * 810)]
eclipses = {
    "id": "g6-eclipses", "title": "Solar and lunar eclipses", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS1-1", "minutes": 10, "colorMode": "illustration",
    "sources": [ESS1_1, astro("4.7", "4-7-eclipses-of-the-sun-and-moon", "Eclipses of the Sun and Moon")],
    "keywords": ["eclipse", "solar eclipse", "lunar eclipse", "shadow", "umbra", "new moon", "full moon", "sun", "moon",
                 "Earth", "Earth-sun-moon system"],
    "printed": [{"text": "Solar eclipse", "at": [500, 80], "size": 36}, {"text": "Lunar eclipse", "at": [500, 530], "size": 36},
                {"text": "Not to scale", "at": [500, 940], "size": 28}],
    "legend": [
        {"name": "Sun", "color": "#F4C430", "meaning": "The light source"},
        {"name": "Earth", "color": "#3B7DD8", "meaning": "Our planet"},
        {"name": "New moon", "color": "#55595F", "meaning": "Its dark side faces Earth"},
        {"name": "Eclipsed moon", "color": "#B5562E", "meaning": "A full moon in Earth's shadow glows dull coppery red"},
    ],
    "structures": [
        {"id": "sun1", "name": "sun", "colorName": "sun", "fill": "#F4C430", "pen": "bold", "outlines": [{"circle": [110, SY, 80]}]},
        {"id": "moon1", "name": "moon", "colorName": "new moon", "fill": "#55595F", "outlines": [{"circle": [480, SY, 32]}]},
        {"id": "earth1", "name": "Earth", "colorName": "Earth", "fill": "#3B7DD8", "outlines": [{"circle": [800, SY, 70]}]},
        {"id": "shadow1", "name": "moon's shadow", "outlines": solar_umbra},
        {"id": "sun2", "name": "sun", "colorName": "sun", "fill": "#F4C430", "pen": "bold", "outlines": [{"circle": [110, LY, 80]}]},
        {"id": "earth2", "name": "Earth", "colorName": "Earth", "fill": "#3B7DD8", "outlines": [{"circle": [480, LY, 70]}]},
        {"id": "shadow2", "name": "Earth's shadow", "outlines": [{"line": lunar_top}, {"line": lunar_bottom}]},
        {"id": "moon2", "name": "moon", "colorName": "eclipsed moon", "fill": "#B5562E", "outlines": [{"circle": [760, LY, 28]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun1", "instruction": "Trace the sun in the top picture.",
         "note": {"text": "Any solid object in sunlight casts a shadow into space behind it. An eclipse happens when that shadow falls on another body."}},
        {"type": "trace", "title": "Moon", "structure": "moon1", "instruction": "Trace the moon between the sun and Earth.",
         "note": {"text": "The moon is between the sun and Earth, so it's at new moon phase.", "remember": "Solar eclipse: new moon."}},
        {"type": "trace", "title": "Earth", "structure": "earth1", "instruction": "Trace Earth.",
         "note": {"text": "The sun is about 400 times wider than the moon, but also about 400 times farther away, so they look the same size."}},
        {"type": "trace", "title": "Moon's shadow", "structure": "shadow1", "instruction": "Draw the moon's dark shadow narrowing to a point on Earth.",
         "note": {"text": "Where this darkest shadow, the umbra, touches Earth, the moon hides the sun: a total solar eclipse.",
                  "remember": "Umbra = darkest shadow."}},
        {"type": "trace", "title": "Sun", "structure": "sun2", "instruction": "Trace the sun in the bottom picture.",
         "note": {"text": "Now the order changes: sun, then Earth, then moon."}},
        {"type": "trace", "title": "Earth", "structure": "earth2", "instruction": "Trace Earth between the sun and the moon.",
         "note": {"text": "Earth is bigger than the moon, so its shadow is much bigger and longer."}},
        {"type": "trace", "title": "Earth's shadow", "structure": "shadow2", "instruction": "Draw the two edges of Earth's shadow.",
         "note": {"text": "Earth's shadow stretches far out into space, away from the sun."}},
        {"type": "trace", "title": "Moon", "structure": "moon2", "instruction": "Trace the moon inside Earth's shadow.",
         "note": {"text": "The moon is opposite the sun, at full moon, and passes into Earth's shadow: a lunar eclipse.",
                  "remember": "Lunar eclipse: full moon."}},
        {"type": "color", "title": "Color", "structures": ["sun1", "moon1", "earth1", "sun2", "earth2", "moon2"],
         "instruction": "Color both pictures."},
        {"type": "choice", "title": "Lunar eclipse color", "instruction": "Think about the bottom picture.", "showsDiagram": True,
         "question": "Why does the moon glow dull red, not go fully black, in a total lunar eclipse?",
         "options": [
             {"text": "Sunlight bends through Earth's atmosphere into the shadow", "correct": True,
              "feedback": "Yes. A little sunlight passes through our air and is bent into Earth's shadow, lighting the moon a coppery red."},
             {"text": "The moon makes its own red light", "feedback": "The moon makes no light. The red is sunlight bent through Earth's atmosphere."},
             {"text": "Mars lights it up", "feedback": "Mars is far too faint. The glow is sunlight bent through Earth's atmosphere."},
             {"text": "The moon gets hot", "feedback": "It's not heat. Sunlight passing through our atmosphere bends into the shadow."}]},
        {"type": "choice", "title": "Not every month", "instruction": "The moon passes new and full every month.", "showsDiagram": False,
         "question": "Why don't we get a solar and a lunar eclipse every month?",
         "options": [
             {"text": "The moon's orbit is tilted about 5°, so it usually passes above or below the shadows", "correct": True,
              "feedback": "Right. Eclipses happen only when the sun, Earth and moon line up exactly, during eclipse seasons twice a year."},
             {"text": "The moon stops moving some months", "feedback": "The moon always orbits. Its tilted orbit usually carries it above or below the line."},
             {"text": "The sun is too far away", "feedback": "Distance stays about the same. The tilt of the moon's orbit is what matters."},
             {"text": "Eclipses only happen in summer", "feedback": "Eclipses can happen at any time of year, whenever the sun, Earth and moon line up."}]},
        {"type": "choice", "title": "Who sees it?", "instruction": "Compare the two shadows.", "showsDiagram": True,
         "question": "Why do far more people see a total lunar eclipse than a total solar eclipse?",
         "options": [
             {"text": "A lunar eclipse is visible from Earth's whole night side; the moon's umbra covers only a thin path", "correct": True,
              "feedback": "Yes. Anyone who can see the full moon sees it darken, but only people in the umbra's narrow path see the sun fully hidden."},
             {"text": "Lunar eclipses happen in the daytime", "feedback": "Lunar eclipses happen at night, at full moon, for everyone on the night side."},
             {"text": "The sun is bigger than Earth", "feedback": "True, but the reason is shadow size: the moon's umbra only touches a small patch of Earth."},
             {"text": "Solar eclipses are too dim to see", "feedback": "They're dramatic, but visible only in the narrow path where the umbra lands."}]},
    ],
}

# ---------------------------------------------------------------- The solar system
INNER = [("Mercury", 90, 300, 13), ("Venus", 120, 150, 15), ("Earth", 150, 0, 15), ("Mars", 185, 230, 13)]
OUTER = [("Jupiter", 270, 200, 30), ("Saturn", 335, 60, 26), ("Uranus", 395, 290, 19), ("Neptune", 450, 130, 19)]


def planets(group):
    return [{"circle": [*at(500, 500, R, a), pr]} for _, R, a, pr in group]


def orbits(group):
    return [s for _, R, a, pr in group for s in orbit_gap(500, 500, R, [a], math.degrees((pr + 10) / R), arrows=False)]


earth = at(500, 500, 150, 0)
planet_names = [n for n, *_ in INNER + OUTER]
solar = {
    "id": "g6-solar-system", "title": "The solar system", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS1-2", "minutes": 10,
    "sources": [ESS1_2, astro("7.1", "7-1-overview-of-our-planetary-system", "Overview of Our Planetary System"), GRAVITY,
                astro("1.6", "1-6-a-tour-of-the-universe", "A Tour of the Universe")],
    "keywords": ["solar system", "planets", "sun", "orbit", "gravity", "Mercury", "Venus", "Earth", "Mars", "Jupiter",
                 "Saturn", "Uranus", "Neptune", "terrestrial planets", "giant planets"],
    "printed": [{"text": "Not to scale", "at": [140, 960], "size": 28}],
    "structures": [
        {"id": "sun", "name": "sun", "pen": "bold", "outlines": [{"circle": [500, 500, 50]}]},
        {"id": "innerOrbits", "name": "inner planets' orbits", "pen": "fine", "outlines": orbits(INNER)},
        {"id": "inner", "name": "inner planets", "outlines": planets(INNER)},
        {"id": "outerOrbits", "name": "outer planets' orbits", "pen": "fine", "outlines": orbits(OUTER)},
        {"id": "outer", "name": "giant planets", "outlines": planets(OUTER)},
        {"id": "gravity", "name": "pull of gravity", "pen": "bold", "outlines": straight_arrow(earth[0] - 22, 500, 562, 500, head=20)},
        {"id": "motion", "name": "direction of motion", "outlines": straight_arrow(earth[0], 478, earth[0], 418, head=20)},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun in the middle.",
         "note": {"text": "The sun holds 99.8% of all the mass in the solar system.", "remember": "The sun has almost all the mass."}},
        {"type": "trace", "title": "Inner orbits", "structure": "innerOrbits", "instruction": "Trace the four inner orbits.",
         "note": {"text": "All eight planets travel the same way around the sun, in nearly circular orbits in about the same flat plane."}},
        {"type": "trace", "title": "Inner planets", "structure": "inner", "instruction": "Trace the four small planets on those orbits.",
         "note": {"text": "Mercury, Venus, Earth and Mars are the terrestrial planets: small, rocky worlds with solid surfaces.",
                  "remember": "Inner planets: small and rocky."}},
        {"type": "trace", "title": "Outer orbits", "structure": "outerOrbits", "instruction": "Trace the four outer orbits.",
         "note": {"text": "In reality, the outer orbits are far more spread out than any drawing can show."}},
        {"type": "trace", "title": "Giant planets", "structure": "outer", "instruction": "Trace the four big planets.",
         "note": {"text": "Jupiter, Saturn, Uranus and Neptune are giant planets of gas, liquid and ice, with no solid surface.",
                  "remember": "Outer planets: giants."}},
        {"type": "trace", "title": "Gravity", "structure": "gravity", "instruction": "Draw the arrow from Earth toward the sun.",
         "note": {"text": "The sun's gravity pulls on every planet, always toward the sun.", "remember": "Gravity pulls toward the sun."}},
        {"type": "trace", "title": "Motion", "structure": "motion", "instruction": "Draw the arrow showing which way Earth is moving.",
         "note": {"text": "Earth moves sideways. Gravity keeps bending its path from a straight line into an orbit."}},
        {"type": "label", "title": "Name the planets", "instruction": "Pick the name of each numbered planet, counting out from the sun.",
         "showsDiagram": True,
         "targets": [
             {"n": 1, "at": list(at(500, 500, 150, 0)), "answer": "Earth", "role": "Third from the sun.",
              "mistakes": {"Venus": "Venus is second from the sun. Count the orbits: this is the third, Earth."}},
             {"n": 2, "at": list(at(500, 500, 185, 230)), "answer": "Mars", "role": "Fourth from the sun."},
             {"n": 3, "at": list(at(500, 500, 270, 200)), "answer": "Jupiter", "role": "The largest planet.",
              "mistakes": {"Saturn": "Saturn is sixth. This is the fifth planet, the first giant: Jupiter."}},
             {"n": 4, "at": list(at(500, 500, 450, 130)), "answer": "Neptune", "role": "The farthest planet."}],
         "vocabulary": planet_names},
        {"type": "choice", "title": "Gravity's role", "instruction": "Use the arrows.", "showsDiagram": True,
         "question": "If the sun's gravity suddenly switched off, what would Earth do?",
         "options": [
             {"text": "Fly off in a straight line, in the direction it was moving", "correct": True,
              "feedback": "Yes. Without a pull toward the sun to bend its path, Earth would keep going straight."},
             {"text": "Fall into the sun", "feedback": "Falling inward needs a pull toward the sun: that's gravity. Without it, Earth goes straight."},
             {"text": "Stop moving", "feedback": "Nothing would slow it down in space. It would keep moving in a straight line."},
             {"text": "Keep orbiting just the same", "feedback": "Gravity is what bends Earth's path into a circle. Without it, there's no orbit."}]},
        {"type": "choice", "title": "Holding together", "instruction": "Think about the whole system.", "showsDiagram": False,
         "question": "What holds the solar system together?",
         "options": [
             {"text": "Gravity, mostly from the massive sun", "correct": True,
              "feedback": "Right. Every object pulls on every other, and the sun, with 99.8% of the mass, pulls hardest."},
             {"text": "Magnetism", "feedback": "Magnets don't hold planets in orbit. Gravity does."},
             {"text": "Air between the planets", "feedback": "Space between the planets is nearly empty. Gravity holds the system together."},
             {"text": "Nothing: the planets just drift", "feedback": "Without gravity, the planets would fly off in straight lines."}]},
    ],
}

# ---------------------------------------------------------------- The Milky Way and our sun
GX, GY, ARM_B = 500, 400, 0.30  # center, and the spiral arms' tightness


def arm(turn):
    pts = []
    for k in range(0, 61):
        th = k * 0.07
        rad = 80 * math.exp(ARM_B * th)
        if rad > 310: break
        pts += [r(GX + rad * math.cos(th + turn)), r(GY + rad * math.sin(th + turn))]
    return {"line": pts}


SUN_R, SUN_A = 172, 236  # 26,000 of 50,000 light-years out (0.52 of the 330 radius); screen angle
sun_pos = at(GX, GY, SUN_R, SUN_A)
toward = (GX - sun_pos[0], GY - sun_pos[1])
d = math.hypot(*toward)
grav_start = (r(sun_pos[0] + toward[0] / d * 22), r(sun_pos[1] + toward[1] / d * 22))
grav_end = (r(GX - toward[0] / d * 84), r(GY - toward[1] / d * 84))



galaxy = {
    "id": "g6-milky-way", "title": "The Milky Way and our sun", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS1-2", "minutes": 9,
    "sources": [ESS1_2, astro("25.1", "25-1-the-architecture-of-the-galaxy", "The Architecture of the Galaxy"),
                astro("25.2", "25-2-spiral-structure", "Spiral Structure"), astro("25.3", "25-3-the-mass-of-the-galaxy", "The Mass of the Galaxy"),
                astro("24.6", "24-6-evidence-for-black-holes", "Evidence for Black Holes"),
                astro("1.6", "1-6-a-tour-of-the-universe", "A Tour of the Universe")],
    "keywords": ["Milky Way", "galaxy", "spiral arms", "bulge", "disk", "sun", "stars", "gravity", "orbit", "light-year",
                 "black hole", "galactic year"],
    "printed": [{"text": "Seen from above", "at": [160, 60], "size": 30}, {"text": "Seen edge-on", "at": [160, 790], "size": 30},
                {"text": "100,000 light-years", "at": [500, 965], "size": 30}],
    "structures": [
        {"id": "bulge", "name": "central bulge", "pen": "bold", "outlines": [{"circle": [GX, GY, 64]}]},
        {"id": "arms", "name": "spiral arms", "outlines": [arm(0), arm(math.pi)]},
        {"id": "hole", "name": "central black hole", "outlines": [{"circle": [GX, GY, 8]}]},
        {"id": "sun", "name": "the sun", "outlines": [{"circle": [*sun_pos, 11]}]},
        {"id": "path", "name": "the sun's orbit", "pen": "fine", "outlines": orbit_gap(GX, GY, SUN_R, [SUN_A], 7)},
        {"id": "gravity", "name": "pull of gravity", "pen": "bold", "outlines": straight_arrow(*grav_start, *grav_end, head=20)},
        {"id": "edge", "name": "edge-on view", "outlines": [{"ellipse": [500, 860, 330, 22]}],
         "details": [{"ellipse": [500, 860, 64, 44]}]},
        {"id": "width", "name": "width", "outlines": [{"line": [170, 925, 830, 925]}, {"line": [170, 902, 170, 948]}, {"line": [830, 902, 830, 948]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Bulge", "structure": "bulge", "instruction": "Trace the bright bulge in the middle.",
         "note": {"text": "The Milky Way is our galaxy: hundreds of billions of stars, plus gas and dust. Stars crowd together in its central bulge."}},
        {"type": "trace", "title": "Spiral arms", "structure": "arms", "instruction": "Trace the two big spiral arms.",
         "note": {"text": "Seen from above, the disk has spiral arms where gas and dust collect and new stars form."}},
        {"type": "trace", "title": "Black hole", "structure": "hole", "instruction": "Dab a dot for the black hole at the center.",
         "note": {"text": "At the very center is a black hole with about 4 million times the mass of the sun.",
                  "remember": "A giant black hole sits at the center."}},
        {"type": "trace", "title": "The sun", "structure": "sun", "instruction": "Dab a dot for the sun.",
         "note": {"text": "Our sun sits about 26,000 light-years from the center, in a small arm between two big ones.",
                  "remember": "We're about halfway out."}},
        {"type": "trace", "title": "The sun's orbit", "structure": "path", "instruction": "Trace the sun's path around the center, with its arrow.",
         "note": {"text": "The sun, carrying the whole solar system with it, orbits the center once every 225 million years."}},
        {"type": "trace", "title": "Gravity", "structure": "gravity", "instruction": "Draw the arrow from the sun toward the center.",
         "note": {"text": "Gravity from all the mass inside the sun's orbit pulls it toward the center, bending its path into an orbit.",
                  "remember": "Gravity holds the galaxy together."}},
        {"type": "trace", "title": "Edge-on", "structure": "edge", "instruction": "Trace the galaxy as it looks from the side.",
         "note": {"text": "From the side, the disk is very thin, like a CD: about 2,000 light-years thick."}},
        {"type": "trace", "title": "Bulge from the side", "structure": "edge", "part": "details", "instruction": "Trace the bulge bulging out of the disk.",
         "note": {"text": "The bulge is thicker than the disk around it."}},
        {"type": "trace", "title": "Width", "structure": "width", "instruction": "Draw the line across the whole disk.",
         "note": {"text": "The disk is about 100,000 light-years across. Light would take 100,000 years to cross it."}},
        {"type": "choice", "title": "Gravity's role", "instruction": "Use the model.", "showsDiagram": True,
         "question": "What keeps the sun and other stars orbiting the center instead of flying off into space?",
         "options": [
             {"text": "Gravity from the galaxy's mass, pulling toward the center", "correct": True,
              "feedback": "Yes. The same force that holds planets around the sun holds stars in orbit around the galaxy's center."},
             {"text": "The spiral arms push them", "feedback": "The arms don't push stars. Gravity pulling toward the center keeps them in orbit."},
             {"text": "Nothing: stars don't move", "feedback": "Stars do move. The sun orbits the center every 225 million years."},
             {"text": "Wind from the black hole", "feedback": "The black hole is only a small part of the mass. Gravity from all the mass inside the orbit holds stars in."}]},
        {"type": "choice", "title": "Scale", "instruction": "Compare the two systems.", "showsDiagram": False,
         "question": "How is the Milky Way like the solar system?",
         "options": [
             {"text": "In both, gravity pulls objects toward the center and keeps them in orbit", "correct": True,
              "feedback": "Right. Planets orbit the sun and stars orbit the galaxy's center, both held by gravity."},
             {"text": "Both are the same size", "feedback": "The galaxy is unimaginably bigger: hundreds of billions of stars, each maybe with planets."},
             {"text": "Both have one star", "feedback": "The solar system has one star; the galaxy has hundreds of billions."},
             {"text": "Both have a black hole at the center", "feedback": "The solar system has the sun at its center. Gravity is what they share."}]},
    ],
}

for lesson in (phases, seasons, eclipses, solar, galaxy):
    save(lesson)
