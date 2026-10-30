"""Grade 6 Earth systems and human activity · the water cycle in detail (MS-ESS2-4), a cold front (MS-ESS2-5), global
wind belts (MS-ESS2-6), an aquifer (MS-ESS3-1), inside a volcano (MS-ESS3-2) and the greenhouse effect (MS-ESS3-5).

Facts checked against Steven Earle's Physical Geology, 2nd edition (BCcampus, CC BY 4.0): 4.3, 4.5, 13.1, 14.1, 14.2,
14.3, 19.1 and 19.2; and NOAA JetStream and the NOAA National Ocean Service for weather and winds.
"""
import math

from lib import save, straight_arrow, head_at, r


def ngss(code, text):
    return {"title": f"NGSS {code}: {text}"}


def geo(section, slug, title):
    return {"title": f"Earle, Physical Geology 2nd ed. (BCcampus), {section} {title}",
            "url": f"https://opentextbc.ca/physicalgeology2ed/chapter/{slug}/"}


def shift(path, dx, dy):
    """Moves an absolute M/L/C/Z path."""
    out, is_x = [], True
    for t in path.split():
        if t.isalpha(): out.append(t); is_x = True
        else: out.append(str(round(float(t) + (dx if is_x else dy), 1))); is_x = not is_x
    return " ".join(out)


CLOUD = ("M 600 260 C 580 220 620 190 660 205 C 680 160 760 160 780 200 C 820 185 860 215 845 250 "
         "C 860 280 820 295 790 285 L 630 285 C 600 290 585 275 600 260 Z")
HYDRO = geo("13.1", "13-1-the-hydrological-cycle", "The Hydrological Cycle")

# ---------------------------------------------------------------- The water cycle in detail
waves = []
for i in range(0, 32):
    x = 650 + i * 10
    waves += [x, round(760 + 7 * math.sin(2 * math.pi * (x - 650) / 80), 1)]
