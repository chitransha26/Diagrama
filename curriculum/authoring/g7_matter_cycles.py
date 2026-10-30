"""Grade 7 · photosynthesis in a leaf (MS-LS1-6), cellular respiration (MS-LS1-7), clownfish and anemone (MS-LS2-2), and
the carbon and nitrogen cycles (MS-LS2-3).

Facts checked against OpenStax Biology 2e (4.3, 6.1, 22.3, 22.5, 24.3, 28.2, 30.2, 30.4, 45.6, 46.1, 46.3), searched with
curriculum/tools/openstax.py, and for the clownfish, NOAA's Fagatele Bay sanctuary and National Geographic.
"""
from lib import save, straight_arrow, mirror_path


def bio(section, slug, title):
    return {"title": f"OpenStax Biology 2e, {section} {title}", "url": f"https://openstax.org/books/biology-2e/pages/{slug}"}


def rrect(x, y, w, h, rad):
    return {"rect": [x, y, w, h, rad]}


LS1_6 = {"title": "NGSS MS-LS1-6: Construct a scientific explanation based on evidence for the role of photosynthesis in the "
                  "cycling of matter and flow of energy into and out of organisms"}
LS1_7 = {"title": "NGSS MS-LS1-7: Develop a model to describe how food is rearranged through chemical reactions forming new "
                  "molecules that support growth and/or release energy as this matter moves through an organism"}
LS2_2 = {"title": "NGSS MS-LS2-2: Construct an explanation that predicts patterns of interactions among organisms across "
                  "multiple ecosystems"}
LS2_3 = {"title": "NGSS MS-LS2-3: Develop a model to describe the cycling of matter and flow of energy among living and "
                  "nonliving parts of an ecosystem"}
ENERGY = bio("6.1", "6-1-energy-and-metabolism", "Energy and Metabolism")
CYCLES = bio("46.3", "46-3-biogeochemical-cycles", "Biogeochemical Cycles")
PROKARYOTES = bio("22.3", "22-3-prokaryotic-metabolism", "Prokaryotic Metabolism")


def arrows(*specs, head=24):
    out = []
    for s in specs:
        out += straight_arrow(*s, head=head)
    return out


