"""Grade 5 Earth and space science · Earth's spheres (5-ESS2-1), Earth's water (5-ESS2-2), the sun and
other stars (5-ESS1-1), shadows, day and night and seasonal constellations (5-ESS1-2), and a community
recycling loop (5-ESS3-1).

Facts checked against OpenStax Astronomy 2e, Biology 2e and University Physics Volume 3 (searched with
curriculum/tools/openstax.py), NASA Night Sky Network and the U.S. EPA.
"""
import math

from lib import save, straight_arrow, arc_arrow


def ngss(code, text):
    return {"title": f"NGSS {code}: {text}"}


def astro(section, slug, title):
    return {"title": f"OpenStax Astronomy 2e, {section} {title}", "url": f"https://openstax.org/books/astronomy-2e/pages/{slug}"}


def bio(section, slug, title):
    return {"title": f"OpenStax Biology 2e, {section} {title}", "url": f"https://openstax.org/books/biology-2e/pages/{slug}"}


SKY = astro("2.1", "2-1-the-sky-above", "The Sky Above")
TIME = astro("4.3", "4-3-keeping-time", "Keeping Time")
ESS1_2 = ngss("5-ESS1-2", "Represent data in graphical displays to reveal patterns of daily changes in length and direction of "
                          "shadows, day and night, and the seasonal appearance of some stars in the night sky")


def rays(cx, cy, radius, inner=16, outer=44, step=45):
    return [{"line": [round(cx + (radius + inner) * math.cos(math.radians(a)), 1), round(cy + (radius + inner) * math.sin(math.radians(a)), 1),
                      round(cx + (radius + outer) * math.cos(math.radians(a)), 1), round(cy + (radius + outer) * math.sin(math.radians(a)), 1)]}
            for a in range(0, 360, step)]


def shift(path, dx, dy):
    """Moves an absolute M/L/C/Z path."""
    out, is_x = [], True
    for t in path.split():
        if t.isalpha(): out.append(t); is_x = True
        else: out.append(str(round(float(t) + (dx if is_x else dy), 1))); is_x = not is_x
    return " ".join(out)


CLOUD = ("M 600 260 C 580 220 620 190 660 205 C 680 160 760 160 780 200 C 820 185 860 215 845 250 "
         "C 860 280 820 295 790 285 L 630 285 C 600 290 585 275 600 260 Z")

# ---------------------------------------------------------------- Earth's four spheres
waves = []
for i in range(0, 41):
    x = 560 + i * 10
    waves += [x, round(700 + 8 * math.sin(2 * math.pi * (x - 560) / 100), 1)]
