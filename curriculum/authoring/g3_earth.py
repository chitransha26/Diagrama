"""Grade 3 Earth & space · weather graph (3-ESS2-1), climate zones (3-ESS2-2), hurricane (3-ESS3-1)."""
import math

from lib import head_at, r, save

# ---------------------------------------------------------------- Temperature bar graph
temps = [("Mon", 12), ("Tue", 15), ("Wed", 21), ("Thu", 24), ("Fri", 18)]
xs = [270, 390, 510, 630, 750]
bars = [{"rect": [x - 35, 820 - t * 20, 70, t * 20, 2]} for x, (_, t) in zip(xs, temps)]
graph = {
    "id": "g3-temperature-graph", "title": "Graphing a week of temperatures", "grade": "3", "subject": "Earth & space",
    "standard": "3-ESS2-1", "minutes": 8,
    "sources": [{"title": "NGSS 3-ESS2-1: Represent data in tables and graphs to describe typical weather conditions during a season"}],
    "keywords": ["weather", "temperature", "bar graph", "season", "spring", "data", "graph", "degrees"],
    "printed": [{"text": "  ".join(f"{d} {t}°" for d, t in temps), "at": [530, 90], "size": 38},
                {"text": "°C", "at": [180, 180]}, {"text": "A week in spring", "at": [530, 160], "size": 36}, {"text": "Day", "at": [530, 930]}]
               + [{"text": str(v), "at": [140, 820 - v * 20], "size": 36} for v in (0, 10, 20, 30)]
               + [{"text": d, "at": [x, 860], "size": 38} for x, (d, _) in zip(xs, temps)],
    "structures": [
        {"id": "axes", "name": "axes", "outlines": [{"line": [180, 210, 180, 820, 860, 820]}],
         "details": [{"line": [170, 820 - v * 20, 190, 820 - v * 20]} for v in (10, 20, 30)]},
        {"id": "bars", "name": "bars", "outlines": bars},
    ],
    "steps": [
        {"type": "trace", "title": "Axes", "structure": "axes", "instruction": "Trace the two axes of the graph.",
         "note": {"text": "The side axis shows temperature in degrees Celsius. The bottom axis shows the days of the week.",
                  "remember": "Read across the bottom, up the side."}},
        {"type": "trace", "title": "Scale marks", "structure": "axes", "part": "details", "instruction": "Draw the tick marks at 10, 20 and 30 degrees.",
         "note": {"text": "Evenly spaced marks make a scale, so every degree takes up the same height on the graph."}},
        {"type": "trace", "title": "Bars", "structure": "bars", "instruction": "Draw a bar for each day, as tall as that day's temperature.",
         "note": {"text": "Each bar's height shows the temperature from the table at the top. Comparing bars shows patterns at a glance.",
                  "remember": "Taller bar, warmer day."}},
        {"type": "choice", "title": "Read the graph", "instruction": "Use the bars you drew.", "showsDiagram": True,
         "question": "Which day was the warmest?",
         "options": [
             {"text": "Thursday", "correct": True, "feedback": "Yes. Thursday's bar is the tallest, at 24 degrees."},
             {"text": "Monday", "feedback": "Monday's bar is the shortest, so it was the coolest day."},
             {"text": "Wednesday", "feedback": "Wednesday was warm at 21 degrees, but Thursday's bar is taller."},
             {"text": "Friday", "feedback": "Friday cooled down to 18 degrees. Look for the tallest bar."}]},
        {"type": "choice", "title": "Find the pattern", "instruction": "Look at how the bars change.", "showsDiagram": True,
         "question": "What pattern does this week in spring show?",
         "options": [
             {"text": "It got warmer each day until Thursday, then cooled on Friday", "correct": True,
              "feedback": "Right. Graphs make patterns easy to spot."},
             {"text": "Every day was the same", "feedback": "The bars have different heights, so the temperatures changed."},
             {"text": "It got colder all week", "feedback": "The bars get taller from Monday to Thursday, so it got warmer."},
             {"text": "Friday was the warmest", "feedback": "Friday's bar is shorter than Thursday's."}]},
        {"type": "choice", "title": "Describe a season", "instruction": "Think like a weather scientist.", "showsDiagram": False,
         "question": "You want to describe what spring weather is usually like where you live. What's the best way?",
         "options": [
             {"text": "Graph temperatures from many springs and look for the pattern", "correct": True,
              "feedback": "Yes. One week can be unusual. Data from many years shows what weather to expect in a season."},
             {"text": "Look at one warm day", "feedback": "One day can be unusual. You need lots of data to see what's typical."},
             {"text": "Guess from what you're wearing today", "feedback": "That's one moment. Scientists use measurements over many seasons."},
             {"text": "Check the weather in a different country", "feedback": "Each place has its own climate. Use data from where you live."}]},
    ],
}