# ---------------------------------------------------------------- Photosynthesis in a leaf
LEAF = "M 330 780 C 380 520 600 260 880 200 C 860 470 620 760 330 780 Z"
GREEN = "#6BA368"
photo = {
    "id": "g7-photosynthesis", "title": "Photosynthesis in a leaf", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-6", "minutes": 9, "colorMode": "illustration",
    "sources": [LS1_6, ENERGY, bio("30.2", "30-2-stems", "Stems (stomata take in carbon dioxide)"),
                bio("30.4", "30-4-leaves", "Leaves (chloroplasts in the mesophyll)")],
    "keywords": ["photosynthesis", "leaf", "chloroplast", "chlorophyll", "sunlight", "carbon dioxide", "water", "sugar",
                 "glucose", "oxygen", "stomata", "producer", "energy", "matter"],
    "legend": [{"name": "Leaf", "color": GREEN, "meaning": "Green from chlorophyll, which captures light"}],
    "structures": [
        {"id": "sun", "name": "sun", "outlines": [{"circle": [130, 130, 70]}]},
        {"id": "light", "name": "sunlight", "pen": "bold", "outlines": arrows((215, 215, 420, 420), head=34)},
        {"id": "leaf", "name": "leaf", "colorName": "leaf", "fill": GREEN, "pen": "bold", "outlines": [{"path": LEAF}],
         "details": [{"path": "M 360 750 C 500 570 680 380 845 232"}]},
        {"id": "stem", "name": "stem", "pen": "bold", "outlines": [{"line": [330, 780, 240, 930]}]},
        {"id": "water", "name": "water in", "outlines": arrows((193, 892, 274, 757))},
        {"id": "co2", "name": "carbon dioxide in", "outlines": arrows((900, 760, 760, 640))},
        {"id": "o2", "name": "oxygen out", "outlines": arrows((640, 720, 760, 870))},
        {"id": "sugar", "name": "sugar out", "outlines": arrows((377, 818, 296, 953))},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "Almost all the energy in living things started as sunlight."}},
        {"type": "trace", "title": "Light", "structure": "light", "instruction": "Draw the arrow of sunlight reaching the leaf.",
         "note": {"text": "Light is the energy input for photosynthesis.", "remember": "Energy in: light."}},
        {"type": "trace", "title": "Leaf", "structure": "leaf", "instruction": "Trace the leaf.",
         "note": {"text": "Leaf cells are packed with chloroplasts. Their green chlorophyll captures light energy."}},
        {"type": "trace", "title": "Vein", "structure": "leaf", "part": "details", "instruction": "Draw the main vein down the middle.",
         "note": {"text": "Veins carry water into the leaf and carry sugar out to the rest of the plant."}},
        {"type": "trace", "title": "Stem", "structure": "stem", "instruction": "Trace the leaf's stalk.", "note": {"text": "The stalk joins the leaf to the plant."}},
        {"type": "trace", "title": "Water in", "structure": "water", "instruction": "Draw the arrow of water coming up from the roots.",
         "note": {"text": "Roots take in water, which travels up the stem to the leaf."}},
        {"type": "trace", "title": "Carbon dioxide in", "structure": "co2", "instruction": "Draw the arrow of carbon dioxide going into the leaf.",
         "note": {"text": "Carbon dioxide from the air enters through tiny openings under the leaf, called stomata."}},
        {"type": "trace", "title": "Oxygen out", "structure": "o2", "instruction": "Draw the arrow of oxygen leaving the leaf.",
         "note": {"text": "Oxygen is given off as a waste product. It leaves through the stomata too.", "remember": "Stomata: gases in and out."}},
        {"type": "trace", "title": "Sugar out", "structure": "sugar", "instruction": "Draw the arrow of sugar going to the rest of the plant.",
         "note": {"text": "The sugar stores the light's energy. The plant uses it to live and to build new leaves, stems and roots.",
                  "remember": "Light energy is stored in sugar."}},
        {"type": "color", "title": "Color", "structures": ["leaf"], "instruction": "Color the leaf green."},
        {"type": "label", "title": "Inputs and outputs", "instruction": "Pick what each numbered arrow carries.",
         "targets": [
             {"n": 1, "at": [318, 318], "answer": "Light energy", "synonyms": ["Sunlight"], "role": "Energy input."},
             {"n": 2, "at": [233, 825], "answer": "Water", "role": "Comes from the roots."},
             {"n": 3, "at": [830, 700], "answer": "Carbon dioxide", "role": "Comes from the air.",
              "mistakes": {"Oxygen": "Oxygen leaves the leaf. Carbon dioxide is what goes in."}},
             {"n": 4, "at": [700, 795], "answer": "Oxygen", "role": "Given off."},
             {"n": 5, "at": [337, 886], "answer": "Sugar", "synonyms": ["Glucose"], "role": "Stores the energy."}],
         "vocabulary": ["Light energy", "Sunlight", "Water", "Carbon dioxide", "Oxygen", "Sugar", "Glucose", "Soil"]},
        {"type": "choice", "title": "Matter", "instruction": "Follow the atoms.", "showsDiagram": True,
         "question": "Where does the carbon in the leaf's sugar come from?",
         "options": [
             {"text": "Carbon dioxide from the air", "correct": True,
              "feedback": "Yes. Plants build sugar from carbon dioxide and water, so matter from the air becomes part of the plant."},
             {"text": "The soil", "feedback": "Roots take in water and minerals. The carbon comes from carbon dioxide in the air."},
             {"text": "Sunlight", "feedback": "Light gives energy, not matter. The carbon comes from carbon dioxide."},
             {"text": "Oxygen", "feedback": "Oxygen is given off. The carbon comes in as carbon dioxide."}]},
        {"type": "choice", "title": "Energy", "instruction": "Think about food chains.", "showsDiagram": False,
         "question": "A rabbit eats this leaf. Where did the energy in the rabbit's meal first come from?",
         "options": [
             {"text": "The sun: the plant stored light energy in sugar", "correct": True,
              "feedback": "Right. Photosynthesis brings energy into living things, and it passes along when animals eat plants."},
             {"text": "The soil", "feedback": "Soil gives minerals and holds water. The energy came from sunlight."},
             {"text": "The water", "feedback": "Water is an input, but the energy came from light, stored in sugar."},
             {"text": "The rabbit makes it", "feedback": "Animals can't make food from light. The energy came from the sun through the plant."}]},
    ],
}