runoff = [{"line": [363, 555, 433, 741, 628, 758]}, head_at((628, 758), (0.996, 0.087), 22)]  # 35 units off the slope
water = {
    "id": "g6-water-cycle-detail", "title": "The water cycle in detail", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS2-4", "minutes": 11,
    "sources": [ngss("MS-ESS2-4", "Develop a model to describe the cycling of water through Earth's systems driven by energy from the "
                                   "sun and the force of gravity"), HYDRO,
                geo("14.2", "14-2-groundwater-flow", "Groundwater Flow")],
    "keywords": ["water cycle", "hydrologic cycle", "evaporation", "transpiration", "condensation", "precipitation", "runoff",
                 "infiltration", "groundwater", "states of water", "sun", "gravity"],
    "structures": [
        {"id": "sun", "name": "sun", "pen": "bold", "outlines": [{"circle": [890, 110, 50]}]},
        {"id": "land", "name": "land and mountain", "pen": "bold", "outlines": [{"line": [40, 780, 110, 780, 260, 380, 410, 780, 640, 780]},
                                                                             {"line": [640, 780, 700, 880, 960, 900]}]},
        {"id": "ocean", "name": "ocean", "outlines": [{"line": waves}]},
        {"id": "snow", "name": "snow cap", "outlines": [{"polygon": [215, 500, 260, 380, 305, 500, 283, 484, 260, 506, 237, 484]}]},
        {"id": "tree", "name": "tree", "outlines": [{"line": [512, 780, 514, 692]}, {"line": [528, 780, 526, 692]}, {"circle": [520, 650, 42]}]},
        {"id": "evap", "name": "evaporation", "outlines": straight_arrow(820, 730, 700, 270)},
        {"id": "transp", "name": "transpiration", "outlines": straight_arrow(535, 600, 560, 255)},
        {"id": "cloud", "name": "cloud", "outlines": [{"path": shift(CLOUD, -170, -60)}]},
        {"id": "precip", "name": "precipitation", "outlines": straight_arrow(440, 245, 330, 400)},
        {"id": "runoff", "name": "runoff", "outlines": runoff},
        {"id": "ground", "name": "groundwater flow", "pen": "fine", "outlines": straight_arrow(200, 840, 640, 890)},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "Energy from the sun drives the water cycle up into the sky.", "remember": "The sun lifts water up."}},
        {"type": "trace", "title": "Land", "structure": "land", "instruction": "Trace the land, the mountain and the sea floor.",
         "note": {"text": "Gravity pulls water back down: as rain and snow, then downhill over and under the land.",
                  "remember": "Gravity brings water down."}},
        {"type": "trace", "title": "Ocean", "structure": "ocean", "instruction": "Trace the ocean's surface.",
         "note": {"text": "The ocean holds 97% of Earth's water."}},
        {"type": "trace", "title": "Snow", "structure": "snow", "instruction": "Trace the snow on the mountain top.",
         "note": {"text": "Some water is stored as snow and ice. When it melts in spring, solid water becomes liquid and flows downhill."}},
        {"type": "trace", "title": "Tree", "structure": "tree", "instruction": "Trace the tree.",
         "note": {"text": "Plants pull water up from the soil through their roots."}},
        {"type": "trace", "title": "Evaporation", "structure": "evap", "instruction": "Draw the arrow rising from the ocean.",
         "note": {"text": "Sunlight warms the ocean, and liquid water evaporates into invisible water vapor, a gas.",
                  "remember": "Evaporation: liquid to gas."}},
        {"type": "trace", "title": "Transpiration", "structure": "transp", "instruction": "Draw the arrow rising from the tree.",
         "note": {"text": "Plants give off water vapor from their leaves. This is called transpiration."}},
        {"type": "trace", "title": "Cloud", "structure": "cloud", "instruction": "Trace the cloud.",
         "note": {"text": "Winds carry the vapor up, where it cools and condenses into tiny droplets or ice crystals: a cloud.",
                  "remember": "Condensation: gas to liquid."}},
        {"type": "trace", "title": "Precipitation", "structure": "precip", "instruction": "Draw the arrow from the cloud down to the mountain.",
         "note": {"text": "When the droplets or crystals grow heavy, gravity pulls them down as rain or snow."}},
        {"type": "trace", "title": "Runoff", "structure": "runoff", "instruction": "Draw the arrow down the mountain and across to the ocean.",
         "note": {"text": "Water flows downhill in streams and rivers, back to the ocean."}},
        {"type": "trace", "title": "Groundwater", "structure": "ground", "instruction": "Draw the arrow through the ground to the ocean.",
         "note": {"text": "Some water soaks into the ground and moves slowly through rock and soil. Some of it reaches the ocean."}},
        {"type": "label", "title": "Name the processes", "instruction": "Pick the name of each numbered process.",
         "targets": [
             {"n": 1, "at": [760, 500], "answer": "Evaporation", "role": "Water rises from the ocean as vapor."},
             {"n": 2, "at": [548, 430], "answer": "Transpiration", "role": "Plants give off water vapor.",
              "mistakes": {"Evaporation": "This vapor comes from a plant's leaves, which is called transpiration."}},
             {"n": 3, "at": [380, 110], "answer": "Condensation", "role": "Vapor cools into droplets."},
             {"n": 4, "at": [385, 322], "answer": "Precipitation", "role": "Rain or snow falls."},
             {"n": 5, "at": [500, 750], "answer": "Runoff", "role": "Water flows over the land."}],
         "vocabulary": ["Evaporation", "Transpiration", "Condensation", "Precipitation", "Runoff", "Melting"]},
        {"type": "choice", "title": "What drives it?", "instruction": "Use the model.", "showsDiagram": True,
         "question": "Which force brings water back down from the clouds and over the land to the sea?",
         "options": [
             {"text": "Gravity", "correct": True, "feedback": "Yes. The sun's energy lifts water up; gravity pulls it back down and downhill."},
             {"text": "Sunlight", "feedback": "Sunlight drives evaporation, lifting water up. Gravity pulls it back down."},
             {"text": "Wind alone", "feedback": "Wind moves clouds sideways, but gravity makes rain fall and rivers flow downhill."},
             {"text": "Magnetism", "feedback": "Magnetism doesn't move water. Gravity does."}]},
        {"type": "choice", "title": "Changes of state", "instruction": "Follow one water molecule.", "showsDiagram": True,
         "question": "Ocean water evaporates, forms a cloud, and falls as snow on the mountain. What states was it in, in order?",
         "options": [
             {"text": "Liquid, gas, liquid droplets or ice, then solid snow", "correct": True,
              "feedback": "Right. It evaporated into a gas, condensed into droplets or crystals, and fell as solid snow."},
             {"text": "Solid, liquid, gas", "feedback": "Ocean water starts as a liquid. It becomes a gas when it evaporates."},
             {"text": "It stayed liquid the whole time", "feedback": "Evaporation turns it into a gas, and snow is a solid."},
             {"text": "Gas, solid, gas", "feedback": "Ocean water is liquid first, then gas, then droplets or ice, then snow."}]},
    ],
}

# ---------------------------------------------------------------- A cold front
AIR = {"title": "NOAA JetStream: Air Masses (fronts)", "url": "https://www.noaa.gov/jetstream/synoptic/air-masses"}
MAPS = {"title": "NOAA JetStream: How to read Surface Weather Maps", "url": "https://www.noaa.gov/jetstream/wxmaps"}
storm = ("M 440 330 C 405 325 405 270 445 262 C 430 235 445 210 470 205 L 380 140 L 400 112 L 700 112 L 720 140 "
         "L 595 205 C 625 212 640 240 628 262 C 668 270 668 325 628 330 Z")