spheres = {
    "id": "g5-earth-spheres", "title": "Earth's four spheres", "grade": "5", "subject": "Earth & space",
    "standard": "5-ESS2-1", "minutes": 8,
    "sources": [ngss("5-ESS2-1", "Develop a model using an example to describe ways the geosphere, biosphere, hydrosphere, and/or "
                                  "atmosphere interact"),
                bio("31.2", "31-2-the-soil", "The Soil (plant roots break up rock)"),
                bio("46.3", "46-3-biogeochemical-cycles", "Biogeochemical Cycles (the water cycle)")],
    "keywords": ["geosphere", "hydrosphere", "atmosphere", "biosphere", "Earth systems", "spheres", "land", "water", "air",
                 "living things", "interactions"],
    "structures": [
        {"id": "geo", "name": "mountain and land", "pen": "bold",
         "outlines": [{"line": [40, 700, 70, 700, 250, 380, 430, 700, 560, 700]}]},
        {"id": "hydro", "name": "ocean", "outlines": [{"line": waves}]},
        {"id": "atmo", "name": "cloud", "outlines": [{"path": shift(CLOUD, -330, -60)}]},
        {"id": "tree", "name": "tree", "outlines": [{"line": [490, 700, 494, 600]}, {"line": [510, 700, 506, 600]}, {"circle": [500, 550, 52]}]},
        {"id": "fish", "name": "fish", "outlines": [{"ellipse": [760, 820, 44, 20]}, {"line": [804, 820, 836, 800, 836, 840, 804, 820]}]},
        {"id": "bird", "name": "bird", "outlines": [{"line": [640, 330, 672, 310, 700, 330, 728, 310, 760, 330]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Land", "structure": "geo", "instruction": "Trace the mountain and the land.",
         "note": {"text": "The geosphere is Earth's rock, soil and sand, from mountains to the deep rock below.",
                  "remember": "Geosphere = rock and soil."}},
        {"type": "trace", "title": "Ocean", "structure": "hydro", "instruction": "Trace the wavy ocean.",
         "note": {"text": "The hydrosphere is all of Earth's water and ice: oceans, rivers, lakes, glaciers, and water underground.",
                  "remember": "Hydrosphere = water and ice."}},
        {"type": "trace", "title": "Cloud", "structure": "atmo", "instruction": "Trace the cloud in the sky.",
         "note": {"text": "The atmosphere is the layer of air around Earth. Clouds, wind and weather happen in it.",
                  "remember": "Atmosphere = air."}},
        {"type": "trace", "title": "Tree", "structure": "tree", "instruction": "Trace the tree.",
         "note": {"text": "The biosphere is every living thing on Earth, including plants, animals and people.",
                  "remember": "Biosphere = living things."}},
        {"type": "trace", "title": "Fish", "structure": "fish", "instruction": "Trace the fish in the ocean.",
         "note": {"text": "Living things are found in every other sphere: on land, in the water, and flying through the air."}},
        {"type": "trace", "title": "Bird", "structure": "bird", "instruction": "Draw the bird flying.",
         "note": {"text": "A bird breathes air, drinks water and nests in a tree: the spheres are linked."}},
        {"type": "label", "title": "Name the spheres", "instruction": "Pick the sphere each numbered part belongs to.",
         "targets": [
             {"n": 1, "at": [250, 560], "answer": "Geosphere", "role": "Rock and soil."},
             {"n": 2, "at": [860, 700], "answer": "Hydrosphere", "role": "Water and ice."},
             {"n": 3, "at": [390, 180], "answer": "Atmosphere", "role": "Air.",
              "mistakes": {"Hydrosphere": "Clouds are made of water droplets, but they float in the air. The sky is the atmosphere."}},
             {"n": 4, "at": [500, 550], "answer": "Biosphere", "role": "Living things."}],
         "vocabulary": ["Geosphere", "Hydrosphere", "Atmosphere", "Biosphere", "Solar system"]},
        {"type": "choice", "title": "Interactions", "instruction": "Two spheres at work.", "showsDiagram": True,
         "question": "A tree's roots grow into cracks in a rock and slowly break it apart. Which two spheres are interacting?",
         "options": [
             {"text": "Biosphere and geosphere", "correct": True,
              "feedback": "Yes. The roots are part of a living thing (biosphere) breaking up rock (geosphere)."},
             {"text": "Atmosphere and hydrosphere", "feedback": "No air or water is involved here: it's living roots and rock."},
             {"text": "Hydrosphere and geosphere", "feedback": "The rock is geosphere, but roots belong to a living thing: the biosphere."},
             {"text": "Only the biosphere", "feedback": "The roots are biosphere, but the rock they break is geosphere."}]},
        {"type": "choice", "title": "Interactions", "instruction": "One more pair.", "showsDiagram": True,
         "question": "The sun warms the ocean, water evaporates, and it forms a cloud. Which two spheres are interacting?",
         "options": [
             {"text": "Hydrosphere and atmosphere", "correct": True,
              "feedback": "Right. Water (hydrosphere) moves into the air (atmosphere) as vapor, then forms clouds."},
             {"text": "Geosphere and biosphere", "feedback": "No rock or living things here. Water is moving into the air."},
             {"text": "Biosphere and atmosphere", "feedback": "The ocean water is hydrosphere, not a living thing."},
             {"text": "Geosphere and hydrosphere", "feedback": "The cloud is up in the air, so the atmosphere is involved."}]},
    ],
}

# ---------------------------------------------------------------- Where Earth's water is
WATER = bio("46.3", "46-3-biogeochemical-cycles", "Biogeochemical Cycles (where Earth's water is stored)")
SCALE = 5  # canvas units per percent
water = {
    "id": "g5-earth-water", "title": "Where Earth's water is", "grade": "5", "subject": "Earth & space",
    "standard": "5-ESS2-2", "minutes": 7, "colorMode": "illustration",
    "sources": [ngss("5-ESS2-2", "Describe and graph the amounts of salt water and fresh water in various reservoirs to provide "
                                  "evidence about the distribution of water on Earth"), WATER],
    "keywords": ["water", "salt water", "fresh water", "ocean", "ice", "glaciers", "groundwater", "lakes", "rivers",
                 "bar graph", "hydrosphere", "reservoirs"],
    "printed": [{"text": "All water", "at": [280, 150], "size": 36}, {"text": "Fresh water", "at": [760, 150], "size": 36},
                {"text": "Salt", "at": [190, 800], "size": 30}, {"text": "Fresh", "at": [350, 800], "size": 30},
                {"text": "Ice and", "at": [670, 796], "size": 26}, {"text": "underground", "at": [670, 826], "size": 26},
                {"text": "Lakes and", "at": [830, 796], "size": 26}, {"text": "rivers", "at": [830, 826], "size": 26},
                {"text": "97.5%", "at": [190, 240], "size": 30}, {"text": "2.5%", "at": [350, 714], "size": 30},
                {"text": "99%", "at": [670, 240], "size": 30}, {"text": "under 1%", "at": [830, 714], "size": 30}],
    "legend": [
        {"name": "Salt water", "color": "#2F6DB5", "meaning": "The ocean and salty seas"},
        {"name": "Fresh water", "color": "#7FC3E8", "meaning": "Water that isn't salty"},
        {"name": "Ice and underground", "color": "#C9E4F2", "meaning": "Fresh water frozen or deep in the ground"},
    ],
    "structures": [
        {"id": "axesA", "name": "left graph's axes", "outlines": [{"line": [100, 200, 100, 760, 460, 760]}]},
        {"id": "salt", "name": "salt water bar", "colorName": "salt water", "fill": "#2F6DB5",
         "outlines": [{"rect": [130, 760 - 97.5 * SCALE, 120, 97.5 * SCALE]}]},
        {"id": "fresh", "name": "fresh water bar", "colorName": "fresh water", "fill": "#7FC3E8",
         "outlines": [{"rect": [290, 760 - 2.5 * SCALE, 120, 2.5 * SCALE]}]},
        {"id": "axesB", "name": "right graph's axes", "outlines": [{"line": [580, 200, 580, 760, 940, 760]}]},
        {"id": "locked", "name": "ice and underground bar", "colorName": "ice and underground", "fill": "#C9E4F2",
         "outlines": [{"rect": [610, 760 - 99 * SCALE, 120, 99 * SCALE]}]},
        {"id": "lakes", "name": "lakes and rivers bar", "outlines": [{"rect": [770, 754, 120, 6]}]},
    ],
    "steps": [
        {"type": "trace", "title": "First graph", "structure": "axesA", "instruction": "Trace the axes of the first graph.",
         "note": {"text": "This bar graph splits all of Earth's water into salt water and fresh water."}},
        {"type": "trace", "title": "Salt water", "structure": "salt", "instruction": "Trace the tall salt water bar.",
         "note": {"text": "97.5% of Earth's water is salt water, mostly in the ocean. We can't drink it.",
                  "remember": "Almost all water is salty."}},
        {"type": "trace", "title": "Fresh water", "structure": "fresh", "instruction": "Trace the tiny fresh water bar.",
         "note": {"text": "Only 2.5% is fresh water. That's about 1 cup out of every 40.", "remember": "Fresh water: 2.5%."}},
        {"type": "trace", "title": "Second graph", "structure": "axesB", "instruction": "Trace the axes of the second graph.",
         "note": {"text": "This graph zooms in on just the fresh water. Where is it?"}},
        {"type": "trace", "title": "Ice and underground", "structure": "locked", "instruction": "Trace the tall bar.",
         "note": {"text": "About 99% of fresh water is frozen in ice or stored underground, where it's hard to reach."}},
        {"type": "trace", "title": "Lakes and rivers", "structure": "lakes", "instruction": "Trace the thin bar for lakes and rivers.",
         "note": {"text": "Less than 1% of fresh water is easy to reach in lakes and rivers. Many living things depend on it.",
                  "remember": "Easy-to-reach fresh water is rare."}},
        {"type": "color", "title": "Color", "structures": ["salt", "fresh", "locked"],
         "instruction": "Color the bars. The lakes and rivers bar is too thin to fill."},
        {"type": "choice", "title": "Read the graph", "instruction": "Use the first graph.", "showsDiagram": True,
         "question": "Where is most of Earth's water?",
         "options": [
             {"text": "In the ocean, as salt water", "correct": True, "feedback": "Yes. 97.5% of all Earth's water is salt water."},
             {"text": "In lakes and rivers", "feedback": "Lakes and rivers hold less than 1% of the fresh water, a tiny part of the total."},
             {"text": "In clouds", "feedback": "Clouds hold very little. Almost all water, 97.5%, is salt water in the ocean."},
             {"text": "Frozen in ice", "feedback": "Ice holds most fresh water, but fresh water is only 2.5% of all water."}]},
        {"type": "choice", "title": "Use the evidence", "instruction": "Think about both graphs.", "showsDiagram": True,
         "question": "Why is it important not to waste fresh water?",
         "options": [
             {"text": "Only a tiny part of Earth's water is fresh and easy to reach", "correct": True,
              "feedback": "Right. Fresh water is 2.5% of the total, and less than 1% of that is in lakes and rivers."},
             {"text": "Fresh water is most of Earth's water", "feedback": "Look at the first graph: fresh water is only 2.5%."},
             {"text": "Salt water is easy to drink", "feedback": "We can't drink salt water, which is why fresh water is so precious."},
             {"text": "All fresh water is in rivers", "feedback": "Most fresh water is locked in ice or underground. Less than 1% is in lakes and rivers."}]},
    ],
}

# ---------------------------------------------------------------- The sun and other stars
stars = {
    "id": "g5-sun-and-stars", "title": "The sun compared with other stars", "grade": "5", "subject": "Earth & space",
    "standard": "5-ESS1-1", "minutes": 7,
    "sources": [ngss("5-ESS1-1", "Support an argument that differences in the apparent brightness of the sun compared to other stars "
                                  "is due to their relative distances from the Earth"),
                astro("1.6", "1-6-a-tour-of-the-universe", "A Tour of the Universe"),
                astro("15", "15-thinking-ahead", "Thinking Ahead (the Sun is a rather ordinary star)"),
                astro("17.1", "17-1-the-brightness-of-stars", "The Brightness of Stars"),
                astro("19.2", "19-2-surveying-the-stars", "Surveying the Stars")],
    "keywords": ["sun", "star", "stars", "brightness", "apparent brightness", "distance", "light-year", "space", "Earth"],
    "printed": [{"text": "Not to scale", "at": [500, 860], "size": 30}],
    "structures": [
        {"id": "earth", "name": "Earth", "outlines": [{"circle": [100, 420, 30]}]},
        {"id": "sun", "name": "sun", "pen": "bold", "outlines": [{"circle": [330, 420, 64]}], "details": rays(330, 420, 64)},
        {"id": "star", "name": "another star", "pen": "bold", "outlines": [{"circle": [860, 420, 64]}], "details": rays(860, 420, 64)},
        {"id": "near", "name": "distance to the sun", "outlines": [{"line": [100, 580, 330, 580]}, {"line": [100, 560, 100, 600]},
                                                                  {"line": [330, 560, 330, 600]}]},
        {"id": "far", "name": "distance to the star", "outlines": [{"line": [100, 720, 860, 720]}, {"line": [100, 700, 100, 740]},
                                                                  {"line": [860, 700, 860, 740]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Earth", "structure": "earth", "instruction": "Trace Earth.",
         "note": {"text": "We look out from Earth at the sun by day and the stars by night."}},
        {"type": "trace", "title": "The sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "The sun is a star, one of hundreds of billions in our galaxy.", "remember": "The sun is a star."}},
        {"type": "trace", "title": "Sunlight", "structure": "sun", "part": "details", "instruction": "Draw the sun's rays.",
         "note": {"text": "Its light reaches us in about 8 minutes."}},
        {"type": "trace", "title": "Another star", "structure": "star", "instruction": "Trace the other star, drawn the same size as the sun.",
         "note": {"text": "The sun is a rather ordinary star: not unusually big or small, hot or cool. Many stars are much like it."}},
        {"type": "trace", "title": "Starlight", "structure": "star", "part": "details", "instruction": "Draw the star's rays.",
         "note": {"text": "Light from even the nearest other star takes over 4 years to reach us."}},
        {"type": "trace", "title": "Near", "structure": "near", "instruction": "Draw the short line from Earth to the sun.",
         "note": {"text": "The sun is close to us, compared with every other star."}},
        {"type": "trace", "title": "Far", "structure": "far", "instruction": "Draw the long line from Earth to the other star.",
         "note": {"text": "In real life, this line would be far too long to fit: the nearest other star is about 270,000 times farther than the sun.",
                  "remember": "Other stars are very far away."}},
        {"type": "choice", "title": "Argue", "instruction": "Use the model.", "showsDiagram": True,
         "question": "Why does the sun look so much bigger and brighter than other stars?",
         "options": [
             {"text": "It's much closer to Earth", "correct": True,
              "feedback": "Yes. Other stars look faint only because they're so very far away."},
             {"text": "It's the biggest star in the universe", "feedback": "The sun is an ordinary star. Many stars are bigger and brighter: they're just farther away."},
             {"text": "Other stars give off no light", "feedback": "Stars all give off light. They look faint because they're so far away."},
             {"text": "Other stars are tiny dots", "feedback": "They only look tiny. Many are as big as the sun or bigger, but far away."}]},
        {"type": "choice", "title": "Test the idea", "instruction": "Try it with flashlights.", "showsDiagram": False,
         "question": "Two identical flashlights shine at you. One is near, one is across a field. What do you see?",
         "options": [
             {"text": "The far one looks dimmer", "correct": True,
              "feedback": "Right. How bright a light looks depends on how far away it is, as well as how much light it gives off."},
             {"text": "They look the same", "feedback": "They give off the same light, but the far one looks dimmer: distance matters."},
             {"text": "The far one looks brighter", "feedback": "Farther lights look dimmer, not brighter."},
             {"text": "You can't see the far one at all", "feedback": "You can see it, just more dimly. That's what happens with distant stars."}]},
    ],
}

# ---------------------------------------------------------------- Shadow length through the day
PROPAGATION = {"title": "OpenStax University Physics Volume 3, 1.1 The Propagation of Light (light travels in straight lines)",
               "url": "https://openstax.org/books/university-physics-volume-3/pages/1-1-the-propagation-of-light"}


def scene(pole_x, sun_x, sun_y):
    """Pole from y 780 to 620, a sun, a ray past the pole's top, and the shadow it casts."""
    dx, dy = pole_x - sun_x, 620 - sun_y
    end = round(pole_x + dx * 160 / dy, 1)
    d = math.hypot(end - sun_x, 780 - sun_y)
    start = (round(sun_x + (end - sun_x) * 40 / d, 1), round(sun_y + (780 - sun_y) * 40 / d, 1))
    lo, hi = sorted((pole_x, end))
    return ({"line": [pole_x, 780, pole_x, 620]}, {"circle": [sun_x, sun_y, 28]},
            straight_arrow(*start, end, 778, head=22), {"polygon": [lo, 786, hi, 786, hi, 798, lo, 798]})


scenes = [scene(130, 50, 560), scene(500, 470, 320), scene(870, 950, 560)]
shadows = {
    "id": "g5-shadow-length", "title": "Shadow length through the day", "grade": "5", "subject": "Earth & space",
    "standard": "5-ESS1-2", "minutes": 8,
    "sources": [ESS1_2, SKY, TIME, PROPAGATION],
    "keywords": ["shadow", "shadows", "sun", "noon", "morning", "afternoon", "light", "east", "west", "daily pattern",
                 "Earth's rotation"],
    "printed": [{"text": "Morning", "at": [170, 220], "size": 34}, {"text": "Noon", "at": [500, 220], "size": 34},
                {"text": "Afternoon", "at": [830, 220], "size": 34},
                {"text": "East", "at": [80, 860], "size": 30}, {"text": "West", "at": [920, 860], "size": 30}],
    "structures": [
        {"id": "ground", "name": "ground", "outlines": [{"line": [40, 780, 960, 780]}]},
        {"id": "poles", "name": "poles", "pen": "bold", "outlines": [s[0] for s in scenes]},
        {"id": "suns", "name": "sun", "outlines": [s[1] for s in scenes]},
        {"id": "rays", "name": "sunlight", "outlines": [shape for s in scenes for shape in s[2]]},
        {"id": "shadows", "name": "shadows", "pen": "bold", "outlines": [s[3] for s in scenes]},
    ],
    "steps": [
        {"type": "trace", "title": "Ground", "structure": "ground", "instruction": "Draw the ground.",
         "note": {"text": "The same pole, seen three times on one sunny day. East is on the left, west on the right."}},
        {"type": "trace", "title": "Poles", "structure": "poles", "instruction": "Trace the pole in each scene.",
         "note": {"text": "The pole never moves or changes. Only the sun's place in the sky changes."}},
        {"type": "trace", "title": "Sun", "structure": "suns", "instruction": "Trace the sun in each scene.",
         "note": {"text": "As Earth turns, the sun seems to rise in the east, climb highest at noon, and sink in the west.",
                  "remember": "Highest sun at noon."}},
        {"type": "trace", "title": "Sunlight", "structure": "rays", "instruction": "Draw each ray of light just past the top of the pole.",
         "note": {"text": "Light travels in straight lines. The pole blocks some of it, leaving a shadow behind."}},
        {"type": "trace", "title": "Shadows", "structure": "shadows", "instruction": "Trace the three shadows on the ground.",
         "note": {"text": "A low sun makes a long shadow; a high sun makes a short one. Shadows point away from the sun.",
                  "remember": "Low sun, long shadow."}},
        {"type": "order", "title": "Shadow pattern",
         "items": ["Long shadow pointing west", "Short shadow at noon", "Long shadow pointing east"],
         "instruction": "Tap the shadows in order, from morning to evening.",
         "why": "In the morning the sun is low in the east, so shadows are long and point west. At noon they're shortest. By evening they're long again, pointing east.",
         "hint": "Where is the sun when the day begins?"},
        {"type": "choice", "title": "Explain", "instruction": "Use the model.", "showsDiagram": True,
         "question": "Why is the shadow shortest at noon?",
         "options": [
             {"text": "The sun is highest in the sky at noon", "correct": True,
              "feedback": "Yes. When the light comes from high overhead, the pole blocks only a little ground behind it."},
             {"text": "The pole shrinks at noon", "feedback": "The pole stays the same. The sun is higher, so the shadow is shorter."},
             {"text": "The sun is closest to Earth at noon", "feedback": "The sun's distance barely changes in a day. It's higher in the sky, so shadows are short."},
             {"text": "There's less light at noon", "feedback": "There's plenty of light. The sun is just high overhead, so the shadow is short."}]},
        {"type": "choice", "title": "Predict", "instruction": "Think about the direction.", "showsDiagram": True,
         "question": "In the afternoon the sun is in the west. Which way does the pole's shadow point?",
         "options": [
             {"text": "East, away from the sun", "correct": True,
              "feedback": "Right. A shadow always points away from the light, so a western sun casts shadows to the east."},
             {"text": "West, toward the sun", "feedback": "Shadows point away from the light. With the sun in the west, they point east."},
             {"text": "Straight up", "feedback": "Shadows fall along the ground, away from the sun: east in the afternoon."},
             {"text": "There's no shadow in the afternoon", "feedback": "There is: a long one pointing east, away from the low western sun."}]},
    ],
}

# ---------------------------------------------------------------- Day and night
ROTATION = astro("6.2", "6-2-telescopes-today", "Telescopes Today (Earth rotates from west to east)")
EX, EY, ER = 620, 500, 230
daynight = {
    "id": "g5-day-and-night", "title": "Earth's rotation: day and night", "grade": "5", "subject": "Earth & space",
    "standard": "5-ESS1-2", "minutes": 7, "colorMode": "illustration",
    "sources": [ESS1_2, SKY, ROTATION],
    "keywords": ["day", "night", "rotation", "Earth", "spin", "axis", "sun", "24 hours", "sunrise", "sunset"],
    "legend": [
        {"name": "Day side", "color": "#F4D35E", "meaning": "Facing the sun"},
        {"name": "Night side", "color": "#2C3E73", "meaning": "Facing away from the sun"},
    ],
    "structures": [
        {"id": "sun", "name": "sun", "pen": "bold", "outlines": [{"circle": [116, 500, 64]}], "details": rays(116, 500, 64, outer=40)},
        {"id": "light", "name": "sunlight", "outlines": straight_arrow(240, 380, 364, 380) + straight_arrow(240, 500, 364, 500)
                                                          + straight_arrow(240, 620, 364, 620)},
        {"id": "day", "name": "day side", "colorName": "day side", "fill": "#F4D35E", "pen": "bold",
         "outlines": [{"path": f"M {EX} {EY - ER} A {ER} {ER} 0 0 0 {EX} {EY + ER} Z"}]},
        {"id": "night", "name": "night side", "colorName": "night side", "fill": "#2C3E73", "pen": "bold",
         "outlines": [{"path": f"M {EX} {EY - ER} A {ER} {ER} 0 0 1 {EX} {EY + ER} Z"}]},
        {"id": "spin", "name": "rotation arrow", "outlines": arc_arrow(EX, EY, ER + 50, 235, 305)},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "The sun lights up Earth, but only one half at a time."}},
        {"type": "trace", "title": "Sun's rays", "structure": "sun", "part": "details", "instruction": "Draw the sun's rays.",
         "note": {"text": "The sun gives off light in every direction. A tiny part of it reaches Earth."}},
        {"type": "trace", "title": "Sunlight", "structure": "light", "instruction": "Draw the three arrows of sunlight.",
         "note": {"text": "Sunlight travels across space and lands on the half of Earth facing the sun."}},
        {"type": "trace", "title": "Day side", "structure": "day", "instruction": "Trace the half of Earth facing the sun, and the line down the middle.",
         "note": {"text": "On the side facing the sun, it's daytime.", "remember": "Facing the sun = day."}},
        {"type": "trace", "title": "Night side", "structure": "night", "instruction": "Trace the other half of Earth, and the middle line again.",
         "note": {"text": "On the side facing away from the sun, it's night.", "remember": "Facing away = night."}},
        {"type": "trace", "title": "Rotation", "structure": "spin", "instruction": "Draw the arrow showing Earth spinning.",
         "note": {"text": "Earth turns on its axis every 24 hours, from west to east. That's why the sun seems to rise and set.",
                  "remember": "One turn = one day."}},
        {"type": "color", "title": "Color", "structures": ["day", "night"], "instruction": "Color the day side and the night side."},
        {"type": "choice", "title": "Explain", "instruction": "Use the model.", "showsDiagram": True,
         "question": "What causes day and night?",
         "options": [
             {"text": "Earth spinning, so each place turns toward the sun and then away", "correct": True,
              "feedback": "Yes. As Earth rotates, your side of Earth turns into sunlight (day) and then out of it (night)."},
             {"text": "The sun moving around Earth every day", "feedback": "It looks that way, but it's Earth that turns. The sun only seems to move."},
             {"text": "The sun switching off at night", "feedback": "The sun always shines. At night, your side of Earth faces away from it."},
             {"text": "Clouds blocking the sun", "feedback": "Clouds don't cause night. Your side of Earth turns away from the sun."}]},
        {"type": "choice", "title": "Predict", "instruction": "Think about the whole Earth.", "showsDiagram": True,
         "question": "It's noon where you live. Is it noon everywhere on Earth?",
         "options": [
             {"text": "No: on the far side of Earth, it's night", "correct": True,
              "feedback": "Right. Only the half facing the sun has daytime. On the other half, it's night."},
             {"text": "Yes, all of Earth has the same time", "feedback": "Look at the model: half of Earth faces away from the sun, so it's night there."},
             {"text": "Yes, because there's only one sun", "feedback": "There's one sun, but it lights only the half of Earth facing it."},
             {"text": "It's day everywhere in summer", "feedback": "Even in summer, the side facing away from the sun has night."}]},
    ],
}

# ---------------------------------------------------------------- Seasonal constellations
NASA_SCORPIUS = {"title": "NASA Night Sky Network: Spy the Scorpion (Scorpius in summer evenings)",
                 "url": "https://science.nasa.gov/solar-system/skywatching/night-sky-network/july2025-night-sky-notes/"}
orion_stars = [(850, 400), (940, 410), (875, 500), (895, 495), (915, 490), (860, 600), (945, 590)]
orion_lines = [[850, 400, 940, 410], [850, 400, 875, 500], [940, 410, 915, 490], [875, 500, 915, 490],
               [875, 500, 860, 600], [915, 490, 945, 590]]
scorpius_stars = [(160, 380), (140, 420), (125, 465), (112, 515), (104, 565), (115, 610), (145, 632), (168, 612)]
constellations = {
    "id": "g5-seasonal-constellations", "title": "Seasonal constellations", "grade": "5", "subject": "Earth & space",
    "standard": "5-ESS1-2", "minutes": 8,
    "sources": [ESS1_2, SKY, NASA_SCORPIUS],
    "keywords": ["constellations", "stars", "Orion", "Scorpius", "seasons", "night sky", "Earth's orbit", "revolution",
                 "year", "pattern"],
    "printed": [{"text": "Winter", "at": [636, 540], "size": 30}, {"text": "Summer", "at": [366, 540], "size": 30},
                {"text": "Not to scale", "at": [500, 880], "size": 28}],
    "structures": [
        {"id": "sun", "name": "sun", "pen": "bold", "outlines": [{"circle": [500, 500, 46]}]},
        {"id": "orbit", "name": "Earth's orbit", "outlines": [{"circle": [500, 500, 220]}]},
        {"id": "earths", "name": "Earth", "outlines": [{"circle": [720, 500, 24]}, {"circle": [280, 500, 24]}]},
        {"id": "views", "name": "night-side view", "pen": "bold", "outlines": straight_arrow(750, 500, 816, 500, head=20)
                                                                         + straight_arrow(250, 500, 184, 500, head=20)},
        {"id": "orion", "name": "Orion", "outlines": [{"circle": [x, y, 8]} for x, y in orion_stars],
         "details": [{"line": l} for l in orion_lines]},
        {"id": "scorpius", "name": "Scorpius", "outlines": [{"circle": [x, y, 8]} for x, y in scorpius_stars],
         "details": [{"line": [c for p in scorpius_stars for c in p]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun in the middle.",
         "note": {"text": "This is a view from far above, looking down on the sun and Earth's path around it."}},
        {"type": "trace", "title": "Orbit", "structure": "orbit", "instruction": "Trace Earth's path around the sun.",
         "note": {"text": "Earth travels once around the sun every year.", "remember": "One trip around the sun = one year."}},
        {"type": "trace", "title": "Earth", "structure": "earths", "instruction": "Trace Earth in winter and in summer.",
         "note": {"text": "Here is Earth at two times of year, half a year apart, as seen from the Northern Hemisphere."}},
        {"type": "trace", "title": "Looking out at night", "structure": "views", "instruction": "Draw the arrows pointing out from Earth's night sides.",
         "note": {"text": "At night we face away from the sun, so we see the stars on the far side of Earth from the sun."}},
        {"type": "trace", "title": "Orion", "structure": "orion", "instruction": "Trace the seven stars of Orion.",
         "note": {"text": "Orion, the hunter, is a winter constellation. In winter, our night side faces toward it.",
                  "remember": "Orion: winter."}},
        {"type": "trace", "title": "Join Orion", "structure": "orion", "part": "details", "instruction": "Connect Orion's stars.",
         "note": {"text": "A constellation is a pattern of stars. The three in a row make Orion's belt."}},
        {"type": "trace", "title": "Scorpius", "structure": "scorpius", "instruction": "Trace the stars of Scorpius.",
         "note": {"text": "Scorpius, the scorpion, shows up on summer evenings, when our night side faces the other way.",
                  "remember": "Scorpius: summer."}},
        {"type": "trace", "title": "Join Scorpius", "structure": "scorpius", "part": "details", "instruction": "Connect the stars of the scorpion's curved body.",
         "note": {"text": "Its bright red star, Antares, is called the heart of the scorpion."}},
        {"type": "choice", "title": "Explain", "instruction": "Use the model.", "showsDiagram": True,
         "question": "Why can't we see Orion on summer nights?",
         "options": [
             {"text": "In summer, Orion is on the sun's side of Earth, so it's up in the daytime", "correct": True,
              "feedback": "Yes. The stars are still there, but the bright sunlight hides them. We'd need to see stars in the daytime."},
             {"text": "Orion moves away in summer", "feedback": "The stars stay put. Earth moves around the sun, changing which way our night side faces."},
             {"text": "Orion stops shining in summer", "feedback": "Stars shine all the time. In summer, Orion is in the daytime sky, hidden by sunlight."},
             {"text": "Clouds cover Orion every summer", "feedback": "It's not clouds. As Earth orbits, Orion ends up on the sun's side of the sky."}]},
        {"type": "choice", "title": "Pattern", "instruction": "Think about next year.", "showsDiagram": True,
         "question": "When will Orion be back in the evening sky?",
         "options": [
             {"text": "Next winter, when Earth returns to the same part of its orbit", "correct": True,
              "feedback": "Right. Earth's trip around the sun repeats every year, so the same constellations return each season."},
             {"text": "Never again", "feedback": "It comes back every winter. Earth's yearly orbit makes the pattern repeat."},
             {"text": "Tomorrow night", "feedback": "In summer, Orion stays hidden by daylight. It returns in the winter."},
             {"text": "Only in 100 years", "feedback": "It's a yearly pattern: Orion returns every winter."}]},
    ],
}

# ---------------------------------------------------------------- A community recycling loop
EPA = {"title": "U.S. EPA: Recycling Basics and Benefits", "url": "https://www.epa.gov/recycle/recycling-basics-and-benefits"}
bottle = "M 230 640 L 270 640 L 270 680 C 300 700 310 720 310 750 L 310 850 L 190 850 L 190 750 C 190 720 200 700 230 680 Z"
recycling = {
    "id": "g5-recycling-loop", "title": "A community recycling loop", "grade": "5", "subject": "Earth & space",
    "standard": "5-ESS3-1", "minutes": 7,
    "sources": [ngss("5-ESS3-1", "Obtain and combine information about ways individual communities use science ideas to protect "
                                  "the Earth's resources and environment"), EPA],
    "keywords": ["recycling", "reduce", "reuse", "natural resources", "community", "landfill", "environment", "waste",
                 "conservation"],
    "structures": [
        {"id": "bin", "name": "recycling bin", "pen": "bold", "outlines": [{"rect": [170, 180, 160, 180, 10]}, {"line": [160, 164, 340, 164]}]},
        {"id": "truck", "name": "collection truck", "outlines": [
            {"rect": [640, 180, 150, 110, 8]}, {"line": [790, 215, 840, 215, 860, 250, 860, 290, 790, 290]},
            {"circle": [680, 300, 18]}, {"circle": [830, 300, 18]}]},
        {"id": "plant", "name": "recycling plant", "outlines": [
            {"polygon": [630, 840, 630, 700, 690, 660, 690, 700, 750, 660, 750, 700, 800, 660, 800, 600, 840, 600, 840, 840]}]},
        {"id": "bottle", "name": "new product", "outlines": [{"path": bottle}]},
        {"id": "loop", "name": "recycling loop", "pen": "bold", "outlines":
            straight_arrow(360, 250, 610, 250) + straight_arrow(750, 340, 750, 630) + straight_arrow(610, 760, 336, 760)
            + straight_arrow(250, 620, 250, 390)},
    ],
    "steps": [
        {"type": "trace", "title": "Recycling bin", "structure": "bin", "instruction": "Trace the recycling bin and its lid.",
         "note": {"text": "The loop starts at home or school: cans, bottles and paper go into the recycling bin, not the trash."}},
        {"type": "trace", "title": "Truck", "structure": "truck", "instruction": "Trace the collection truck and its wheels.",
         "note": {"text": "Trucks collect the recycling. At a facility, it's sorted and cleaned.", "remember": "Step 1: collect and sort."}},
        {"type": "trace", "title": "Recycling plant", "structure": "plant", "instruction": "Trace the recycling plant.",
         "note": {"text": "The sorted materials are made into new products at a recycling plant.", "remember": "Step 2: make new products."}},
        {"type": "trace", "title": "New product", "structure": "bottle", "instruction": "Trace the new bottle.",
         "note": {"text": "People buy products made from recycled material. That closes the loop.", "remember": "Step 3: buy recycled."}},
        {"type": "trace", "title": "The loop", "structure": "loop", "instruction": "Draw the four arrows around the loop.",
         "note": {"text": "Materials go round and round instead of ending up in a landfill."}},
        {"type": "order", "title": "Around the loop",
         "items": ["Put the bottle in the recycling bin", "A truck collects it", "It's sorted and cleaned", "A plant makes a new product",
                   "Someone buys the recycled product"],
         "instruction": "Tap the steps in order.",
         "why": "Recycling is a loop: collect and sort, make new products, then buy them, so the materials get used again.",
         "hint": "Where does the bottle go first?"},
        {"type": "choice", "title": "Why recycle?", "instruction": "Think about Earth's resources.", "showsDiagram": True,
         "question": "How does a community recycling program help protect Earth?",
         "options": [
             {"text": "It saves natural resources and keeps waste out of landfills", "correct": True,
              "feedback": "Yes. Reusing materials means less digging, cutting and drilling for new ones, and less waste to bury or burn."},
             {"text": "It makes more trash", "feedback": "Recycling turns used things into new products, so there's less trash."},
             {"text": "It uses up more trees and metal", "feedback": "It's the opposite: recycled material replaces new trees and metal."},
             {"text": "It doesn't help at all", "feedback": "It does: it conserves resources and energy, and keeps waste out of landfills."}]},
        {"type": "choice", "title": "Even better", "instruction": "Think beyond recycling.", "showsDiagram": False,
         "question": "Which is even better for Earth than recycling a plastic bottle?",
         "options": [
             {"text": "Using a refillable bottle so there's less waste to begin with", "correct": True,
              "feedback": "Right. Reducing and reusing come first. Things should be recycled when they can't be reduced or reused."},
             {"text": "Throwing it in the trash", "feedback": "Trash goes to a landfill. Reusing a bottle is better, and recycling is better than trash."},
             {"text": "Buying two bottles", "feedback": "That makes more waste. Reusing a refillable bottle makes less."},
             {"text": "Burying it in the yard", "feedback": "That's still waste. Reusing a bottle means less waste to begin with."}]},
    ],
}

for lesson in (spheres, water, stars, shadows, daynight, constellations, recycling):
    save(lesson)