# ---------------------------------------------------------------- Cellular respiration
CRISTAE = "M 360 500 C 380 440 400 440 410 500 C 420 560 440 560 450 500 C 460 440 480 440 490 500 C 500 560 520 560 530 500 C 540 440 560 440 570 500 C 580 560 600 560 610 500 C 620 440 640 440 640 500"
respiration = {
    "id": "g7-cellular-respiration", "title": "Cellular respiration overview", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-7", "minutes": 9,
    "sources": [LS1_7, ENERGY, bio("4.3", "4-3-eukaryotic-cells", "Eukaryotic Cells (mitochondria)")],
    "keywords": ["cellular respiration", "mitochondria", "mitochondrion", "glucose", "sugar", "oxygen", "carbon dioxide",
                 "water", "energy", "ATP", "cell", "breathing"],
    "printed": [{"text": "A body cell", "at": [500, 120], "size": 26}],
    "structures": [
        {"id": "cell", "name": "cell", "pen": "bold", "outlines": [{"circle": [500, 500, 330]}]},
        {"id": "mito", "name": "mitochondrion", "pen": "bold", "outlines": [{"ellipse": [500, 500, 180, 100]}],
         "details": [{"path": CRISTAE}]},
        {"id": "glucose", "name": "sugar in", "outlines": arrows((90, 200, 330, 420))},
        {"id": "oxygen", "name": "oxygen in", "outlines": arrows((40, 600, 300, 560))},
        {"id": "co2", "name": "carbon dioxide out", "outlines": arrows((690, 420, 950, 300))},
        {"id": "water", "name": "water out", "outlines": arrows((690, 590, 940, 720))},
        {"id": "energy", "name": "energy", "pen": "bold", "outlines": arrows((500, 620, 500, 960), head=34)},
    ],
    "steps": [
        {"type": "trace", "title": "Cell", "structure": "cell", "instruction": "Trace the body cell.",
         "note": {"text": "Every cell needs a steady supply of energy to stay alive and do its job."}},
        {"type": "trace", "title": "Mitochondrion", "structure": "mito", "instruction": "Trace the mitochondrion in the middle.",
         "note": {"text": "Mitochondria are where most of the cell's energy is released from food.", "remember": "Mitochondria: release energy."}},
        {"type": "trace", "title": "Folds", "structure": "mito", "part": "details", "instruction": "Draw the folded inner membrane.",
         "note": {"text": "The folds give lots of surface for the reactions."}},
        {"type": "trace", "title": "Sugar in", "structure": "glucose", "instruction": "Draw the arrow of sugar coming in.",
         "note": {"text": "Sugar, called glucose, comes from digested food and is carried to the cell in the blood."}},
        {"type": "trace", "title": "Oxygen in", "structure": "oxygen", "instruction": "Draw the arrow of oxygen coming in.",
         "note": {"text": "Oxygen comes from the lungs, also carried in the blood."}},
        {"type": "trace", "title": "Carbon dioxide out", "structure": "co2", "instruction": "Draw the arrow of carbon dioxide leaving.",
         "note": {"text": "The sugar's atoms are rearranged into carbon dioxide and water. The carbon dioxide you breathe out comes from this.",
                  "remember": "Sugar + oxygen → carbon dioxide + water."}},
        {"type": "trace", "title": "Water out", "structure": "water", "instruction": "Draw the arrow of water leaving.",
         "note": {"text": "Water is made too. No atoms are lost: they're only rearranged into new molecules."}},
        {"type": "trace", "title": "Energy", "structure": "energy", "instruction": "Draw the big arrow of energy released.",
         "note": {"text": "The energy stored in the sugar is released, mostly as ATP, the cell's energy carrier, and some as heat.",
                  "remember": "Energy out: ATP."}},
        {"type": "label", "title": "Inputs and outputs", "instruction": "Pick what each numbered arrow carries.",
         "targets": [
             {"n": 1, "at": [210, 310], "answer": "Sugar", "synonyms": ["Glucose"], "role": "Input from food."},
             {"n": 2, "at": [170, 580], "answer": "Oxygen", "role": "Input from the lungs.",
              "mistakes": {"Carbon dioxide": "Carbon dioxide leaves the cell. Oxygen comes in."}},
             {"n": 3, "at": [820, 360], "answer": "Carbon dioxide", "role": "Breathed out."},
             {"n": 4, "at": [815, 655], "answer": "Water", "role": "Also made."},
             {"n": 5, "at": [500, 790], "answer": "Energy", "synonyms": ["ATP"], "role": "What the cell needs."}],
         "vocabulary": ["Sugar", "Glucose", "Oxygen", "Carbon dioxide", "Water", "Energy", "ATP", "Sunlight"]},
        {"type": "choice", "title": "Compare", "instruction": "Think about photosynthesis.", "showsDiagram": True,
         "question": "How is cellular respiration related to photosynthesis?",
         "options": [
             {"text": "It runs the other way: photosynthesis makes sugar and oxygen, respiration uses them", "correct": True,
              "feedback": "Yes. Photosynthesis stores energy in sugar; respiration releases it. Their inputs and outputs swap."},
             {"text": "They're the same process", "feedback": "Look at the arrows. Respiration's inputs are photosynthesis's outputs."},
             {"text": "Only plants do respiration", "feedback": "All living cells do respiration, including plant cells and yours."},
             {"text": "Respiration makes sugar", "feedback": "It breaks sugar down. Photosynthesis makes sugar."}]},
        {"type": "choice", "title": "Exercise", "instruction": "Use the model.", "showsDiagram": True,
         "question": "When you run, why do you breathe faster?",
         "options": [
             {"text": "Muscle cells need more energy, so they use more oxygen and make more carbon dioxide", "correct": True,
              "feedback": "Right. Faster breathing brings in oxygen and removes carbon dioxide from working muscle cells."},
             {"text": "To cool the lungs", "feedback": "Breathing faster supplies oxygen for respiration in the muscles."},
             {"text": "Muscles make oxygen", "feedback": "Muscles use oxygen. Respiration in muscle cells needs more of it."},
             {"text": "To get more sugar", "feedback": "Sugar comes from food in the blood. Breathing brings in oxygen."}]},
    ],
}