# ---------------------------------------------------------------- Climate zones
R, C = 340, 500


def lat_line(lat):
    dy = R * math.sin(math.radians(lat))
    half = math.sqrt(R * R - dy * dy)
    y = r(C - dy)
    return {"line": [r(C - half), y, r(C + half), y]}


climate = {
    "id": "g3-climate-zones", "title": "Climate zones of the world", "grade": "3", "subject": "Earth & space",
    "standard": "3-ESS2-2", "minutes": 8,
    "sources": [{"title": "NGSS 3-ESS2-2: Obtain and combine information to describe climates in different regions of the world"},
                {"title": "Meteoblue Meteoscool: General climate zones", "url": "https://content.meteoblue.com/en/research-education/educational-resources/meteoscool/general-climate-zones/"}],
    "keywords": ["climate", "climate zones", "tropical", "temperate", "polar", "equator", "latitude"],
    "structures": [
        {"id": "globe", "name": "Earth", "pen": "bold", "outlines": [{"circle": [C, C, R]}]},
        {"id": "equator", "name": "equator", "outlines": [lat_line(0)]},
        {"id": "tropics", "name": "tropic lines", "outlines": [lat_line(23.5), lat_line(-23.5)]},
        {"id": "polar", "name": "polar circles", "outlines": [lat_line(66.5), lat_line(-66.5)]},
    ],
    "steps": [
        {"type": "trace", "title": "Earth", "structure": "globe", "instruction": "Trace the outline of the Earth.",
         "note": {"text": "Earth is a sphere, so sunlight hits different places at different angles. That's why climates differ."}},
        {"type": "trace", "title": "Equator", "structure": "equator", "instruction": "Draw the equator across the middle.",
         "note": {"text": "The equator circles Earth halfway between the poles. The sun is almost straight overhead here all year.",
                  "remember": "Equator: the hottest, sunniest belt."}},
        {"type": "trace", "title": "Tropic lines", "structure": "tropics", "instruction": "Draw the two lines on either side of the equator.",
         "note": {"text": "Between these lines is the tropical zone. It's warm all year, and many places have a wet and a dry season."}},
        {"type": "trace", "title": "Polar circles", "structure": "polar", "instruction": "Draw the two short lines near the top and bottom.",
         "note": {"text": "Beyond these lines are the polar zones. Sunlight arrives at a low slant, so it's cold all year.",
                  "remember": "Between tropical and polar lies temperate: four seasons."}},
        {"type": "label", "title": "Label the zones", "instruction": "Pick the climate zone for each numbered spot.",
         "targets": [
             {"n": 1, "at": [500, 500], "answer": "Tropical", "role": "Near the equator: hot all year."},
             {"n": 2, "at": [640, 280], "answer": "Temperate", "role": "Middle latitudes: warm summers, cool winters.",
              "mistakes": {"Tropical": "The tropical zone hugs the equator. This spot is farther north, where seasons change."}},
             {"n": 3, "at": [500, 175], "answer": "Polar", "role": "Near the poles: cold all year."}],
         "vocabulary": ["Tropical", "Temperate", "Polar", "Desert"],
         "commonMistakes": {"Desert": "Deserts are dry places. They're found in several zones, so desert isn't one of these three bands."}},
        {"type": "choice", "title": "Explain", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "Why is it warmer near the equator than near the poles?",
         "options": [
             {"text": "Sunlight hits the equator more directly", "correct": True,
              "feedback": "Yes. Direct rays concentrate energy on a small area. At the poles, slanted rays spread the same energy thin."},
             {"text": "The equator is closer to the sun",
              "feedback": "The difference in distance is tiny. It's the angle of the sunlight that matters."},
             {"text": "There is more land at the equator",
              "feedback": "Climate zones form because of sunlight angle, not how much land there is."},
             {"text": "The poles have no sunlight", "feedback": "The poles get sunlight, but at a low angle, so it's weaker."}]},
    ],
}