front = {
    "id": "g6-cold-front", "title": "A cold front", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS2-5", "minutes": 9,
    "sources": [ngss("MS-ESS2-5", "Collect data to provide evidence for how the motions and complex interactions of air masses result "
                                   "in changes in weather conditions"), AIR, MAPS],
    "keywords": ["cold front", "air mass", "weather", "front", "thunderstorm", "temperature", "density", "warm air",
                 "cold air", "weather map"],
    "printed": [{"text": "Ground", "at": [860, 840], "size": 26}],
    "structures": [
        {"id": "ground", "name": "ground", "outlines": [{"line": [60, 800, 940, 800]}]},
        {"id": "boundary", "name": "front", "pen": "bold", "outlines": [{"path": "M 560 800 C 470 780 380 600 300 350"}]},
        {"id": "cold", "name": "cold air moving in", "outlines": straight_arrow(110, 700, 380, 700)},
        {"id": "warm", "name": "warm air rising", "outlines": straight_arrow(760, 760, 560, 400)},
        {"id": "cloud", "name": "thunderstorm cloud", "outlines": [{"path": storm}],
         "details": [{"line": [470, 355, 458, 400]}, {"line": [520, 355, 508, 400]}, {"line": [570, 355, 558, 400]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Ground", "structure": "ground", "instruction": "Trace the ground.",
         "note": {"text": "This is a slice through the air, seen from the side. An air mass is a huge body of air with the same temperature and humidity."}},
        {"type": "trace", "title": "The front", "structure": "boundary", "instruction": "Trace the steep curved boundary.",
         "note": {"text": "A front is where two air masses meet. At a cold front, cold air is pushing in and replacing warm air.",
                  "remember": "Cold front: cold air replaces warm."}},
        {"type": "trace", "title": "Cold air", "structure": "cold", "instruction": "Draw the arrow of cold air moving in from the left.",
         "note": {"text": "Cold air is denser than warm air, so it stays low and wedges under the warm air like a snowplow."}},
        {"type": "trace", "title": "Warm air", "structure": "warm", "instruction": "Draw the arrow of warm air forced up over the front.",
         "note": {"text": "The steep cold front forces the warm air up quickly. Rising air cools, and its water vapor condenses.",
                  "remember": "Rising warm air makes clouds."}},
        {"type": "trace", "title": "Storm cloud", "structure": "cloud", "instruction": "Trace the tall storm cloud.",
         "note": {"text": "The fast-rising air builds tall clouds along a narrow band: showers and thunderstorms."}},
        {"type": "trace", "title": "Rain", "structure": "cloud", "part": "details", "instruction": "Draw the rain falling.",
         "note": {"text": "On weather maps, a cold front is drawn as a blue line with triangles pointing the way it's moving."}},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [200, 620], "answer": "Cold air mass", "role": "Dense air pushing in.",
              "mistakes": {"Warm air mass": "This air is behind the front, wedging in low: it's the cold air mass."}},
             {"n": 2, "at": [820, 560], "answer": "Warm air mass", "role": "Air being pushed up."},
             {"n": 3, "at": [455, 700], "answer": "Cold front", "role": "Where the air masses meet."}],
         "vocabulary": ["Cold air mass", "Warm air mass", "Cold front", "Warm front"]},
        {"type": "choice", "title": "Read the data", "instruction": "A weather station records this.", "showsDiagram": False,
         "question": "At 3 pm it's 75 °F with south winds. A line of storms passes. At 9 pm it's 45 °F, skies are clear, and winds blow from the northwest. What happened?",
         "options": [
             {"text": "A cold front passed, and a cold air mass replaced the warm one", "correct": True,
              "feedback": "Yes. Storms, then falling temperatures, clearing skies and a wind shift are signs of a cold front passing."},
             {"text": "A warm front passed", "feedback": "A warm front brings warmer air. Here the temperature dropped 30 degrees."},
             {"text": "Nothing changed but the time of day", "feedback": "Evening cools things a little, but a 30-degree drop with a wind shift means a new air mass arrived."},
             {"text": "The air masses stopped moving", "feedback": "A stationary front wouldn't bring such a quick, big change."}]},
        {"type": "choice", "title": "Why storms?", "instruction": "Use the model.", "showsDiagram": True,
         "question": "Why do cold fronts often bring thunderstorms?",
         "options": [
             {"text": "Dense cold air forces warm, moist air up quickly, and it cools to form tall clouds", "correct": True,
              "feedback": "Right. The steep front lifts the warm air fast, so tall storm clouds build in a narrow band."},
             {"text": "Cold air holds more rain", "feedback": "The storms come from warm, moist air being forced up, not from the cold air itself."},
             {"text": "Warm air sinks under the cold air", "feedback": "It's the reverse: warm air is less dense and gets pushed up."},
             {"text": "The ground gets hotter", "feedback": "The key is air masses colliding: cold air lifting warm air."}]},
    ],
}

# ---------------------------------------------------------------- Global wind belts
GR = 380


def lat_y(deg): return r(500 - GR * math.sin(math.radians(deg)))


def chord(deg):
    half = GR * math.cos(math.radians(deg))
    return {"line": [r(500 - half), lat_y(deg), r(500 + half), lat_y(deg)]}


def arrows(pairs):
    return [s for p in pairs for s in straight_arrow(*p, head=20)]


