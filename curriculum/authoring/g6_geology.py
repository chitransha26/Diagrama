"""Grade 6 geology · reading rock layers (MS-ESS1-4), the rock cycle (MS-ESS2-1), a river delta (MS-ESS2-2), plate
boundaries and Pangaea (MS-ESS2-3).

Facts checked against Steven Earle's Physical Geology, 2nd edition (BCcampus, CC BY 4.0): 1.5, 3.1, 8.2, 10.1, 10.4,
13.3 and 13.4. OpenStax has no geology book, so this open, peer-reviewed university text stands in for it.
"""
import math

from lib import save, straight_arrow, r


def ngss(code, text):
    return {"title": f"NGSS {code}: {text}"}


def geo(section, slug, title):
    return {"title": f"Earle, Physical Geology 2nd ed. (BCcampus), {section} {title}",
            "url": f"https://opentextbc.ca/physicalgeology2ed/chapter/{slug}/"}


ESS2_3 = ngss("MS-ESS2-3", "Analyze and interpret data on the distribution of fossils and rocks, continental shapes, and seafloor "
                           "structures to provide evidence of the past plate motions")
BOUNDARIES = geo("10.4", "10-4-plate-plate-motions-and-plate-boundary-processes", "Plates, Plate Motions, and Plate Boundary Processes")


def rect(x, y, w, h):
    return {"rect": [x, y, w, h]}


# ---------------------------------------------------------------- Reading rock layers
DX0, DX1 = 540, 600  # the dike's sides
layers = [("A", "top layer", 200, 330, "#D9C28A", "sandstone"), ("B", "layer B", 330, 480, "#8C8F94", "shale"),
          ("C", "layer C", 480, 630, "#D8D4C8", "limestone"), ("D", "layer D", 630, 800, "#D9C28A", "sandstone")]


def layer(letter, name, top, bottom, fill, rock):
    cut = letter != "A"  # the dike cuts every layer except the top one
    shapes = [rect(100, top, DX0 - 100, bottom - top), rect(DX1, top, 900 - DX1, bottom - top)] if cut else [rect(100, top, 800, bottom - top)]
    return {"id": letter, "name": name, "colorName": f"{rock} ({name})", "fill": fill, "outlines": shapes}


def shell(cx, cy):
    """A small clam shell."""
    return [{"path": f"M {cx - 26} {cy + 8} C {cx - 22} {cy - 24} {cx + 22} {cy - 24} {cx + 26} {cy + 8} L {cx} {cy + 16} Z"}]