# ---------------------------------------------------------------- Hurricane (Northern Hemisphere)
def spiral(theta0_deg):
    pts = []
    for i in range(0, 41):
        rad = 380 - i * 6.5           # inward from 380 to 120
        theta = math.radians(theta0_deg + (rad - 120) * 0.62)  # screen angle shrinks inward: counterclockwise
        pts += [r(C + rad * math.cos(theta)), r(C + rad * math.sin(theta))]
    return pts


arms = [spiral(a) for a in (0, 120, 240)]
arm_heads = []
for pts in arms:
    x1, y1, x2, y2 = pts[-4], pts[-3], pts[-2], pts[-1]
    d = math.hypot(x2 - x1, y2 - y1)
    arm_heads.append(head_at((x2, y2), ((x2 - x1) / d, (y2 - y1) / d), 30))
hurricane = {
    "id": "g3-hurricane", "title": "Structure of a hurricane", "grade": "3", "subject": "Earth & space",
    "standard": "3-ESS3-1", "minutes": 8,
    "sources": [{"title": "NGSS 3-ESS3-1: Make a claim about the merit of a design solution that reduces the impacts of a weather-related hazard"},
                {"title": "Hurricane Science: Hurricane structure", "url": "https://hurricanescience.org/science/science/hurricanestructure/"},
                {"title": "Environment Canada: Hurricane structure and motion", "url": "https://www.canada.ca/en/environment-climate-change/services/archive/hurricanes/structure-and-motion.html"}],
    "keywords": ["hurricane", "storm", "eye", "eyewall", "rain bands", "weather hazard", "tropical cyclone"],
    "structures": [
        {"id": "eye", "name": "eye", "outlines": [{"circle": [C, C, 42]}]},
        {"id": "eyewall", "name": "eyewall", "pen": "bold", "outlines": [{"circle": [C, C, 95]}]},
        {"id": "bands", "name": "rain bands", "outlines": [{"line": a} for a in arms]},
        {"id": "wind", "name": "wind arrows", "pen": "bold", "outlines": arm_heads},
    ],
    "steps": [
        {"type": "trace", "title": "Eye", "structure": "eye", "instruction": "Trace the eye in the center.",
         "note": {"text": "The eye is the calm center of the storm. Skies can be clear and winds light here.",
                  "remember": "Calm in the eye, but the storm isn't over."}},
        {"type": "trace", "title": "Eyewall", "structure": "eyewall", "instruction": "Trace the ring around the eye.",
         "note": {"text": "The eyewall is a ring of towering clouds. It has the strongest winds and heaviest rain of the whole storm."}},
        {"type": "trace", "title": "Rain bands", "structure": "bands", "instruction": "Draw the three curving rain bands.",
         "note": {"text": "Rain bands are long arms of clouds spiraling in toward the center, bringing bursts of heavy rain and gusty wind."}},
        {"type": "trace", "title": "Wind direction", "structure": "wind", "instruction": "Draw an arrowhead at the inner end of each band.",
         "note": {"text": "Air spirals inward counterclockwise in the Northern Hemisphere, because of Earth's spin. South of the equator it's clockwise.",
                  "remember": "North: counterclockwise."}},
        {"type": "choice", "title": "Explain", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "Where are a hurricane's strongest winds?",
         "options": [
             {"text": "In the eyewall", "correct": True, "feedback": "Yes. The ring of clouds around the eye has the fastest winds."},
             {"text": "In the eye", "feedback": "The eye is the calm center. The strongest winds circle right around it."},
             {"text": "At the outer edge", "feedback": "Winds get stronger closer to the center, peaking at the eyewall."},
             {"text": "Everywhere equally", "feedback": "Winds vary a lot. They're strongest at the eyewall."}]},
        {"type": "choice", "title": "Stay safe", "instruction": "Hurricanes are a weather hazard.", "showsDiagram": False,
         "question": "Which idea best reduces harm when a hurricane is coming?",
         "options": [
             {"text": "Use forecasts to leave early and protect windows with shutters", "correct": True,
              "feedback": "Yes. Forecasts give days of warning, and shutters, strong roofs and leaving low areas reduce damage and keep people safe."},
             {"text": "Go outside when the eye passes over", "feedback": "The calm eye is followed by the eyewall's strongest winds. Stay inside."},
             {"text": "Wait until the rain starts to prepare", "feedback": "By then it's dangerous to travel. Prepare early."},
             {"text": "Open windows to let wind through", "feedback": "This doesn't protect a house. Shutters and closed windows are safer."}]},
    ],
}

for lesson in (graph, climate, hurricane):
    save(lesson)