wind_sources = [ngss("MS-ESS2-6", "Develop and use a model to describe how unequal heating and rotation of the Earth cause patterns of "
                                   "atmospheric and oceanic circulation that determine regional climates"),
                {"title": "NOAA JetStream: Global Atmospheric Circulations",
                 "url": "https://www.noaa.gov/jetstream/global/global-atmospheric-circulations"},
                {"title": "NOAA National Ocean Service: Surface Ocean Currents (trade winds and westerlies)",
                 "url": "https://oceanservice.noaa.gov/education/tutorial_currents/04currents2.html"}]
winds = {
    "id": "g6-wind-belts", "title": "Global wind belts", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS2-6", "minutes": 9,
    "sources": wind_sources,
    "keywords": ["wind belts", "trade winds", "westerlies", "polar easterlies", "Coriolis effect", "global circulation",
                 "equator", "latitude", "climate", "deserts", "high pressure", "low pressure"],
    "printed": [{"text": "0°", "at": [935, 500], "size": 26}, {"text": "30°N", "at": [930, lat_y(30)], "size": 26},
                {"text": "60°N", "at": [800, lat_y(60) - 20], "size": 26}, {"text": "30°S", "at": [930, lat_y(-30)], "size": 26},
                {"text": "60°S", "at": [800, lat_y(-60) + 20], "size": 26}],
    "structures": [
        {"id": "globe", "name": "Earth", "pen": "bold", "outlines": [{"circle": [500, 500, GR]}],
         "details": [chord(0), chord(30), chord(-30), chord(60), chord(-60)]},
        {"id": "trades", "name": "trade winds", "outlines": arrows([(440, 375, 320, 435), (700, 375, 580, 435),
                                                                  (440, 625, 320, 565), (700, 625, 580, 565)])},
        {"id": "westerlies", "name": "westerlies", "outlines": arrows([(320, 260, 440, 220), (560, 260, 680, 220),
                                                                      (320, 740, 440, 780), (560, 740, 680, 780)])},
        {"id": "polar", "name": "polar easterlies", "outlines": straight_arrow(536, 147, 464, 157, head=16) + straight_arrow(536, 853, 464, 843, head=16)},
    ],
    "steps": [
        {"type": "trace", "title": "Earth", "structure": "globe", "instruction": "Trace Earth.",
         "note": {"text": "The sun heats Earth unevenly: most strongly near the equator, least at the poles."}},
        {"type": "trace", "title": "Latitude lines", "structure": "globe", "part": "details", "instruction": "Draw the equator and the lines at 30° and 60°.",
         "note": {"text": "Hot air rises at the equator, sinks near 30°, and rises again near 60°. This makes three loops of air in each half of Earth."}},
        {"type": "trace", "title": "Trade winds", "structure": "trades", "instruction": "Draw the four arrows between the equator and 30°.",
         "note": {"text": "Air sinking near 30° flows back toward the equator. Earth's spin bends it, so these trade winds blow from the east.",
                  "remember": "Trade winds: 0° to 30°, from the east."}},
        {"type": "trace", "title": "Westerlies", "structure": "westerlies", "instruction": "Draw the four arrows between 30° and 60°.",
         "note": {"text": "Between about 35° and 60°, the westerlies blow from west to east. Air rising near 60° brings rainy, stormy weather.",
                  "remember": "Westerlies: 30° to 60°, from the west."}},
        {"type": "trace", "title": "Polar easterlies", "structure": "polar", "instruction": "Draw the arrows near the poles.",
         "note": {"text": "Cold air sinks at the poles and spreads out as the polar easterlies, blowing from the east."}},
        {"type": "label", "title": "Name the winds", "instruction": "Pick the name of each numbered wind belt.",
         "targets": [
             {"n": 1, "at": [380, 405], "answer": "Trade winds", "role": "Between the equator and 30°.",
              "mistakes": {"Westerlies": "These blow from the east, toward the equator. They're the trade winds."}},
             {"n": 2, "at": [380, 240], "answer": "Westerlies", "role": "Between 30° and 60°.",
              "mistakes": {"Trade winds": "These blow from the west, between 30° and 60°: the westerlies."}},
             {"n": 3, "at": [500, 150], "answer": "Polar easterlies", "role": "Near the poles."}],
         "vocabulary": ["Trade winds", "Westerlies", "Polar easterlies", "Jet stream"]},
        {"type": "choice", "title": "Climate", "instruction": "Air sinks near 30°.", "showsDiagram": True,
         "question": "Many of the world's deserts lie near 30° north and south. Why?",
         "options": [
             {"text": "Sinking air there makes high pressure, which brings dry, clear weather", "correct": True,
              "feedback": "Yes. Sinking air forms a belt of high pressure, and high pressure usually means fair, dry weather."},
             {"text": "It's the hottest place on Earth", "feedback": "The equator gets the most direct sunlight. Deserts near 30° come from sinking, dry air."},
             {"text": "No wind reaches 30°", "feedback": "Winds blow there. The dryness comes from air sinking and forming high pressure."},
             {"text": "The ocean is too far away", "feedback": "Some of these deserts are on coasts. The cause is sinking air and high pressure."}]},
        {"type": "choice", "title": "Causes", "instruction": "Think about the whole pattern.", "showsDiagram": True,
         "question": "Which two things cause the pattern of wind belts?",
         "options": [
             {"text": "Uneven heating by the sun, and Earth's rotation", "correct": True,
              "feedback": "Right. Uneven heating sets air moving between the equator and poles; Earth's spin bends it into east and west winds."},
             {"text": "The moon's gravity and the tides", "feedback": "Tides don't make the wind belts. The sun's uneven heating and Earth's spin do."},
             {"text": "Mountains and forests", "feedback": "Land shapes local winds, but the global belts come from uneven heating and Earth's spin."},
             {"text": "Only Earth's rotation", "feedback": "Rotation bends the winds, but uneven heating by the sun is what sets the air moving."}]},
    ],
}