rock_layers = {
    "id": "g6-rock-layers", "title": "Reading rock layers and geologic history", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS1-4", "minutes": 10, "colorMode": "illustration",
    "sources": [ngss("MS-ESS1-4", "Construct a scientific explanation based on evidence from rock strata for how the geologic time "
                                   "scale is used to organize Earth's 4.6-billion-year-old history"),
                geo("8.2", "8-2-relative-dating-methods", "Relative Dating Methods"),
                geo("3.1", "3-1-the-rock-cycle", "The Rock Cycle")],
    "keywords": ["rock layers", "strata", "superposition", "cross-cutting", "relative age", "fossils", "dike", "igneous",
                 "sedimentary", "geologic time scale", "history"],
    "printed": [{"text": "A", "at": [60, 265], "size": 36}, {"text": "B", "at": [60, 405], "size": 36},
                {"text": "C", "at": [60, 555], "size": 36}, {"text": "D", "at": [60, 715], "size": 36}],
    "legend": [{"name": "Sandstone", "color": "#D9C28A", "meaning": "Sand grains cemented together"},
               {"name": "Shale", "color": "#8C8F94", "meaning": "Hardened mud"},
               {"name": "Limestone", "color": "#D8D4C8", "meaning": "Often made from shells"},
               {"name": "Dike", "color": "#3E3B3A", "meaning": "Dark igneous rock that cooled from magma"}],
    "structures": [layer(*l) for l in reversed(layers)] + [
        {"id": "dike", "name": "dike", "colorName": "dike", "fill": "#3E3B3A", "pen": "bold", "outlines": [rect(DX0, 330, DX1 - DX0, 470)]},
        {"id": "fossils", "name": "shell fossils", "outlines": shell(260, 560) + shell(760, 560)},
    ],
    "steps": [
        {"type": "trace", "title": "Layer D", "structure": "D", "instruction": "Trace the bottom layer, on both sides of the gap.",
         "note": {"text": "Sediment settles in flat layers, one on top of another. The bottom layer was laid down first.",
                  "remember": "Bottom layer = oldest."}},
        {"type": "trace", "title": "Layer C", "structure": "C", "instruction": "Trace layer C, on both sides.",
         "note": {"text": "Layer C settled on top of D, so it's younger. This is the principle of superposition."}},
        {"type": "trace", "title": "Layer B", "structure": "B", "instruction": "Trace layer B, on both sides.",
         "note": {"text": "Each layer records a time. A change in rock type means the place changed, like a sea becoming a muddy shore."}},
        {"type": "trace", "title": "Dike", "structure": "dike", "instruction": "Trace the dark band cutting up through the layers.",
         "note": {"text": "A dike is magma that forced its way up through cracks and cooled. It cuts layers B, C and D, so it's younger than them.",
                  "remember": "What cuts across is younger."}},
        {"type": "trace", "title": "Layer A", "structure": "A", "instruction": "Trace the top layer.",
         "note": {"text": "Layer A lies over the top of the dike without being cut, so it formed after the dike."}},
        {"type": "trace", "title": "Fossils", "structure": "fossils", "instruction": "Trace the two shell fossils in layer C.",
         "note": {"text": "Fossils are dated by the layer they're in. These shells lived while layer C was forming, before B and A."}},
        {"type": "color", "title": "Color", "structures": ["D", "C", "B", "dike", "A"], "instruction": "Color each rock."},
        {"type": "order", "title": "Tell the story", "instruction": "Tap the events from oldest to youngest.",
         "items": ["Layer D is deposited", "Layer C is deposited, with shells", "Layer B is deposited", "Magma cuts through as a dike",
                   "Layer A is deposited on top"],
         "why": "Lower layers are older (superposition), and the dike is younger than the layers it cuts (cross-cutting).",
         "hint": "Start at the bottom."},
        {"type": "choice", "title": "Evidence", "instruction": "Use the layers.", "showsDiagram": True,
         "question": "How do we know the dike is older than layer A?",
         "options": [
             {"text": "The dike stops at layer A instead of cutting through it", "correct": True,
              "feedback": "Yes. Layer A was laid on top after the dike cooled. If the dike were younger, it would cut A too."},
             {"text": "The dike is darker", "feedback": "Color doesn't show age. What matters is which rock cuts across which."},
             {"text": "The dike is lower down", "feedback": "The dike reaches up through B. What shows it's older than A is that it doesn't cut A."},
             {"text": "We can't tell", "feedback": "We can: the dike ends under layer A, so A formed after it."}]},
        {"type": "choice", "title": "Time scale", "instruction": "Think about Earth's whole history.", "showsDiagram": False,
         "question": "How do geologists build the geologic time scale of Earth's 4.6-billion-year history?",
         "options": [
             {"text": "By matching the order of rock layers and the fossils in them from place to place", "correct": True,
              "feedback": "Right. Layers and fossils show which events came first, so Earth's history can be put in order and divided into eras."},
             {"text": "By counting every year since Earth formed", "feedback": "No one could count that. The order of layers and fossils puts events in sequence."},
             {"text": "From written records", "feedback": "People have written for only a few thousand years. Rocks record far older events."},
             {"text": "By measuring how tall mountains are", "feedback": "Height doesn't give an order of events. Layers and fossils do."}]},
    ],
}

# ---------------------------------------------------------------- The rock cycle
NODES = [("magma", "Magma", 500, 190), ("igneous", "Igneous rock", 812, 420), ("sediment", "Sediment", 700, 780),
         ("sedimentary", "Sedimentary rock", 300, 780), ("metamorphic", "Metamorphic rock", 188, 420)]
NW, NH = 180, 100


def link(a, b, trim=118):
    (_, _, x0, y0), (_, _, x1, y1) = a, b
    d = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / d, (y1 - y0) / d
    return straight_arrow(r(x0 + ux * trim), r(y0 + uy * trim), r(x1 - ux * trim), r(y1 - uy * trim), head=22)


