"""Grade 4 Earth science · rock layers (4-ESS1-1), ice wedging (4-ESS2-1), the Ring of Fire
(4-ESS2-2), energy resources (4-ESS3-1) and an earthquake-resistant building (4-ESS3-2).

Facts checked against the Geological Society of London, the National Park Service, Physical
Geology (Earle and Panchuk, BCcampus), National Geographic Education, the U.S. Energy
Information Administration and FEMA P-749.
"""
import math

from lib import save, straight_arrow


def ngss(code, text):
    return {"title": f"NGSS {code}: {text}"}


GEOLSOC = {"title": "Geological Society of London: Burial and Compaction (oldest layers at the bottom)",
           "url": "https://www.geolsoc.org.uk/ks3/gsl/education/resources/rockcycle/page3464.html"}
TETON = {"title": "National Park Service, Grand Teton: Fossils (marine fossils show an ancient sea floor)",
         "url": "https://www.nps.gov/grte/learn/nature/fossils.htm"}
GRCA = {"title": "National Park Service, Grand Canyon: Fossils", "url": "https://www.nps.gov/grca/learn/nature/fossils.htm"}
WEATHERING = {"title": "Physical Geology, H5P Edition (Earle and Panchuk, BCcampus), 8.1 Physical Weathering",
              "url": "https://opentextbc.ca/physicalgeologyh5p/chapter/mechanical-weathering/"}
RING = {"title": "National Geographic Education: Ring of Fire", "url": "https://education.nationalgeographic.org/resource/ring-fire/"}
EIA = {"title": "U.S. Energy Information Administration, Energy Kids: Energy sources", "url": "https://www.eia.gov/kids/energy-sources/"}
EIA_NONRENEW = {"title": "U.S. Energy Information Administration, Energy Kids: Nonrenewable energy sources",
                "url": "https://www.eia.gov/kids/energy-sources/nonrenewable.php"}
FEMA = {"title": "FEMA P-749, Earthquake-Resistant Design Concepts (2022): 8.1.2 Braced Frame Systems, 10.5 Seismic Isolation Systems",
        "url": "https://www.wbdg.org/FFC/DHS/fema_p749_2022.pdf"}
QUAKES = {"title": "Physical Geology, H5P Edition (Earle and Panchuk, BCcampus), 12.5 Forecasting Earthquakes and Minimizing Impacts",
          "url": "https://opentextbc.ca/physicalgeologyh5p/chapter/forecasting-earthquakes-and-minimizing-impacts/"}


def shell(x, y):
    """A brachiopod-like fossil shell, about 64 wide."""
    return {"path": f"M {x - 32} {y} C {x - 32} {y - 42} {x + 32} {y - 42} {x + 32} {y} C {x + 12} {y + 12} {x - 12} {y + 12} {x - 32} {y} Z"}