# ---------------------------------------------------------------- An aquifer cross-section
WT = 470  # water table away from the well
W0, W1 = 590, 610  # the well's walls
left_wet = [40, WT, 500, 475, W0, 560, W0, 700, 40, 700]
right_wet = [W1, 560, 700, 475, 960, WT, 960, 700, W1, 700]
aquifer = {
    "id": "g6-aquifer", "title": "An aquifer cross-section", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS3-1", "minutes": 10, "colorMode": "illustration",
    "sources": [ngss("MS-ESS3-1", "Construct a scientific explanation based on evidence for how the uneven distributions of Earth's "
                                   "mineral, energy, and groundwater resources are the result of past and current geoscience processes"),
                geo("14.1", "14-1-groundwater-and-aquifers", "Groundwater and Aquifers"), geo("14.2", "14-2-groundwater-flow", "Groundwater Flow"),
                geo("14.3", "14-3-groundwater-extraction", "Groundwater Extraction")],
    "keywords": ["aquifer", "groundwater", "water table", "well", "porosity", "permeability", "clay", "sand", "gravel",
                 "recharge", "cone of depression", "natural resources"],
    "legend": [{"name": "Water-filled sand", "color": "#7FB3D9", "meaning": "Sand and gravel with every pore full of water"},
               {"name": "Clay", "color": "#9C7B6B", "meaning": "Tight layer that water barely passes through"}],
    "structures": [
        {"id": "surface", "name": "ground surface", "pen": "bold", "outlines": [{"line": [40, 300, 300, 282, 560, 300]},
                                                                               {"line": [640, 298, 960, 290]}]},
        {"id": "rain", "name": "rain soaking in", "outlines": straight_arrow(200, 100, 200, 250) + straight_arrow(330, 100, 330, 240)
                                                              + straight_arrow(265, 330, 265, 440)},
        {"id": "wet", "name": "saturated zone", "colorName": "water-filled sand", "fill": "#7FB3D9",
         "outlines": [{"polygon": left_wet}, {"polygon": right_wet}]},
        {"id": "clay", "name": "clay layer", "colorName": "clay", "fill": "#9C7B6B", "outlines": [{"rect": [40, 700, 920, 110]}]},
        {"id": "well", "name": "well", "pen": "bold", "outlines": [{"line": [W0, 300, W0, 680]}, {"line": [W1, 300, W1, 680]},
                                                                   {"rect": [565, 240, 70, 46]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Ground", "structure": "surface", "instruction": "Trace the ground surface on both sides of the well.",
         "note": {"text": "Below the ground, rock and sediment have tiny open spaces called pores. Groundwater is stored in them."}},
        {"type": "trace", "title": "Rain", "structure": "rain", "instruction": "Draw the rain falling and the arrow soaking into the ground.",
         "note": {"text": "Rain and snowmelt soak into the ground and trickle down. This refills, or recharges, the groundwater.",
                  "remember": "Recharge: water soaking in."}},
        {"type": "trace", "title": "Saturated zone", "structure": "wet", "instruction": "Trace the zone where every pore is full of water, on both sides.",
         "note": {"text": "Its top is the water table. Sand and gravel make a good aquifer: their pores are big and connected, so water flows through.",
                  "remember": "Aquifer: rock that holds and passes water."}},
        {"type": "trace", "title": "Clay", "structure": "clay", "instruction": "Trace the clay layer below.",
         "note": {"text": "Clay's pores are tiny and poorly connected, so water barely moves through it. It holds the groundwater above it."}},
        {"type": "trace", "title": "Well", "structure": "well", "instruction": "Trace the well and its pump.",
         "note": {"text": "Pumping lowers the water around the well, making a dip in the water table: a cone of depression.",
                  "remember": "Pumping draws the water table down."}},
        {"type": "color", "title": "Color", "structures": ["wet", "clay"], "instruction": "Color the water-filled sand and the clay."},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [250, 470], "answer": "Water table", "role": "Top of the saturated zone."},
             {"n": 2, "at": [300, 600], "answer": "Aquifer", "role": "Water-filled sand and gravel.",
              "mistakes": {"Clay layer": "This layer is sand and gravel that holds and passes water: the aquifer."}},
             {"n": 3, "at": [300, 755], "answer": "Clay layer", "role": "Water barely passes through."},
             {"n": 4, "at": [600, 545], "answer": "Cone of depression", "role": "Dip made by pumping."}],
         "vocabulary": ["Water table", "Aquifer", "Clay layer", "Cone of depression", "Bedrock"]},
        {"type": "choice", "title": "Too much pumping", "instruction": "Think about the well.", "showsDiagram": True,
         "question": "A town pumps water out faster than rain can recharge the aquifer. What happens over the years?",
         "options": [
             {"text": "The water table drops, and shallow wells can go dry", "correct": True,
              "feedback": "Yes. When the cone of depression spreads and deepens, nearby wells may end above the water and go dry."},
             {"text": "The aquifer fills up more", "feedback": "Taking out more than comes in lowers the water, not raises it."},
             {"text": "Nothing: groundwater never runs out", "feedback": "Groundwater is limited. It refills slowly, so heavy pumping can use it up."},
             {"text": "The clay turns into sand", "feedback": "The rock doesn't change. The water table drops."}]},
        {"type": "choice", "title": "Uneven resources", "instruction": "Compare places.", "showsDiagram": True,
         "question": "Why do some places have lots of groundwater and others very little?",
         "options": [
             {"text": "It depends on the rock and sediment underground, which past geologic processes laid down", "correct": True,
              "feedback": "Right. Sand and gravel left by old rivers and glaciers hold lots of water; solid granite holds little."},
             {"text": "Groundwater is spread evenly everywhere", "feedback": "It isn't. Porous sand and gravel hold far more than solid rock."},
             {"text": "People put it there", "feedback": "Groundwater collects naturally in porous rock and sediment."},
             {"text": "Only deserts have groundwater", "feedback": "Groundwater is found almost everywhere, but how much depends on the rock."}]},
    ],
}