arrows = [link(NODES[k], NODES[(k + 1) % 5]) for k in range(5)]
rock_cycle = {
    "id": "g6-rock-cycle", "title": "The rock cycle", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS2-1", "minutes": 10,
    "sources": [ngss("MS-ESS2-1", "Develop a model to describe the cycling of Earth's materials and the flow of energy that drives this process"),
                geo("3.1", "3-1-the-rock-cycle", "The Rock Cycle"), geo("1.5", "1-5-fundamentals-of-plate-tectonics", "Fundamentals of Plate Tectonics")],
    "keywords": ["rock cycle", "igneous", "sedimentary", "metamorphic", "magma", "sediment", "weathering", "erosion",
                 "melting", "crystallization", "heat", "pressure", "energy"],
    "printed": [{"text": "Cooling", "at": [720, 255], "size": 28},
                {"text": "Weathering,", "at": [880, 590], "size": 26}, {"text": "erosion", "at": [880, 620], "size": 26},
                {"text": "Burial, cementing", "at": [500, 860], "size": 26},
                {"text": "Heat and", "at": [118, 590], "size": 26}, {"text": "pressure", "at": [118, 620], "size": 26},
                {"text": "Melting", "at": [280, 255], "size": 28}],
    "structures": [{"id": i, "name": n.lower(), "outlines": [{"rect": [x - NW / 2, y - NH / 2, NW, NH, 18]}]} for i, n, x, y in NODES] + [
        {"id": "arrows", "name": "cycle arrows", "pen": "bold", "outlines": [s for a in arrows for s in a]},
    ],
    "steps": [
        {"type": "trace", "title": "Magma", "structure": "magma", "instruction": "Trace the box at the top.",
         "note": {"text": "Magma is rock so hot it's completely melted: about 800 to 1300 °C.", "remember": "Magma = melted rock."}},
        {"type": "trace", "title": "Igneous rock", "structure": "igneous", "instruction": "Trace the box on the right.",
         "note": {"text": "When magma cools and crystallizes, it becomes igneous rock: slowly underground, or fast if it erupts as lava."}},
        {"type": "trace", "title": "Sediment", "structure": "sediment", "instruction": "Trace the box at the bottom right.",
         "note": {"text": "Rock lifted to the surface is weathered into bits, which water, ice and wind carry away and drop as sediment."}},
        {"type": "trace", "title": "Sedimentary rock", "structure": "sedimentary", "instruction": "Trace the box at the bottom left.",
         "note": {"text": "Buried under more sediment, the bits are squeezed and cemented together into sedimentary rock."}},
        {"type": "trace", "title": "Metamorphic rock", "structure": "metamorphic", "instruction": "Trace the box on the left.",
         "note": {"text": "Rock buried deeper is heated and squeezed until it changes, without melting, into metamorphic rock."}},
        {"type": "trace", "title": "The cycle", "structure": "arrows", "instruction": "Draw the five arrows around the cycle.",
         "note": {"text": "If metamorphic rock gets hot enough, it melts back into magma, and the cycle goes on for millions of years.",
                  "remember": "Rock is always being recycled."}},
        {"type": "label", "title": "Name the stages", "instruction": "Pick the name for each numbered box.",
         "targets": [
             {"n": 1, "at": [500, 190], "answer": "Magma", "role": "Melted rock."},
             {"n": 2, "at": [812, 420], "answer": "Igneous rock", "role": "Formed when magma cools.",
              "mistakes": {"Metamorphic rock": "Metamorphic rock forms from heat and pressure. Rock made by cooling magma is igneous."}},
             {"n": 3, "at": [700, 780], "answer": "Sediment", "role": "Bits of weathered rock."},
             {"n": 4, "at": [300, 780], "answer": "Sedimentary rock", "role": "Sediment cemented together.",
              "mistakes": {"Igneous rock": "This rock forms from buried, cemented sediment, so it's sedimentary."}},
             {"n": 5, "at": [188, 420], "answer": "Metamorphic rock", "role": "Changed by heat and pressure."}],
         "vocabulary": ["Magma", "Igneous rock", "Sediment", "Sedimentary rock", "Metamorphic rock", "Lava"]},
        {"type": "choice", "title": "Energy", "instruction": "Think about what powers each part.", "showsDiagram": True,
         "question": "What two energy sources drive the rock cycle?",
         "options": [
             {"text": "Earth's internal heat, and the sun powering water, ice and wind", "correct": True,
              "feedback": "Yes. Inner heat melts and changes rock deep down; the sun drives the weathering and erosion at the surface."},
             {"text": "Only the sun", "feedback": "The sun drives weathering and erosion, but melting and metamorphism come from Earth's internal heat."},
             {"text": "Only Earth's internal heat", "feedback": "Internal heat works deep down. Weathering by water and wind is powered by the sun."},
             {"text": "The moon's gravity", "feedback": "The two drivers are Earth's internal heat and the sun's energy at the surface."}]},
        {"type": "choice", "title": "Shortcuts", "instruction": "Does every rock go all the way around?", "showsDiagram": True,
         "question": "Sedimentary rock is pushed up into a mountain. What can happen to it next?",
         "options": [
             {"text": "It's weathered into new sediment, skipping the rest of the loop", "correct": True,
              "feedback": "Right. Rocks don't have to make a full loop: any rock at the surface can be weathered into sediment."},
             {"text": "It must become metamorphic rock first", "feedback": "Not always. Uplifted rock at the surface can be weathered straight back into sediment."},
             {"text": "Nothing: rocks never change once formed", "feedback": "Rocks change all the time, just very slowly."},
             {"text": "It turns straight into magma at the surface", "feedback": "Surface rock isn't hot enough to melt. It gets weathered."}]},
    ],
}