# ---------------------------------------------------------------- Rock layers with fossils
fish_fossil = "M 600 600 C 640 572 712 572 744 600 C 712 628 640 628 600 600 Z"
layers = {
    "id": "g4-rock-layers", "title": "Rock layers with fossils", "grade": "4", "subject": "Earth & space",
    "standard": "4-ESS1-1", "minutes": 8,
    "sources": [ngss("4-ESS1-1", "Identify evidence from patterns in rock formations and fossils in rock layers to support an "
                                  "explanation for changes in a landscape over time"), GEOLSOC, TETON, GRCA],
    "keywords": ["rock layers", "sedimentary rock", "fossils", "superposition", "oldest layer", "landscape change",
                 "ancient sea", "cliff", "evidence"],
    "structures": [
        {"id": "cliff", "name": "rock layers", "pen": "bold",
         "outlines": [{"rect": [150, 200, 700, 640, 8]}],
         "details": [{"line": [150, 362, 420, 352, 850, 366]}, {"line": [150, 520, 500, 528, 850, 514]},
                     {"line": [150, 680, 380, 672, 850, 686]}]},
        {"id": "shells", "name": "shell fossils", "outlines": [shell(300, 770), shell(560, 790), shell(720, 760)]},
        {"id": "fish", "name": "fish fossil",
         "outlines": [{"path": fish_fossil}, {"polygon": [600, 600, 560, 572, 572, 600, 560, 628]}],
         "details": [{"line": [624, 600, 728, 600]}]},
        {"id": "fern", "name": "fern fossil",
         "outlines": [{"line": [480, 344, 560, 216]}, {"line": [496, 318, 446, 296]}, {"line": [508, 300, 560, 300]},
                      {"line": [520, 280, 476, 252]}, {"line": [534, 258, 584, 252]}, {"line": [546, 238, 512, 214]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Cliff", "structure": "cliff", "instruction": "Trace the side of the cliff.",
         "note": {"text": "A cliff or canyon wall shows rock layers, one on top of another, like a stack of pancakes."}},
        {"type": "trace", "title": "Layers", "structure": "cliff", "part": "details", "instruction": "Draw the lines between the four layers.",
         "note": {"text": "Layers form as mud and sand settle in flat sheets, one on top of the last. So the bottom layer is the oldest; the top is the youngest.",
                  "remember": "Oldest at the bottom."}},
        {"type": "trace", "title": "Shells", "structure": "shells", "instruction": "Trace the three shell fossils in the bottom layer.",
         "note": {"text": "These are fossils of sea animals. Finding them tells us this place was once the floor of a sea.",
                  "remember": "Sea fossils: there was once a sea."}},
        {"type": "trace", "title": "Fish", "structure": "fish", "instruction": "Trace the fish fossil and its tail in the second layer.",
         "note": {"text": "A fish fossil means water was still here when this layer formed, after the bottom layer."}},
        {"type": "trace", "title": "Backbone", "structure": "fish", "part": "details", "instruction": "Draw the fish's backbone.",
         "note": {"text": "Hard parts like bones and shells are what usually turn into fossils."}},
        {"type": "trace", "title": "Fern", "structure": "fern", "instruction": "Draw the fern fossil in the top layer: its stem and leaves.",
         "note": {"text": "Ferns grow on land. A land plant in the top layer shows that, much later, the sea was gone and land took its place.",
                  "remember": "Fossils show how a place changed."}},
        {"type": "choice", "title": "Read the layers", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "Which layer formed first?",
         "options": [
             {"text": "The bottom layer", "correct": True,
              "feedback": "Yes. Each layer settled on top of the one before, so the bottom layer is the oldest."},
             {"text": "The top layer", "feedback": "The top layer settled last, so it's the youngest. The bottom one is oldest."},
             {"text": "They all formed at once", "feedback": "Layers form one at a time, each on top of the last."},
             {"text": "The layer with the fern", "feedback": "The fern is in the top layer, the youngest. The bottom layer formed first."}]},
        {"type": "choice", "title": "Explain the change", "instruction": "Think about the fossils.", "showsDiagram": True,
         "question": "What do the fossils tell us about how this place changed over time?",
         "options": [
             {"text": "It was once covered by water, and later became land", "correct": True,
              "feedback": "Right. Sea fossils at the bottom, a fish above, then a land fern on top: the water went away over a very long time."},
             {"text": "It was always dry land", "feedback": "Shell and fish fossils show there was once water here."},
             {"text": "It started as land and became a sea", "feedback": "Read from the bottom up: sea fossils come first (oldest), the land fern last."},
             {"text": "Fossils can't tell us anything", "feedback": "Fossils are evidence: they show what lived here, and so what the place was like."}]},
    ],
}

# ---------------------------------------------------------------- Weathering by ice wedging
ice = {
    "id": "g4-ice-wedging", "title": "Weathering by ice wedging", "grade": "4", "subject": "Earth & space",
    "standard": "4-ESS2-1", "minutes": 7,
    "sources": [ngss("4-ESS2-1", "Make observations and/or measurements to provide evidence of the effects of weathering or the "
                                  "rate of erosion by water, ice, wind, or vegetation"), WEATHERING],
    "keywords": ["weathering", "ice wedging", "frost wedging", "freeze", "thaw", "crack", "rock", "ice", "water", "erosion"],
    "printed": [{"text": "1", "at": [110, 300]}, {"text": "2", "at": [490, 300]}, {"text": "3", "at": [820, 300]}],
    "structures": [
        {"id": "rock1", "name": "rock with a crack",
         "outlines": [{"polygon": [70, 720, 70, 470, 170, 424, 280, 474, 280, 720]}],
         "details": [{"line": [172, 428, 180, 520, 170, 600]}]},
        {"id": "drops", "name": "water drops", "outlines": [{"circle": [170, 376, 9]}, {"circle": [196, 352, 9]}]},
        {"id": "rock2", "name": "rock with a wider crack",
         "outlines": [{"polygon": [380, 720, 380, 470, 486, 424, 600, 474, 600, 720]}],
         "details": [{"line": [466, 432, 490, 620, 516, 436]}]},
        {"id": "ice", "name": "ice", "outlines": [{"polygon": [476, 446, 506, 448, 491, 580]}]},
        {"id": "pieces", "name": "broken rock",
         "outlines": [{"polygon": [700, 720, 700, 474, 790, 432, 800, 560, 772, 720]},
                      {"polygon": [836, 720, 848, 560, 862, 434, 940, 474, 940, 720]}]},
        {"id": "arrows", "name": "arrows", "pen": "bold",
         "outlines": straight_arrow(298, 600, 362, 600) + straight_arrow(618, 600, 682, 600)},
    ],
    "steps": [
        {"type": "trace", "title": "Rock", "structure": "rock1", "instruction": "Trace the first rock.",
         "note": {"text": "Even hard rock has tiny cracks in it."}},
        {"type": "trace", "title": "Crack", "structure": "rock1", "part": "details", "instruction": "Draw the thin crack in the rock.",
         "note": {"text": "Rain and melting snow can seep into a crack."}},
        {"type": "trace", "title": "Water", "structure": "drops", "instruction": "Dab the two drops of water falling into the crack.",
         "note": {"text": "Step 1: water trickles into the crack and fills it."}},
        {"type": "trace", "title": "Second rock", "structure": "rock2", "instruction": "Trace the rock in picture 2.",
         "note": {"text": "Step 2 shows the same rock on a freezing night."}},
        {"type": "trace", "title": "Wider crack", "structure": "rock2", "part": "details", "instruction": "Draw the crack, now wider.",
         "note": {"text": "When water freezes into ice, it expands: it takes up more space. The ice pushes the crack wider.",
                  "remember": "Freezing water expands."}},
        {"type": "trace", "title": "Ice", "structure": "ice", "instruction": "Trace the wedge of ice inside the crack.",
         "note": {"text": "Then the ice melts, more water seeps deeper in, and it freezes again. Each freeze and thaw pushes the crack a little wider."}},
        {"type": "trace", "title": "Broken rock", "structure": "pieces", "instruction": "Trace the two pieces in picture 3.",
         "note": {"text": "Step 3: after many freezes and thaws, the rock splits apart. Breaking rock down like this is called weathering.",
                  "remember": "Ice wedging breaks rock."}},
        {"type": "trace", "title": "Arrows", "structure": "arrows", "instruction": "Draw the arrows from one picture to the next.",
         "note": {"text": "This happens slowly, over many cold nights and warm days."}},
        {"type": "order", "title": "Steps", "items": ["Water seeps into a crack", "The water freezes and expands", "The crack gets wider", "The rock breaks apart"],
         "instruction": "Tap the steps of ice wedging in order.",
         "why": "Water fills the crack, freezes and expands, widening it; after many freezes and thaws, the rock breaks.",
         "hint": "What has to get into the crack first?"},
        {"type": "choice", "title": "Where?", "instruction": "Think about the weather.", "showsDiagram": False,
         "question": "Where does ice wedging break rocks fastest?",
         "options": [
             {"text": "A place that often freezes at night and thaws in the day", "correct": True,
              "feedback": "Yes. Each freeze widens the cracks a little, so many freeze-thaw swings break rock fastest."},
             {"text": "A hot desert", "feedback": "It rarely freezes there, and there's little water to seep into cracks."},
             {"text": "A place that's frozen all year", "feedback": "If it never thaws, the ice doesn't melt and refreeze, so cracks don't keep growing."},
             {"text": "A warm beach", "feedback": "Ice wedging needs freezing. A warm place rarely freezes."}]},
    ],
}

# ---------------------------------------------------------------- The Ring of Fire (simplified map)
asia = "M 60 120 C 200 90 330 130 360 220 C 378 300 332 380 300 430 C 250 470 150 450 60 420 Z"
australia = "M 200 640 C 260 600 352 612 372 680 C 384 748 320 790 240 770 C 180 752 170 692 200 640 Z"
n_america = "M 660 110 C 770 90 920 120 940 200 C 950 300 880 380 800 420 C 760 440 716 420 700 380 C 676 320 650 220 660 110 Z"
s_america = "M 790 500 C 860 480 930 530 922 620 C 912 720 842 830 800 890 C 762 820 744 700 734 620 C 726 560 752 510 790 500 Z"
ring = ("M 412 724 C 420 560 404 440 396 340 C 388 230 444 168 520 160 C 580 154 612 200 616 280 "
        "C 620 360 652 450 690 540 C 714 620 714 740 730 852")


def volcano(x, y):
    return {"polygon": [x - 18, y + 14, x, y - 18, x + 18, y + 14]}


ring_map = {
    "id": "g4-ring-of-fire", "title": "Map of volcanoes and earthquakes: Ring of Fire", "grade": "4", "subject": "Earth & space",
    "standard": "4-ESS2-2", "minutes": 7,
    "sources": [ngss("4-ESS2-2", "Analyze and interpret data from maps to describe patterns of Earth's features"), RING],
    "keywords": ["Ring of Fire", "volcanoes", "earthquakes", "map", "pattern", "Pacific Ocean", "plates", "tectonic plates",
                 "plate boundaries"],
    "printed": [{"text": "Asia", "at": [190, 270]}, {"text": "Australia", "at": [276, 700], "size": 34},
                {"text": "North America", "at": [812, 250], "size": 32}, {"text": "South America", "at": [832, 624], "size": 26}],
    "structures": [
        {"id": "land", "name": "continents",
         "outlines": [{"path": asia}, {"path": australia}, {"path": n_america}, {"path": s_america}]},
        {"id": "ring", "name": "Ring of Fire", "pen": "bold", "outlines": [{"path": ring}]},
        {"id": "volcanoes", "name": "volcanoes",
         "outlines": [volcano(412, 620), volcano(398, 420), volcano(450, 186), volcano(600, 216), volcano(636, 420),
                      volcano(704, 640), volcano(718, 790)]},
    ],
    "steps": [
        {"type": "trace", "title": "Continents", "structure": "land", "instruction": "Trace the four continents around the big ocean.",
         "note": {"text": "This simplified map shows the lands around the Pacific Ocean: Asia and Australia on one side, the Americas on the other."}},
        {"type": "trace", "title": "Ring of Fire", "structure": "ring", "instruction": "Trace the curved line around the edge of the ocean.",
         "note": {"text": "This horseshoe-shaped path is the Ring of Fire. About 90 percent of Earth's earthquakes happen along it.",
                  "remember": "Ring of Fire: around the Pacific."}},
        {"type": "trace", "title": "Volcanoes", "structure": "volcanoes", "instruction": "Trace the seven volcanoes along the ring.",
         "note": {"text": "About three out of every four of Earth's volcanoes, more than 450, are on the Ring of Fire.",
                  "remember": "Most volcanoes are on the ring."}},
        {"type": "choice", "title": "Find the pattern", "instruction": "Read the map.", "showsDiagram": True,
         "question": "What pattern does the map show about where volcanoes are?",
         "options": [
             {"text": "Many are in a ring around the edge of the Pacific Ocean", "correct": True,
              "feedback": "Yes. Volcanoes and earthquakes aren't scattered randomly: they line up around the Pacific."},
             {"text": "They're spread evenly everywhere", "feedback": "Look again: they cluster in a line around the ocean's edge."},
             {"text": "They're all in the middle of the ocean", "feedback": "On this map they follow the edges of the ocean, near the coasts."},
             {"text": "There's no pattern", "feedback": "There is one: they follow a ring around the Pacific."}]},
        {"type": "choice", "title": "Why there?", "instruction": "Think about Earth's crust.", "showsDiagram": True,
         "question": "Earth's surface is broken into giant pieces called plates. Why are so many volcanoes and earthquakes on the Ring of Fire?",
         "options": [
             {"text": "The ring follows the edges where plates meet", "correct": True,
              "feedback": "Right. The Ring of Fire traces the boundaries between several plates, where the ground is most active."},
             {"text": "The ocean water heats the rocks", "feedback": "The cause is underground: the ring follows the edges of Earth's plates."},
             {"text": "More people live there", "feedback": "People don't cause volcanoes. The ring follows plate edges."},
             {"text": "It's the hottest part of Earth", "feedback": "It's not about air temperature. The ring follows where plates meet."}]},
    ],
}

# ---------------------------------------------------------------- Renewable and nonrenewable energy
sun_rays = [{"line": [round(275 + 62 * math.cos(math.radians(a)), 1), round(250 + 62 * math.sin(math.radians(a)), 1),
                      round(275 + 90 * math.cos(math.radians(a)), 1), round(250 + 90 * math.sin(math.radians(a)), 1)]}
            for a in range(0, 360, 45)]
blades = [{"line": [275, 500, round(275 + 86 * math.sin(math.radians(a)), 1), round(500 - 86 * math.cos(math.radians(a)), 1)]}
          for a in (0, 120, 240)]
energy = {
    "id": "g4-energy-sources", "title": "Renewable and nonrenewable energy sources", "grade": "4", "subject": "Earth & space",
    "standard": "4-ESS3-1", "minutes": 7,
    "sources": [ngss("4-ESS3-1", "Obtain and combine information to describe that energy and fuels are derived from natural "
                                  "resources and their uses affect the environment"), EIA, EIA_NONRENEW],
    "keywords": ["energy", "renewable", "nonrenewable", "solar", "wind", "hydropower", "coal", "oil", "petroleum",
                 "natural gas", "fossil fuels", "natural resources"],
    "printed": [{"text": "Renewable", "at": [275, 110]}, {"text": "Nonrenewable", "at": [725, 110]}],
    "structures": [
        {"id": "divider", "name": "dividing line", "outlines": [{"line": [500, 150, 500, 900]}]},
        {"id": "sun", "name": "sun", "outlines": [{"circle": [275, 250, 48]}], "details": sun_rays},
        {"id": "wind", "name": "wind turbine", "outlines": [{"line": [275, 660, 275, 514]}, {"circle": [275, 500, 12]}],
         "details": blades},
        {"id": "water", "name": "moving water",
         "outlines": [{"path": "M 160 760 C 200 730 240 790 280 760 C 320 730 360 790 400 760"},
                      {"path": "M 160 820 C 200 790 240 850 280 820 C 320 790 360 850 400 820"}]},
        {"id": "coal", "name": "coal", "outlines": [{"polygon": [664, 284, 686, 214, 740, 196, 790, 222, 798, 280, 740, 304]}]},
        {"id": "oil", "name": "oil barrel", "outlines": [{"rect": [680, 430, 90, 130, 8]}],
         "details": [{"line": [680, 474, 770, 474]}, {"line": [680, 516, 770, 516]}]},
        {"id": "gas", "name": "natural gas flame",
         "outlines": [{"path": "M 725 700 C 760 750 782 790 762 832 C 744 862 706 862 688 832 C 668 790 690 750 725 700 Z"}]},
    ],
    "steps": [
        {"type": "trace", "title": "Two kinds", "structure": "divider", "instruction": "Draw the line splitting the page in two.",
         "note": {"text": "All our energy comes from natural resources. Some are renewable, and some are nonrenewable."}},
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "Solar energy comes from sunlight. It's renewable: it's replaced naturally, so it won't run out.",
                  "remember": "Renewable = replaced naturally."}},
        {"type": "trace", "title": "Sunbeams", "structure": "sun", "part": "details", "instruction": "Draw the sun's rays.",
         "note": {"text": "Solar panels change sunlight into electricity."}},
        {"type": "trace", "title": "Wind turbine", "structure": "wind", "instruction": "Trace the turbine's pole and hub.",
         "note": {"text": "Wind is renewable too. Wind turbines turn moving air into electricity."}},
        {"type": "trace", "title": "Blades", "structure": "wind", "part": "details", "instruction": "Draw the three blades.",
         "note": {"text": "The wind keeps blowing, so this energy source is replaced naturally."}},
        {"type": "trace", "title": "Moving water", "structure": "water", "instruction": "Draw the two waves of moving water.",
         "note": {"text": "Hydropower uses moving water to make electricity. It's renewable too: most renewable energy is used to make electricity."}},
        {"type": "trace", "title": "Coal", "structure": "coal", "instruction": "Trace the lump of coal.",
         "note": {"text": "Coal is a fossil fuel. It took thousands of years to form from buried plants and animals. It's nonrenewable.",
                  "remember": "Fossil fuels: coal, oil, natural gas."}},
        {"type": "trace", "title": "Oil", "structure": "oil", "instruction": "Trace the oil barrel.",
         "note": {"text": "Oil is a fossil fuel too. We can only use what's already in the ground, so one day it could run out."}},
        {"type": "trace", "title": "Barrel bands", "structure": "oil", "part": "details", "instruction": "Draw the two bands around the barrel.",
         "note": {"text": "Crude oil is also called petroleum."}},
        {"type": "trace", "title": "Natural gas", "structure": "gas", "instruction": "Trace the flame of natural gas.",
         "note": {"text": "Natural gas is the third fossil fuel. Like coal and oil, it can't be made again quickly."}},
        {"type": "choice", "title": "Explain", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "Why are coal, oil and natural gas called nonrenewable?",
         "options": [
             {"text": "They took a very long time to form, so we can't make more quickly", "correct": True,
              "feedback": "Yes. They formed from buried plants and animals long ago. There's only so much in the ground."},
             {"text": "They're too heavy to move", "feedback": "Weight isn't it. They can't be made again in a short time."},
             {"text": "They don't make any energy", "feedback": "They make lots of energy, but they can't be replaced quickly."},
             {"text": "Only adults can use them", "feedback": "It's about supply: they can't be made again quickly."}]},
        {"type": "choice", "title": "Sort it", "instruction": "One more.", "showsDiagram": False,
         "question": "Which of these is a renewable energy source?",
         "options": [
             {"text": "Wind", "correct": True, "feedback": "Right. The wind is replaced naturally, so it won't run out."},
             {"text": "Coal", "feedback": "Coal is a fossil fuel: nonrenewable."},
             {"text": "Natural gas", "feedback": "Natural gas is a fossil fuel: nonrenewable."},
             {"text": "Uranium", "feedback": "Uranium, used in nuclear power, is mined and is nonrenewable."}]},
    ],
}