# ---------------------------------------------------------------- Inside a volcano
ash = ("M 400 255 C 340 250 330 190 380 175 C 360 120 420 80 470 105 C 500 55 580 60 600 110 "
       "C 650 90 700 140 670 185 C 710 210 690 260 640 255 Z")
bulge = "M 666 420 C 760 440 820 540 810 620"
volcano = {
    "id": "g6-volcano", "title": "Inside a volcano", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS3-2", "minutes": 10, "colorMode": "illustration",
    "sources": [ngss("MS-ESS3-2", "Analyze and interpret data on natural hazards to forecast future catastrophic events and inform the "
                                   "development of technologies to mitigate their effects"),
                geo("4.3", "4-3-types-of-volcanoes", "Types of Volcanoes"),
                geo("4.5", "4-5-monitoring-volcanoes-and-predicting-eruptions", "Monitoring Volcanoes and Predicting Eruptions")],
    "keywords": ["volcano", "magma chamber", "vent", "crater", "ash", "eruption", "earthquakes", "monitoring", "prediction",
                 "natural hazards", "Mount St. Helens", "composite volcano"],
    "printed": [{"text": "Not to scale", "at": [140, 960], "size": 26}],
    "legend": [{"name": "Magma", "color": "#E8622C", "meaning": "Molten rock, glowing hot"},
               {"name": "Ash cloud", "color": "#9A9A9A", "meaning": "Gas and tiny bits of shattered rock"}],
    "structures": [
        {"id": "cone", "name": "volcano", "pen": "bold", "outlines": [{"line": [60, 800, 420, 300, 455, 335, 545, 335, 580, 300, 940, 800]}]},
        {"id": "chamber", "name": "magma chamber", "colorName": "magma", "fill": "#E8622C", "outlines": [{"ellipse": [500, 890, 150, 56]}]},
        {"id": "vent", "name": "vent", "outlines": [{"line": [482, 836, 482, 345]}, {"line": [518, 836, 518, 345]}]},
        {"id": "ash", "name": "ash cloud", "colorName": "ash cloud", "fill": "#9A9A9A", "outlines": [{"path": ash}]},
        {"id": "quakes", "name": "small earthquakes", "outlines": [{"line": [300, 880, 315, 860, 330, 900, 345, 860, 360, 880]},
                                                                   {"line": [640, 880, 655, 860, 670, 900, 685, 860, 700, 880]}]},
        {"id": "bulge", "name": "bulge", "pen": "fine", "outlines": [{"path": bulge}]},
    ],
    "steps": [
        {"type": "trace", "title": "Volcano", "structure": "cone", "instruction": "Trace the volcano and its crater.",
         "note": {"text": "Steep volcanoes like Mount St. Helens are built of layers of lava and ash. Most stand near subduction zones."}},
        {"type": "trace", "title": "Magma chamber", "structure": "chamber", "instruction": "Trace the magma chamber deep below.",
         "note": {"text": "Magma collects in a chamber kilometres underground. Under Mount St. Helens it's about 6 to 14 km down.",
                  "remember": "Magma chamber: the store of melted rock."}},
        {"type": "trace", "title": "Vent", "structure": "vent", "instruction": "Trace the vent rising to the crater.",
         "note": {"text": "Magma rises through the vent and erupts from the crater at the top."}},
        {"type": "trace", "title": "Ash cloud", "structure": "ash", "instruction": "Trace the ash cloud.",
         "note": {"text": "Gas-rich magma can erupt explosively, blasting ash high into the sky."}},
        {"type": "trace", "title": "Warning: earthquakes", "structure": "quakes", "instruction": "Draw the two zigzags for small earthquakes.",
         "note": {"text": "Hundreds of small earthquakes show magma moving underground. Seismometers detect them.",
                  "remember": "Swarms of small quakes are a warning."}},
        {"type": "trace", "title": "Warning: bulge", "structure": "bulge", "instruction": "Draw the bulge swelling out of the volcano's side.",
         "note": {"text": "A volcano swells as magma pushes up. Tiltmeters and GPS measure it. Rising gas is another warning sign."}},
        {"type": "color", "title": "Color", "structures": ["chamber", "ash"], "instruction": "Color the magma and the ash cloud."},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [500, 890], "answer": "Magma chamber", "role": "Store of magma."},
             {"n": 2, "at": [500, 600], "answer": "Vent", "role": "Path up to the surface.",
              "mistakes": {"Crater": "The crater is the bowl at the top. This pipe leading up to it is the vent."}},
             {"n": 3, "at": [500, 320], "answer": "Crater", "role": "Opening at the top."},
             {"n": 4, "at": [520, 170], "answer": "Ash cloud", "role": "Blasted into the sky."}],
         "vocabulary": ["Magma chamber", "Vent", "Crater", "Ash cloud", "Lava"]},
        {"type": "choice", "title": "Forecast", "instruction": "You monitor a volcano.", "showsDiagram": True,
         "question": "Which set of readings would most strongly suggest an eruption is coming?",
         "options": [
             {"text": "Many small earthquakes, the side swelling, and more gas", "correct": True,
              "feedback": "Yes. Together they show magma rising and pressure building, so scientists can warn people to leave."},
             {"text": "A sunny, calm day", "feedback": "Weather doesn't tell us about magma. Scientists watch quakes, swelling and gas."},
             {"text": "No change at all for years", "feedback": "No change suggests the magma isn't moving. Changes are the warning signs."},
             {"text": "Snow on the summit", "feedback": "Snow is weather. The warning signs are quakes, swelling and gas."}]},
        {"type": "choice", "title": "Hazards compared", "instruction": "Compare two hazards.", "showsDiagram": False,
         "question": "Why can scientists often forecast volcanic eruptions but not earthquakes on a fault?",
         "options": [
             {"text": "Eruptions usually give warning signs first; most big earthquakes strike suddenly", "correct": True,
              "feedback": "Right. Rising magma causes quakes, swelling and gas before an eruption. Fault earthquakes rarely give such warnings."},
             {"text": "Volcanoes never erupt without warning", "feedback": "Not never, but usually there are signs. Fault earthquakes rarely give any."},
             {"text": "Earthquakes don't cause damage", "feedback": "Earthquakes can be very destructive. They're just much harder to predict."},
             {"text": "Scientists don't study earthquakes", "feedback": "They do, closely. But most earthquakes still strike with no notice."}]},
    ],
}