# ---------------------------------------------------------------- A river delta
COAST = 715
fan = (330, COAST, 360, 820, 640, 820, 670, COAST)


def bez(t, p=fan):
    u = 1 - t
    return (r(u**3 * p[0] + 3 * u * u * t * p[2] + 3 * u * t * t * p[4] + t**3 * p[6]),
            r(u**3 * p[1] + 3 * u * u * t * p[3] + 3 * u * t * t * p[5] + t**3 * p[7]))


FAN_EDGE = f"C {fan[2]} {fan[3]} {fan[4]} {fan[5]} {fan[6]} {fan[7]}"
delta = {
    "id": "g6-river-delta", "title": "Erosion and deposition: a river delta", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS2-2", "minutes": 9, "colorMode": "illustration",
    "sources": [ngss("MS-ESS2-2", "Construct an explanation based on evidence for how geoscience processes have changed Earth's surface "
                                   "at varying time and spatial scales"),
                geo("13.3", "13-3-stream-erosion-and-deposition", "Stream Erosion and Deposition"),
                geo("13.4", "13-4-stream-types", "Stream Types (deltas)"), geo("3.1", "3-1-the-rock-cycle", "The Rock Cycle")],
    "keywords": ["erosion", "deposition", "delta", "river", "sediment", "weathering", "mountains", "ocean", "landforms",
                 "time scales"],
    "printed": [{"text": "Seen from above", "at": [840, 960], "size": 28}],
    "legend": [{"name": "Mountains", "color": "#8A8F98", "meaning": "Bare rock high up"},
               {"name": "Delta", "color": "#D9C28A", "meaning": "New land built of river sand and mud"},
               {"name": "Ocean", "color": "#3B7DD8", "meaning": "Still water where the river slows"}],
    "structures": [
        {"id": "mountains", "name": "mountains", "colorName": "mountains", "fill": "#8A8F98",
         "outlines": [{"polygon": [120, 250, 240, 90, 360, 250]}, {"polygon": [380, 250, 500, 70, 620, 250]},
                      {"polygon": [640, 250, 760, 110, 880, 250]}]},
        {"id": "river", "name": "river", "pen": "bold",
         "outlines": [{"path": "M 500 262 C 420 330 600 380 520 450 C 450 510 560 570 500 640"}]},
        {"id": "carry", "name": "sediment on the move", "outlines": straight_arrow(700, 300, 700, 600)},
        {"id": "ocean", "name": "ocean", "colorName": "ocean", "fill": "#3B7DD8",
         "outlines": [{"path": f"M 40 {COAST} L 330 {COAST} {FAN_EDGE} L 960 {COAST} L 960 940 L 40 940 Z"}]},
        {"id": "delta", "name": "delta", "colorName": "delta", "fill": "#D9C28A",
         "outlines": [{"path": f"M 500 640 L 330 {COAST} {FAN_EDGE} Z"}],
         "details": [{"line": [500, 640, *bez(0.3)]}, {"line": [500, 640, *bez(0.5)]}, {"line": [500, 640, *bez(0.7)]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Mountains", "structure": "mountains", "instruction": "Trace the three mountains.",
         "note": {"text": "Rock high in the mountains is weathered: broken into pieces by ice, water and plant roots."}},
        {"type": "trace", "title": "River", "structure": "river", "instruction": "Trace the river winding down from the mountains.",
         "note": {"text": "Fast-flowing water erodes: it picks up rock pieces and carries them away. Faster water can carry bigger pieces.",
                  "remember": "Erosion = carrying rock away."}},
        {"type": "trace", "title": "Carrying sediment", "structure": "carry", "instruction": "Draw the arrow showing sediment moving downstream.",
         "note": {"text": "Sand and mud travel with the water, sometimes for hundreds of kilometres."}},
        {"type": "trace", "title": "Ocean", "structure": "ocean", "instruction": "Trace the coastline and the ocean.",
         "note": {"text": "Where the river meets still water, it slows down and can't carry its load any more."}},
        {"type": "trace", "title": "Delta", "structure": "delta", "instruction": "Trace the fan of land where the river meets the ocean.",
         "note": {"text": "The dropped sediment builds new land: a delta. Dropping sediment is called deposition.",
                  "remember": "Deposition = dropping sediment."}},
        {"type": "trace", "title": "Channels", "structure": "delta", "part": "details", "instruction": "Draw the three channels spreading across the delta.",
         "note": {"text": "The river splits into channels that spread sediment across the delta, making it grow out into the sea."}},
        {"type": "color", "title": "Color", "structures": ["mountains", "ocean", "delta"], "instruction": "Color the mountains, the ocean and the delta."},
        {"type": "choice", "title": "Explain", "instruction": "Use the model.", "showsDiagram": True,
         "question": "Why does the river drop its sediment at the coast?",
         "options": [
             {"text": "The water slows down when it enters the still ocean", "correct": True,
              "feedback": "Yes. Slower water can't hold up as much sediment, so the sand and mud settle out and build the delta."},
             {"text": "The water speeds up at the coast", "feedback": "It's the opposite: the river slows down, and slow water drops its sediment."},
             {"text": "Salt dissolves the sediment", "feedback": "Salt doesn't dissolve sand. The river slows down and drops it."},
             {"text": "The mountains pull it back", "feedback": "The sediment settles because the water slows down when it reaches the ocean."}]},
        {"type": "choice", "title": "Time scale", "instruction": "How fast do landforms change?", "showsDiagram": False,
         "question": "Most of the land on the Fraser River delta in Canada formed in the last 10,000 years. What does this show?",
         "options": [
             {"text": "Slow, steady deposition can build a lot of new land over thousands of years", "correct": True,
              "feedback": "Right. A little sediment each year adds up: whole towns now stand on land the river built."},
             {"text": "Deltas form in a single day", "feedback": "Deltas grow bit by bit. The Fraser delta took about 10,000 years."},
             {"text": "Rivers only erode, never build", "feedback": "Rivers do both: they erode upstream and deposit downstream, building deltas."},
             {"text": "Land never changes", "feedback": "This delta shows land changing a lot, slowly, over thousands of years."}]},
    ],
}

# ---------------------------------------------------------------- Plate boundaries
SLAB = (540, 470, 0.9375)  # the subducting plate's top surface: starts at (540, 470), slope 0.9375


def slab_y(x): return r(SLAB[1] + (x - SLAB[0]) * SLAB[2])


def slab_x(y): return r(SLAB[0] + (y - SLAB[1]) / SLAB[2])


continent = [560, slab_y(560), 600, 450, 690, 440, 725, 375, 760, 440, 960, 440, 960, 560, slab_x(560), 560]
plates = {
    "id": "g6-plate-boundaries", "title": "Plate boundaries", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS2-3", "minutes": 11,
    "sources": [ESS2_3, BOUNDARIES, geo("1.5", "1-5-fundamentals-of-plate-tectonics", "Fundamentals of Plate Tectonics")],
    "keywords": ["plate tectonics", "plate boundaries", "divergent", "convergent", "transform", "subduction", "trench",
                 "mid-ocean ridge", "volcano", "earthquake", "San Andreas Fault", "Andes"],
    "printed": [{"text": "1", "at": [40, 60], "size": 40}, {"text": "2", "at": [40, 380], "size": 40}, {"text": "3", "at": [40, 720], "size": 40},
                {"text": "Seen from above", "at": [800, 712], "size": 26}, {"text": "Not to scale", "at": [150, 620], "size": 26}],
    "structures": [
        {"id": "apart", "name": "plates pulling apart", "outlines": [{"polygon": [80, 200, 470, 150, 470, 210, 80, 260]},
                                                                    {"polygon": [920, 200, 530, 150, 530, 210, 920, 260]}],
         "details": straight_arrow(440, 100, 300, 100) + straight_arrow(560, 100, 700, 100)},
        {"id": "rise", "name": "rising magma", "pen": "bold", "outlines": straight_arrow(500, 310, 500, 175)},
        {"id": "ocean", "name": "ocean plate", "outlines": [{"polygon": [60, 470, 540, 470, 700, 620, 660, 650, 520, 520, 60, 520]}],
         "details": straight_arrow(200, 430, 400, 430)},
        {"id": "land", "name": "continent", "outlines": [{"polygon": continent}]},
        {"id": "melt", "name": "magma to the volcano", "pen": "bold", "outlines": straight_arrow(690, 600, 722, 395, head=22)},
        {"id": "slide", "name": "plates sliding past", "outlines": [{"rect": [80, 740, 840, 200]}, {"line": [80, 840, 920, 840]}],
         "details": straight_arrow(600, 790, 400, 790) + straight_arrow(400, 890, 600, 890)},
    ],
    "steps": [
        {"type": "trace", "title": "Two plates", "structure": "apart", "instruction": "Trace the two plates in picture 1.",
         "note": {"text": "Earth's outer shell is broken into about 20 plates that move a few centimetres a year."}},
        {"type": "trace", "title": "Moving apart", "structure": "apart", "part": "details", "instruction": "Draw the arrows showing the plates moving apart.",
         "note": {"text": "Here the plates spread apart. This is a divergent boundary.", "remember": "Divergent = apart."}},
        {"type": "trace", "title": "Rising magma", "structure": "rise", "instruction": "Draw the arrow of magma rising between them.",
         "note": {"text": "Hot rock rises and partly melts, making new ocean crust. Most divergent boundaries are mid-ocean ridges."}},
        {"type": "trace", "title": "Ocean plate", "structure": "ocean", "instruction": "Trace the ocean plate in picture 2, bending down under the land.",
         "note": {"text": "Here plates move together: a convergent boundary. The denser ocean plate sinks under the other. This is subduction.",
                  "remember": "Convergent = together."}},
        {"type": "trace", "title": "Moving in", "structure": "ocean", "part": "details", "instruction": "Draw the arrow showing the ocean plate moving.",
         "note": {"text": "A deep ocean trench forms where the plate bends down."}},
        {"type": "trace", "title": "Continent", "structure": "land", "instruction": "Trace the continent and its volcano.",
         "note": {"text": "The sinking plate releases water that helps melt rock, building a chain of volcanic mountains like the Andes."}},
        {"type": "trace", "title": "Magma", "structure": "melt", "instruction": "Draw the arrow of magma rising to the volcano.",
         "note": {"text": "Convergent boundaries have many of Earth's big earthquakes and volcanoes."}},
        {"type": "trace", "title": "Sliding plates", "structure": "slide", "instruction": "Trace picture 3, seen from above, and the boundary line across it.",
         "note": {"text": "Here plates slide past each other: a transform boundary. No crust is made or destroyed.",
                  "remember": "Transform = sliding past."}},
        {"type": "trace", "title": "Sliding past", "structure": "slide", "part": "details", "instruction": "Draw the two arrows pointing opposite ways.",
         "note": {"text": "The San Andreas Fault in California is a transform boundary. Plates sticking and slipping cause earthquakes."}},
        {"type": "label", "title": "Name the boundaries", "instruction": "Pick the type of boundary in each picture.",
         "targets": [
             {"n": 1, "at": [500, 200], "answer": "Divergent", "role": "Plates move apart.",
              "mistakes": {"Convergent": "The arrows point away from each other, so the plates move apart: divergent."}},
             {"n": 2, "at": [560, 500], "answer": "Convergent", "role": "Plates move together.",
              "mistakes": {"Divergent": "One plate sinks under the other here, so they're moving together: convergent."}},
             {"n": 3, "at": [500, 840], "answer": "Transform", "role": "Plates slide past."}],
         "vocabulary": ["Divergent", "Convergent", "Transform"]},
        {"type": "choice", "title": "Evidence", "instruction": "Use the pictures.", "showsDiagram": True,
         "question": "Scientists find a deep trench beside a line of volcanoes. What does this tell them?",
         "options": [
             {"text": "Two plates are coming together, and one is sinking under the other", "correct": True,
              "feedback": "Yes. A trench and a chain of volcanoes are evidence of a convergent boundary, like the one in picture 2."},
             {"text": "The plates are pulling apart", "feedback": "Spreading plates make a ridge with new crust, not a trench beside volcanoes."},
             {"text": "The plates are sliding past each other", "feedback": "Transform boundaries don't make trenches or volcanic chains."},
             {"text": "The plates aren't moving", "feedback": "Trenches and volcanoes form because plates move: here, one sinks under another."}]},
        {"type": "choice", "title": "New crust", "instruction": "Compare the three boundaries.", "showsDiagram": True,
         "question": "At which boundary is new ocean crust made?",
         "options": [
             {"text": "Divergent", "correct": True, "feedback": "Right. Magma rises between the separating plates and cools into new crust."},
             {"text": "Convergent", "feedback": "At convergent boundaries crust sinks and is destroyed. New crust forms where plates pull apart."},
             {"text": "Transform", "feedback": "Transform boundaries neither make nor destroy crust."},
             {"text": "All of them", "feedback": "Only divergent boundaries make new crust."}]},
    ],
}

# ---------------------------------------------------------------- Pangaea and continental drift
SHIFT = 150  # South America's east coast is Africa's west coast moved this far left: they'd fit together
africa_coast = [(520, 290), (560, 330), (630, 360), (640, 450), (645, 560), (660, 680), (690, 800), (720, 860)]
sa_coast = [(x - SHIFT, y) for x, y in africa_coast]
africa = [(560, 125), (480, 185), (465, 245)] + africa_coast + [(760, 880), (800, 800), (860, 660), (890, 540), (935, 420),
                                                     (970, 340), (890, 290), (870, 200), (820, 130), (700, 110)]
south_america = [(150, 260), (270, 240)] + sa_coast + [(560, 900), (500, 905), (430, 830), (340, 700), (250, 560), (170, 430), (125, 330)]
ridge = [c for x, y in africa_coast[1:] for c in (x - SHIFT / 2, y)]


def flat(pts): return [c for p in pts for c in p]


def band(coast_x0, coast_x1, side, y0, y1, w=110, inset=12):
    """A zone of fossils against a coast, from y0 to y1, on one side (-1 = west of the coast, +1 = east)."""
    a, b = coast_x0 + side * inset, coast_x1 + side * inset
    return {"polygon": [a, y0, a + side * w, y0, b + side * w, y1, b, y1]}


def coast_x(pts, y):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if y0 <= y <= y1: return r(x0 + (x1 - x0) * (y - y0) / (y1 - y0))


Y0, Y1 = 560, 660
pangaea = {
    "id": "g6-pangaea", "title": "Pangaea and continental drift", "grade": "6", "subject": "Earth & space",
    "standard": "MS-ESS2-3", "minutes": 10, "colorMode": "illustration",
    "sources": [ESS2_3, geo("10.1", "10-1-alfred-wegener-the-father-of-plate-tectonics", "Alfred Wegener: The Father of Plate Tectonics"),
                BOUNDARIES],
    "keywords": ["Pangaea", "Pangea", "continental drift", "Wegener", "fossils", "Mesosaurus", "South America", "Africa",
                 "Atlantic Ocean", "mid-ocean ridge", "plate tectonics", "evidence"],
    "printed": [{"text": "Today", "at": [500, 960], "size": 30}],
    "legend": [{"name": "Mesosaurus fossils", "color": "#5E9E6E", "meaning": "Where the reptile's fossils are found"}],
    "structures": [
        {"id": "sa", "name": "South America", "pen": "bold", "outlines": [{"polygon": flat(south_america)}]},
        {"id": "af", "name": "Africa", "pen": "bold", "outlines": [{"polygon": flat(africa)}]},
        {"id": "fossils", "name": "Mesosaurus fossils", "colorName": "Mesosaurus fossils", "fill": "#5E9E6E",
         "outlines": [band(coast_x(sa_coast, Y0), coast_x(sa_coast, Y1), -1, Y0, Y1),
                      band(coast_x(africa_coast, Y0), coast_x(africa_coast, Y1), 1, Y0, Y1)]},
        {"id": "ridge", "name": "Mid-Atlantic Ridge", "pen": "fine", "outlines": [{"line": ridge}]},
        {"id": "drift", "name": "spreading", "outlines": straight_arrow(480, 70, 340, 70) + straight_arrow(560, 70, 700, 70)},
    ],
    "steps": [
        {"type": "trace", "title": "South America", "structure": "sa", "instruction": "Trace South America.",
         "note": {"text": "Look at South America's east coast, with its bulge sticking out into the Atlantic."}},
        {"type": "trace", "title": "Africa", "structure": "af", "instruction": "Trace Africa.",
         "note": {"text": "Africa's west coast curves in where South America's bulges out, like puzzle pieces.",
                  "remember": "The coasts fit together."}},
        {"type": "trace", "title": "Fossils", "structure": "fossils", "instruction": "Trace the two areas where Mesosaurus fossils are found.",
         "note": {"text": "Mesosaurus was a small freshwater reptile. Its fossils are found in both South America and Africa, but it couldn't cross an ocean."}},
        {"type": "trace", "title": "Ridge", "structure": "ridge", "instruction": "Trace the ridge down the middle of the Atlantic.",
         "note": {"text": "Down the middle of the ocean runs a ridge where plates pull apart and new sea floor forms.",
                  "remember": "The Atlantic is widening."}},
        {"type": "trace", "title": "Moving apart", "structure": "drift", "instruction": "Draw the arrows showing the continents moving apart.",
         "note": {"text": "The continents still drift apart, about 2.5 cm a year: roughly as fast as your fingernails grow."}},
        {"type": "color", "title": "Color", "structures": ["fossils"], "instruction": "Color the fossil areas."},
        {"type": "choice", "title": "Explain the fossils", "instruction": "Use the evidence.", "showsDiagram": True,
         "question": "How did the same freshwater reptile end up on two continents an ocean apart?",
         "options": [
             {"text": "The continents were joined when it lived, and later drifted apart", "correct": True,
              "feedback": "Yes. Alfred Wegener used fossils like these as evidence for a supercontinent, which he named Pangaea (also spelled Pangea)."},
             {"text": "It swam across the Atlantic", "feedback": "Mesosaurus lived in fresh water and couldn't cross a whole ocean."},
             {"text": "Two different animals evolved to look the same", "feedback": "The fossils match, and so do the rocks around them. The simpler answer: the land was joined."},
             {"text": "People carried the fossils", "feedback": "The fossils are buried in rock millions of years old, long before people."}]},
        {"type": "choice", "title": "More evidence", "instruction": "What else would support drift?", "showsDiagram": False,
         "question": "Which other finding supports the idea that the continents were once joined?",
         "options": [
             {"text": "Matching rock layers on the two coasts", "correct": True,
              "feedback": "Right. Wegener found rock layers in Brazil matching those in Africa, and mountains in Canada matching ones in Britain."},
             {"text": "Both continents have rivers", "feedback": "Every continent has rivers, so that's no evidence they were joined."},
             {"text": "Both have hot weather", "feedback": "Weather changes over time and doesn't show the land was joined."},
             {"text": "Both have people", "feedback": "People came much later. Matching rocks and fossils are the evidence."}]},
        {"type": "choice", "title": "The missing piece", "instruction": "Wegener's idea had a problem.", "showsDiagram": False,
         "question": "Why did most geologists reject Wegener's idea at first, around 1912?",
         "options": [
             {"text": "He couldn't explain what force could move whole continents", "correct": True,
              "feedback": "Yes. Decades later, sea-floor spreading and plate tectonics supplied the mechanism, and his idea was accepted."},
             {"text": "The coasts didn't fit at all", "feedback": "The fit was striking. The real problem was that he had no mechanism for the movement."},
             {"text": "No fossils had been found", "feedback": "He used fossils as evidence. What he lacked was a force to move the continents."},
             {"text": "Maps hadn't been made yet", "feedback": "Good maps existed. The missing piece was a force to move continents."}]},
    ],
}

for lesson in (rock_layers, rock_cycle, delta, plates, pangaea):
    save(lesson)