# ---------------------------------------------------------------- Symbiosis: clownfish and anemone
COLUMN = "M 390 880 C 400 760 380 650 370 590 L 630 590 C 620 650 600 760 610 880 Z"
tentacles = [{"path": f"M {x} 586 C {x - 10} 520 {x + 30} 470 {x + 10 + (x - 500) // 3} {400 - abs(x - 500) // 4}"}
             for x in range(385, 640, 40)]
CLOWN = "M 680 470 C 700 420 800 410 840 460 L 890 425 L 890 515 L 840 480 C 800 530 700 520 680 470 Z"
BUTTERFLY = "M 760 170 C 760 100 880 100 900 160 L 950 130 L 950 210 L 900 180 C 880 240 760 240 760 170 Z"
ORANGE = "#F08A24"
symbiosis = {
    "id": "g7-symbiosis", "title": "Symbiosis: clownfish and anemone", "grade": "7", "subject": "Life science",
    "standard": "MS-LS2-2", "minutes": 9, "colorMode": "illustration",
    "sources": [LS2_2, bio("45.6", "45-6-community-ecology", "Community Ecology (symbiosis and parasitism)"),
                bio("24.3", "24-3-ecology-of-fungi", "Ecology of Fungi (mutualism and commensalism)"),
                bio("28.2", "28-2-phylum-cnidaria", "Phylum Cnidaria (stinging cells)"),
                {"title": "NOAA Fagatele Bay National Marine Sanctuary, Clownfish and Sea Anemone",
                 "url": "https://sanctuaries.noaa.gov/pgallery/pgfagatele/living/living_03_100.html"},
                {"title": "National Geographic, Beautiful Friendship (clownfish and anemones)",
                 "url": "https://www.nationalgeographic.com/magazine/article/clownfish-anemone-symbiotic-relationship"}],
    "keywords": ["symbiosis", "mutualism", "commensalism", "parasitism", "clownfish", "anemonefish", "sea anemone",
                 "stinging cells", "coral reef", "butterflyfish", "interactions"],
    "printed": [{"text": "Butterflyfish", "at": [855, 75], "size": 24}],
    "legend": [{"name": "Clownfish", "color": ORANGE, "meaning": "Orange with white stripes"}],
    "structures": [
        {"id": "column", "name": "anemone's body", "pen": "bold", "outlines": [{"path": COLUMN}]},
        {"id": "tentacles", "name": "tentacles", "outlines": tentacles},
        {"id": "clownfish", "name": "clownfish", "colorName": "clownfish", "fill": ORANGE, "pen": "bold", "outlines": [{"path": CLOWN}],
         "details": [{"path": "M 730 432 C 715 455 715 485 730 510"}, {"path": "M 800 428 C 785 455 785 485 800 508"}]},
        {"id": "butterfly", "name": "butterflyfish", "outlines": [{"path": BUTTERFLY}]},
        {"id": "chase", "name": "chasing it away", "pen": "fine", "outlines": arrows((760, 400, 800, 250))},
        {"id": "floor", "name": "reef floor", "pen": "fine", "outlines": [{"line": [100, 905, 900, 905]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Anemone", "structure": "column", "instruction": "Trace the sea anemone's body.",
         "note": {"text": "A sea anemone is an animal related to jellyfish. It clings to the reef and stays in one place."}},
        {"type": "trace", "title": "Tentacles", "structure": "tentacles", "instruction": "Trace the tentacles.",
         "note": {"text": "Its tentacles are covered in stinging cells that catch prey and drive off predators.",
                  "remember": "Tentacles sting."}},
        {"type": "trace", "title": "Clownfish", "structure": "clownfish", "instruction": "Trace the clownfish.",
         "note": {"text": "A slimy mucus coat keeps the anemone from stinging the clownfish, so it can hide among the tentacles."}},
        {"type": "trace", "title": "Stripes", "structure": "clownfish", "part": "details", "instruction": "Draw its two stripes.",
         "note": {"text": "The anemone's stings protect the clownfish and its eggs from fish that would eat them."}},
        {"type": "trace", "title": "Butterflyfish", "structure": "butterfly", "instruction": "Trace the butterflyfish.",
         "note": {"text": "Butterflyfish eat anemones."}},
        {"type": "trace", "title": "Defense", "structure": "chase", "instruction": "Draw the arrow of the clownfish chasing it.",
         "note": {"text": "The clownfish chases off anemone-eating fish. It also cleans algae off its anemone.",
                  "remember": "Both partners benefit."}},
        {"type": "trace", "title": "Reef", "structure": "floor", "instruction": "Draw the reef floor.",
         "note": {"text": "This partnership is found on coral reefs in warm, shallow seas."}},
        {"type": "color", "title": "Color", "structures": ["clownfish"], "instruction": "Color the clownfish orange, leaving the stripes white."},
        {"type": "choice", "title": "Kind of symbiosis", "instruction": "Compare the partners.", "showsDiagram": True,
         "question": "Both the clownfish and the anemone benefit. What kind of symbiosis is this?",
         "options": [
             {"text": "Mutualism", "correct": True, "feedback": "Yes. In mutualism, both partners benefit."},
             {"text": "Commensalism", "feedback": "In commensalism one partner benefits and the other isn't affected. Here both benefit."},
             {"text": "Parasitism", "feedback": "A parasite harms its host. Neither partner is harmed here."},
             {"text": "Predation", "feedback": "Neither one eats the other. They help each other."}]},
        {"type": "choice", "title": "Parasitism", "instruction": "Compare with another pair.", "showsDiagram": False,
         "question": "A tick feeds on a deer's blood, weakening the deer. What kind of relationship is that?",
         "options": [
             {"text": "Parasitism: the tick benefits and the deer is harmed", "correct": True,
              "feedback": "Right. A parasite lives on or in a host and takes nutrients from it."},
             {"text": "Mutualism", "feedback": "The deer doesn't benefit. It's harmed, so this is parasitism."},
             {"text": "Commensalism", "feedback": "In commensalism the other partner isn't affected. The deer is harmed."},
             {"text": "Competition", "feedback": "They aren't competing for a resource. The tick feeds on the deer: parasitism."}]},
        {"type": "choice", "title": "Predict", "instruction": "Use the model.", "showsDiagram": True,
         "question": "Divers remove all the clownfish from a reef. What would you predict for the anemones?",
         "options": [
             {"text": "More of them get eaten by butterflyfish", "correct": True,
              "feedback": "Yes. Without clownfish chasing them off, anemone-eating fish can feed more easily."},
             {"text": "Nothing changes", "feedback": "The clownfish defended the anemones. Losing them leaves the anemones less protected."},
             {"text": "The anemones swim away", "feedback": "Anemones mostly stay put. They'd be less protected from predators."},
             {"text": "The anemones grow stripes", "feedback": "Anemones can't do that. Without defenders, more would be eaten."}]},
    ],
}

# ---------------------------------------------------------------- The carbon cycle
TREE_TOP = {"circle": [190, 390, 100]}
carbon = {
    "id": "g7-carbon-cycle", "title": "The carbon cycle", "grade": "7", "subject": "Life science", "standard": "MS-LS2-3",
    "minutes": 10,
    "sources": [LS2_3, CYCLES, PROKARYOTES, bio("46.1", "46-1-ecology-of-ecosystems", "Ecology of Ecosystems (fossil fuels)")],
    "keywords": ["carbon cycle", "carbon dioxide", "photosynthesis", "respiration", "decomposers", "fossil fuels",
                 "burning", "combustion", "ocean", "matter", "cycling"],
    "printed": [{"text": "Carbon dioxide in the air", "at": [500, 70], "size": 30}, {"text": "Fossil fuels", "at": [560, 940], "size": 24},
                {"text": "Ocean", "at": [880, 760], "size": 26}],
    "structures": [
        {"id": "tree", "name": "tree", "pen": "bold", "outlines": [TREE_TOP, rrect(170, 490, 40, 150, 6)]},
        {"id": "rabbit", "name": "rabbit", "outlines": [{"ellipse": [410, 605, 60, 34]}, {"circle": [478, 572, 24]},
                                                     {"line": [470, 550, 462, 500]}, {"line": [488, 550, 498, 502]}]},
        {"id": "mushroom", "name": "decomposers", "outlines": [{"path": "M 540 590 C 545 545 615 545 620 590 Z"}, rrect(568, 592, 24, 46, 6)]},
        {"id": "factory", "name": "power plant", "pen": "bold", "outlines": [rrect(650, 470, 60, 170, 4)]},
        {"id": "ground", "name": "ground and fossil fuels", "pen": "fine",
         "outlines": [{"line": [40, 640, 740, 640]}, rrect(410, 830, 300, 70, 30), {"line": [680, 830, 680, 650]}]},
        {"id": "ocean", "name": "ocean", "pen": "fine", "outlines": [{"path": "M 770 660 C 800 640 830 640 860 660 C 890 680 920 680 960 660"}]},
        {"id": "photo", "name": "photosynthesis", "outlines": arrows((90, 140, 120, 300))},
        {"id": "resp", "name": "respiration", "outlines": arrows((260, 300, 300, 140)) + arrows((440, 520, 460, 140))},
        {"id": "eat", "name": "eating", "outlines": arrows((290, 430, 380, 545))},
        {"id": "decay", "name": "decomposition", "outlines": arrows((580, 530, 590, 140))},
        {"id": "burn", "name": "burning fossil fuels", "outlines": arrows((680, 450, 700, 140))},
        {"id": "sea", "name": "ocean exchange", "outlines": arrows((830, 140, 830, 620)) + arrows((910, 620, 910, 140))},
    ],
    "steps": [
        {"type": "trace", "title": "Tree", "structure": "tree", "instruction": "Trace the tree.",
         "note": {"text": "Carbon is in every living thing. Plants are where it enters the living world."}},
        {"type": "trace", "title": "Photosynthesis", "structure": "photo", "instruction": "Draw the arrow from the air into the tree.",
         "note": {"text": "Plants take carbon dioxide from the air and build it into sugar by photosynthesis.",
                  "remember": "Photosynthesis: carbon out of the air."}},
        {"type": "trace", "title": "Rabbit", "structure": "rabbit", "instruction": "Trace the rabbit.", "note": {"text": "Animals get their carbon by eating."}},
        {"type": "trace", "title": "Eating", "structure": "eat", "instruction": "Draw the arrow from the tree to the rabbit.",
         "note": {"text": "When the rabbit eats plants, carbon in the plant's sugar and other molecules becomes part of the rabbit."}},
        {"type": "trace", "title": "Respiration", "structure": "resp", "instruction": "Draw the two arrows back up to the air.",
         "note": {"text": "Plants and animals both do respiration, breaking down sugar and releasing carbon dioxide back to the air.",
                  "remember": "Respiration: carbon back into the air."}},
        {"type": "trace", "title": "Decomposers", "structure": "mushroom", "instruction": "Trace the mushroom.",
         "note": {"text": "Fungi and bacteria are decomposers. They break down dead plants and animals."}},
        {"type": "trace", "title": "Decomposition", "structure": "decay", "instruction": "Draw the arrow from the decomposers to the air.",
         "note": {"text": "Decomposers release carbon dioxide as they feed, returning the carbon in dead things to the air."}},
        {"type": "trace", "title": "Underground", "structure": "ground", "instruction": "Draw the ground, the fossil fuel layer and the pipe.",
         "note": {"text": "Coal, oil and gas formed from living things buried long ago. They hold carbon locked away for millions of years."}},
        {"type": "trace", "title": "Power plant", "structure": "factory", "instruction": "Trace the power plant's chimney.",
         "note": {"text": "People burn fossil fuels in power plants, factories and cars."}},
        {"type": "trace", "title": "Burning", "structure": "burn", "instruction": "Draw the arrow from the chimney to the air.",
         "note": {"text": "Burning releases that carbon as CO2 faster than plants can take it up, so the CO2 in the air is rising."}},
        {"type": "trace", "title": "Ocean", "structure": "ocean", "instruction": "Draw the ocean's surface.",
         "note": {"text": "The oceans are a huge store of carbon."}},
        {"type": "trace", "title": "Ocean exchange", "structure": "sea", "instruction": "Draw the arrows between the air and the ocean.",
         "note": {"text": "Carbon dioxide passes back and forth between the air and the ocean's water."}},
        {"type": "label", "title": "Name the processes", "instruction": "Pick the process for each numbered arrow.",
         "targets": [
             {"n": 1, "at": [105, 220], "answer": "Photosynthesis", "role": "Takes CO2 out of the air.",
              "mistakes": {"Respiration": "Respiration puts CO2 into the air. This arrow takes it out: photosynthesis."}},
             {"n": 2, "at": [280, 220], "answer": "Respiration", "role": "Puts CO2 back into the air."},
             {"n": 3, "at": [335, 488], "answer": "Eating", "role": "Passes carbon along a food chain."},
             {"n": 4, "at": [585, 335], "answer": "Decomposition", "role": "Breaks down dead things."},
             {"n": 5, "at": [690, 295], "answer": "Burning fossil fuels", "synonyms": ["Combustion"], "role": "Releases ancient carbon."}],
         "vocabulary": ["Photosynthesis", "Respiration", "Eating", "Decomposition", "Burning fossil fuels", "Combustion", "Evaporation"]},
        {"type": "choice", "title": "Matter is conserved", "instruction": "Follow one carbon atom.", "showsDiagram": True,
         "question": "A carbon atom is in the air. Which path could bring it back to the air?",
         "options": [
             {"text": "Tree, then rabbit, then respiration", "correct": True,
              "feedback": "Yes. The atom is never destroyed: it moves between living and nonliving parts of the ecosystem."},
             {"text": "It's used up by the tree and gone forever", "feedback": "Atoms aren't used up. The carbon cycles back to the air."},
             {"text": "Only by burning fossil fuels", "feedback": "That's one way, but respiration and decomposition return carbon all the time."},
             {"text": "It can't come back", "feedback": "Respiration, decomposition and burning all return carbon to the air."}]},
        {"type": "choice", "title": "Predict", "instruction": "Use the model.", "showsDiagram": True,
         "question": "A large forest is cut down and burned. What happens to the carbon dioxide in the air?",
         "options": [
             {"text": "It goes up: burning adds CO2, and fewer trees take it out", "correct": True,
              "feedback": "Right. Both arrows change: more carbon goes in and less comes out."},
             {"text": "It goes down", "feedback": "Fewer trees means less photosynthesis, and burning adds CO2. So it rises."},
             {"text": "Nothing changes", "feedback": "Look at the arrows. Burning adds CO2 and fewer trees take it out."},
             {"text": "The ocean stops working", "feedback": "The ocean still exchanges CO2. The air's CO2 still rises."}]},
    ],
}

# ---------------------------------------------------------------- The nitrogen cycle
LEAF_SMALL = "M 330 330 C 290 320 250 290 240 250 C 285 250 320 280 330 330 Z"
BOLT = [880, 110, 920, 110, 895, 210, 930, 210, 860, 360, 880, 250, 845, 250]
nitrogen = {
    "id": "g7-nitrogen-cycle", "title": "The nitrogen cycle", "grade": "7", "subject": "Life science", "standard": "MS-LS2-3",
    "minutes": 10,
    "sources": [LS2_3, CYCLES, PROKARYOTES, bio("22.5", "22-5-beneficial-prokaryotes", "Beneficial Prokaryotes (lightning fixes nitrogen)")],
    "keywords": ["nitrogen cycle", "nitrogen", "nitrogen fixation", "bacteria", "root nodules", "legumes", "nitrates",
                 "lightning", "decomposers", "denitrification", "protein", "matter", "cycling"],
    "printed": [{"text": "Nitrogen gas in the air", "at": [600, 70], "size": 30}, {"text": "Nitrates in the soil", "at": [440, 910], "size": 24},
                {"text": "Soil bacteria", "at": [690, 900], "size": 24}],
    "structures": [
        {"id": "plant", "name": "bean plant", "outlines": [{"line": [330, 560, 330, 330]}, {"path": LEAF_SMALL}, {"path": mirror_path(LEAF_SMALL, 330)}]},
        {"id": "roots", "name": "roots and nodules", "outlines": [{"line": [330, 575, 330, 790]}, {"line": [330, 650, 260, 740]},
                                                                {"line": [330, 700, 395, 780]}],
         "details": [{"circle": [288, 704, 12]}, {"circle": [372, 752, 12]}, {"circle": [330, 760, 12]}]},
        {"id": "soil", "name": "soil", "pen": "fine", "outlines": [{"line": [40, 565, 960, 565]}]},
        {"id": "bolt", "name": "lightning", "outlines": [{"polygon": BOLT}]},
        {"id": "rabbit", "name": "rabbit", "outlines": [{"ellipse": [590, 515, 60, 34]}, {"circle": [658, 482, 24]},
                                                     {"line": [650, 460, 642, 410]}, {"line": [668, 460, 678, 412]}]},
        {"id": "bacteria", "name": "soil bacteria", "outlines": [rrect(620, 780, 50, 22, 11), rrect(685, 800, 50, 22, 11), rrect(640, 830, 50, 22, 11)]},
        {"id": "fix", "name": "nitrogen fixation", "outlines": arrows((150, 140, 278, 690))},
        {"id": "strike", "name": "lightning fixing nitrogen", "outlines": arrows((880, 380, 880, 550))},
        {"id": "uptake", "name": "plants take up nitrates", "outlines": arrows((450, 870, 348, 795))},
        {"id": "eat", "name": "eating", "outlines": arrows((370, 330, 520, 480))},
        {"id": "decay", "name": "decomposition", "outlines": arrows((590, 560, 630, 765))},
        {"id": "nitrify", "name": "bacteria make nitrates", "outlines": arrows((615, 835, 520, 855))},
        {"id": "denitrify", "name": "back to the air", "outlines": arrows((745, 790, 780, 140))},
    ],
    "steps": [
        {"type": "trace", "title": "Soil", "structure": "soil", "instruction": "Draw the soil line.",
         "note": {"text": "About 78% of the air is nitrogen gas. Living things need nitrogen to build proteins and DNA."}},
        {"type": "trace", "title": "Bean plant", "structure": "plant", "instruction": "Trace the bean plant.",
         "note": {"text": "Plants and animals can't use nitrogen gas straight from the air.", "remember": "Nitrogen gas: not usable directly."}},
        {"type": "trace", "title": "Roots", "structure": "roots", "instruction": "Trace the roots.",
         "note": {"text": "Bean and pea plants are legumes. Their roots have bumps called nodules."}},
        {"type": "trace", "title": "Nodules", "structure": "roots", "part": "details", "instruction": "Dab the three nodules on the roots.",
         "note": {"text": "Bacteria living inside the nodules turn nitrogen gas into a form plants can use."}},
        {"type": "trace", "title": "Nitrogen fixation", "structure": "fix", "instruction": "Draw the arrow from the air to the nodules.",
         "note": {"text": "Changing nitrogen gas into a usable form is nitrogen fixation. Only certain bacteria can do it.",
                  "remember": "Fixation: bacteria make nitrogen usable."}},
        {"type": "trace", "title": "Lightning", "structure": "bolt", "instruction": "Trace the lightning bolt.",
         "note": {"text": "Lightning's energy can also fix nitrogen."}},
        {"type": "trace", "title": "Into the soil", "structure": "strike", "instruction": "Draw the arrow from the lightning to the soil.",
         "note": {"text": "Rain carries the fixed nitrogen down into the soil."}},
        {"type": "trace", "title": "Uptake", "structure": "uptake", "instruction": "Draw the arrow from the soil nitrates to the plant's roots.",
         "note": {"text": "Plant roots take in nitrates from the soil and use the nitrogen to build proteins."}},
        {"type": "trace", "title": "Rabbit", "structure": "rabbit", "instruction": "Trace the rabbit.", "note": {"text": "Animals get nitrogen by eating."}},
        {"type": "trace", "title": "Eating", "structure": "eat", "instruction": "Draw the arrow from the plant to the rabbit.",
         "note": {"text": "The rabbit uses the nitrogen in plant proteins to build its own proteins."}},
        {"type": "trace", "title": "Bacteria", "structure": "bacteria", "instruction": "Trace the soil bacteria.",
         "note": {"text": "Decomposers break down wastes and dead things, releasing ammonia into the soil."}},
        {"type": "trace", "title": "Decomposition", "structure": "decay", "instruction": "Draw the arrow from the rabbit down to the bacteria.",
         "note": {"text": "Wastes and dead bodies return their nitrogen to the soil."}},
        {"type": "trace", "title": "Nitrates", "structure": "nitrify", "instruction": "Draw the arrow from the bacteria to the nitrates.",
         "note": {"text": "Other bacteria change the ammonia into nitrates, which plants can take up again."}},
        {"type": "trace", "title": "Back to the air", "structure": "denitrify", "instruction": "Draw the arrow from the bacteria up to the air.",
         "note": {"text": "Some bacteria turn nitrates back into nitrogen gas, completing the cycle."}},
        {"type": "label", "title": "Name the steps", "instruction": "Pick the process for each numbered arrow.",
         "targets": [
             {"n": 1, "at": [214, 415], "answer": "Nitrogen fixation", "role": "Air to a usable form.",
              "mistakes": {"Decomposition": "Decomposition breaks down dead things. This arrow takes nitrogen from the air: fixation."}},
             {"n": 2, "at": [399, 832], "answer": "Uptake by roots", "role": "Soil nitrates into the plant."},
             {"n": 3, "at": [445, 405], "answer": "Eating", "role": "Plant to animal."},
             {"n": 4, "at": [610, 662], "answer": "Decomposition", "role": "Returns nitrogen to the soil."}],
         "vocabulary": ["Nitrogen fixation", "Uptake by roots", "Eating", "Decomposition", "Photosynthesis", "Evaporation"]},
        {"type": "choice", "title": "Why bacteria matter", "instruction": "Use the model.", "showsDiagram": True,
         "question": "Nitrogen gas is all around plants. Why do they still depend on bacteria?",
         "options": [
             {"text": "Plants can't use nitrogen gas; bacteria change it into a form they can", "correct": True,
              "feedback": "Yes. Without nitrogen-fixing bacteria, very little nitrogen would enter the living world."},
             {"text": "Bacteria eat the plants", "feedback": "These bacteria help plants. They fix nitrogen into a usable form."},
             {"text": "Bacteria make oxygen for roots", "feedback": "They fix nitrogen, changing the gas into a form plants can use."},
             {"text": "They don't depend on bacteria", "feedback": "Plants can't use nitrogen gas themselves. Bacteria make it usable."}]},
        {"type": "choice", "title": "Farmers", "instruction": "Apply the model.", "showsDiagram": True,
         "question": "Farmers often plant beans in a field one year and corn the next. Why does this help the corn?",
         "options": [
             {"text": "Bacteria in the bean roots add usable nitrogen to the soil", "correct": True,
              "feedback": "Right. The nodule bacteria fix nitrogen, enriching the soil for the next crop."},
             {"text": "Beans add oxygen to the soil", "feedback": "The key is nitrogen: bean root bacteria fix it into the soil."},
             {"text": "Beans scare away insects", "feedback": "The benefit is nitrogen fixed by bacteria in bean roots."},
             {"text": "Corn and beans are the same plant", "feedback": "They're different. Beans' root bacteria fix nitrogen for the corn."}]},
    ],
}

for lesson in (photo, respiration, symbiosis, carbon, nitrogen):
    save(lesson)