# ---------------------------------------------------------------- The greenhouse effect
EARTH_R, ATMO_R, ECY = 1500, 1750, 2300  # Earth's surface and the top of the atmosphere, as huge circles centered far below


def surface_y(x, radius=EARTH_R): return r(ECY - math.sqrt(radius ** 2 - (x - 500) ** 2))


def molecule(cx, cy):
    """CO2: a carbon atom between two oxygens."""
    return [{"circle": [cx - 30, cy, 15]}, {"circle": [cx, cy, 15]}, {"circle": [cx + 30, cy, 15]}]


greenhouse = {
    "id": "g6-greenhouse", "title": "The greenhouse effect", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS3-5", "minutes": 10,
    "sources": [ngss("MS-ESS3-5", "Ask questions to clarify evidence of the factors that have caused the rise in global temperatures "
                                   "over the past century"),
                geo("19.1", "19-1-what-makes-the-climate-change", "What Makes the Climate Change?"),
                geo("19.2", "19-2-anthropogenic-climate-change", "Anthropogenic Climate Change")],
    "keywords": ["greenhouse effect", "greenhouse gases", "carbon dioxide", "CO2", "methane", "infrared", "climate change",
                 "global warming", "fossil fuels", "temperature", "atmosphere"],
    "printed": [{"text": "Space", "at": [860, 380], "size": 30}, {"text": "Not to scale", "at": [140, 960], "size": 26}],
    "structures": [
        {"id": "ground", "name": "Earth's surface", "pen": "bold",
         "outlines": [{"path": f"M 40 {surface_y(40)} A {EARTH_R} {EARTH_R} 0 0 1 960 {surface_y(960)}"}]},
        {"id": "atmo", "name": "top of the atmosphere", "pen": "fine",
         "outlines": [{"path": f"M 40 {surface_y(40, ATMO_R)} A {ATMO_R} {ATMO_R} 0 0 1 960 {surface_y(960, ATMO_R)}"}]},
        {"id": "sun", "name": "sun", "pen": "bold", "outlines": [{"circle": [120, 120, 60]}]},
        {"id": "sunlight", "name": "sunlight", "outlines": straight_arrow(180, 180, 415, 785, head=36)},
        {"id": "heat", "name": "heat from the ground", "outlines": straight_arrow(520, 785, 600, 600)},
        {"id": "out", "name": "heat escaping", "outlines": straight_arrow(620, 575, 700, 330)},
        {"id": "back", "name": "heat sent back", "outlines": straight_arrow(660, 600, 660, 790)},
        {"id": "gas", "name": "carbon dioxide", "outlines": molecule(230, 700) + molecule(870, 700)},
        {"id": "chimney", "name": "smokestack", "outlines": [{"polygon": [790, 845, 790, 760, 830, 760, 830, 842]}],
         "details": straight_arrow(810, 750, 810, 660, head=20)},
    ],
    "steps": [
        {"type": "trace", "title": "Ground", "structure": "ground", "instruction": "Trace Earth's curved surface.",
         "note": {"text": "Sunlight warms Earth. The air above controls how much of that heat escapes back to space."}},
        {"type": "trace", "title": "Atmosphere", "structure": "atmo", "instruction": "Trace the top of the atmosphere.",
         "note": {"text": "The atmosphere is mostly nitrogen and oxygen, which don't trap heat."}},
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "Energy reaches Earth from the sun as light."}},
        {"type": "trace", "title": "Sunlight", "structure": "sunlight", "instruction": "Draw sunlight passing through the air to the ground.",
         "note": {"text": "Sunlight passes through the air and warms the ground.", "remember": "Sunlight in, heats the ground."}},
        {"type": "trace", "title": "Heat rising", "structure": "heat", "instruction": "Draw the arrow of heat leaving the ground.",
         "note": {"text": "The warm ground gives off invisible infrared radiation: heat energy."}},
        {"type": "trace", "title": "Escaping", "structure": "out", "instruction": "Draw the arrow of heat escaping to space.",
         "note": {"text": "Some of that heat escapes out to space."}},
        {"type": "trace", "title": "Sent back", "structure": "back", "instruction": "Draw the arrow of heat sent back down.",
         "note": {"text": "Greenhouse gases absorb some heat and send it out in all directions, some back down. This warms the surface.",
                  "remember": "Greenhouse gases trap heat."}},
        {"type": "trace", "title": "Greenhouse gas", "structure": "gas", "instruction": "Trace the two carbon dioxide molecules.",
         "note": {"text": "Gases with three or more atoms, like carbon dioxide (CO2), methane and water vapor, are greenhouse gases."}},
        {"type": "trace", "title": "Smokestack", "structure": "chimney", "instruction": "Trace the smokestack.",
         "note": {"text": "Burning coal, oil and gas releases carbon that was stored underground for millions of years, as CO2."}},
        {"type": "trace", "title": "Emissions", "structure": "chimney", "part": "details", "instruction": "Draw the arrow of CO2 rising.",
         "note": {"text": "Earth is now about 1 °C warmer than before industry, and two-thirds of that warming came after 1975.",
                  "remember": "More CO2, more trapped heat."}},
        {"type": "choice", "title": "Explain", "instruction": "Use the model.", "showsDiagram": True,
         "question": "How does adding more carbon dioxide to the air raise Earth's temperature?",
         "options": [
             {"text": "More of the ground's heat is absorbed and sent back down instead of escaping", "correct": True,
              "feedback": "Yes. More greenhouse gas means less heat escapes to space, so the surface warms."},
             {"text": "Carbon dioxide makes the sun shine brighter", "feedback": "CO2 doesn't change the sun. It traps heat leaving the ground."},
             {"text": "Carbon dioxide is hot smoke", "feedback": "The gas itself isn't the heat source. It traps heat that would escape."},
             {"text": "It blocks all sunlight", "feedback": "Sunlight still gets through. CO2 traps the heat the ground gives off."}]},
        {"type": "choice", "title": "Ask a good question", "instruction": "Scientists test every possible cause.", "showsDiagram": False,
         "question": "Someone says the warming of the past century was caused by the sun. Which question would best test that?",
         "options": [
             {"text": "Has the sun's energy output actually increased over the past century?", "correct": True,
              "feedback": "Right. A good question asks for evidence. Scientists compare the sun's measured output with the temperature record."},
             {"text": "Is the sun hot?", "feedback": "Everyone agrees the sun is hot. The question is whether its output changed."},
             {"text": "Do people like sunny days?", "feedback": "That's opinion, not evidence about the cause of warming."},
             {"text": "Is the sun far away?", "feedback": "Its distance barely changes. Ask whether its energy output has gone up."}]},
    ],
}

for lesson in (water, front, winds, aquifer, volcano, greenhouse):
    save(lesson)