# ---------------------------------------------------------------- An earthquake-resistant building
braces = []
for top, bottom in ((300, 410), (410, 520), (520, 630), (630, 740)):
    braces += [{"line": [338, top + 8, 662, bottom - 8]}, {"line": [662, top + 8, 338, bottom - 8]}]
building = {
    "id": "g4-earthquake-building", "title": "An earthquake-resistant building", "grade": "4", "subject": "Earth & space",
    "standard": "4-ESS3-2", "minutes": 8,
    "sources": [ngss("4-ESS3-2", "Generate and compare multiple solutions to reduce the impacts of natural Earth processes on humans"),
                FEMA, QUAKES],
    "keywords": ["earthquake", "building", "engineering", "base isolation", "bearings", "braces", "cross bracing",
                 "natural hazards", "design", "safety"],
    "printed": [{"text": "Ground shakes", "at": [500, 930]}],
    "structures": [
        {"id": "ground", "name": "ground", "pen": "bold", "outlines": [{"line": [60, 812, 940, 812]}]},
        {"id": "building", "name": "building", "pen": "bold", "outlines": [{"rect": [330, 300, 340, 440, 4]}],
         "details": [{"line": [330, 410, 670, 410]}, {"line": [330, 520, 670, 520]}, {"line": [330, 630, 670, 630]}]},
        {"id": "braces", "name": "cross braces", "outlines": braces},
        {"id": "isolators", "name": "isolators",
         "outlines": [{"rect": [350, 756, 64, 40, 8]}, {"rect": [468, 756, 64, 40, 8]}, {"rect": [586, 756, 64, 40, 8]}]},
        {"id": "shake", "name": "shaking", "pen": "bold", "outlines": straight_arrow(470, 870, 130, 870) + straight_arrow(530, 870, 870, 870)},
    ],
    "steps": [
        {"type": "trace", "title": "Ground", "structure": "ground", "instruction": "Trace the ground line.",
         "note": {"text": "In an earthquake, the ground shakes. Buildings that aren't built to handle the shaking can be badly damaged."}},
        {"type": "trace", "title": "Building", "structure": "building", "instruction": "Trace the outside of the building.",
         "note": {"text": "Engineers can't stop earthquakes, but they can design buildings that keep people safer when one strikes."}},
        {"type": "trace", "title": "Floors", "structure": "building", "part": "details", "instruction": "Draw the three floors inside.",
         "note": {"text": "Each floor is held up by the frame of the building."}},
        {"type": "trace", "title": "Cross braces", "structure": "braces", "instruction": "Draw an X of braces on every floor.",
         "note": {"text": "Diagonal steel braces make an X on each floor. They stiffen the frame so it resists being pushed sideways.",
                  "remember": "Braces resist sideways shaking."}},
        {"type": "trace", "title": "Isolators", "structure": "isolators", "instruction": "Trace the three isolators between the building and the ground.",
         "note": {"text": "Isolators are thick pads of rubber and steel layers under the building. The ground can move under them, so less shaking reaches the building.",
                  "remember": "Isolators soak up shaking."}},
        {"type": "trace", "title": "Shaking", "structure": "shake", "instruction": "Draw the arrows showing the ground shaking both ways.",
         "note": {"text": "Strong building rules, called codes, help make sure new buildings are built to be earthquake-safe."}},
        {"type": "label", "title": "Label the parts", "instruction": "Pick the right name for each numbered part.",
         "targets": [
             {"n": 1, "at": [500, 355], "answer": "Cross brace", "role": "Stiffens the frame against sideways shaking."},
             {"n": 2, "at": [500, 776], "answer": "Isolator", "role": "Rubber-and-steel pad that soaks up shaking."},
             {"n": 3, "at": [700, 812], "answer": "Ground", "role": "Shakes in an earthquake."}],
         "vocabulary": ["Cross brace", "Isolator", "Ground", "Roof", "Window"],
         "commonMistakes": {"Roof": "The roof is at the very top. This part is between the building and the ground: an isolator."}},
        {"type": "choice", "title": "Compare solutions", "instruction": "Think like an engineer.", "showsDiagram": True,
         "question": "Which plan would best protect people in this building during an earthquake?",
         "options": [
             {"text": "Add braces and isolators, as drawn", "correct": True,
              "feedback": "Yes. Braces make the frame stronger, and isolators reduce how much shaking reaches it. Together they help most."},
             {"text": "Paint the building a bright color", "feedback": "Color doesn't change how the building handles shaking."},
             {"text": "Add more floors on top", "feedback": "A taller building isn't safer by itself. Braces and isolators are what help."},
             {"text": "Remove the braces to make it lighter", "feedback": "The braces stop the frame bending sideways. Taking them out makes it weaker."}]},
    ],
}

for lesson in (layers, ice, ring_map, energy, building):
    save(lesson)
