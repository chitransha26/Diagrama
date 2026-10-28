"""Grade 5 life and Earth science · what a plant takes in and gives out (5-LS1-1), a forest food web,
an ocean food chain and decomposers (5-LS2-1), and the water cycle (5-ESS2-1).

Facts checked against OpenStax Biology 2e (searched with curriculum/tools/openstax.py), NOAA Ocean Today
and National Wildlife Federation species pages and articles.
"""
import math

from lib import save, straight_arrow, mirror_path


def ngss(code, text):
    return {"title": f"NGSS {code}: {text}"}


def bio(section, slug, title):
    return {"title": f"OpenStax Biology 2e, {section} {title}", "url": f"https://openstax.org/books/biology-2e/pages/{slug}"}


LS2 = ngss("5-LS2-1", "Develop a model to describe the movement of matter among plants, animals, decomposers, and the environment")
ECOSYSTEMS = bio("46.1", "46-1-ecology-of-ecosystems", "Ecology of Ecosystems")


def sun(cx=130, cy=130, radius=60):
    rays = [{"line": [round(cx + (radius + 18) * math.cos(math.radians(a)), 1), round(cy + (radius + 18) * math.sin(math.radians(a)), 1),
                      round(cx + (radius + 50) * math.cos(math.radians(a)), 1), round(cy + (radius + 50) * math.sin(math.radians(a)), 1)]}
            for a in range(0, 360, 45)]
    return {"id": "sun", "name": "sun", "pen": "bold", "outlines": [{"circle": [cx, cy, radius]}], "details": rays}


# ---------------------------------------------------------------- What a plant takes in and gives out
left_leaf = "M 500 520 C 460 470 400 460 350 476 C 390 520 450 540 500 520 Z"
upper_leaf = "M 500 440 C 460 390 400 380 350 396 C 390 440 450 460 500 440 Z"
plant = {
    "id": "g5-plant-in-out", "title": "What a plant takes in and gives out", "grade": "5", "subject": "Life science",
    "standard": "5-LS1-1", "minutes": 7,
    "sources": [ngss("5-LS1-1", "Support an argument that plants get the materials they need for growth chiefly from air and water"),
                bio("30.2", "30-2-stems", "Stems (stomata take up carbon dioxide and release oxygen and water vapor)"),
                bio("25.1", "25-1-early-plant-life", "Early Plant Life (roots take up water and minerals)"),
                bio("31.3", "31-3-nutritional-adaptations-of-plants", "Nutritional Adaptations of Plants")],
    "keywords": ["plant", "photosynthesis", "carbon dioxide", "oxygen", "water", "sunlight", "air", "roots", "leaves",
                 "growth", "matter", "food"],
    "structures": [
        sun(),
        {"id": "ground", "name": "ground", "outlines": [{"line": [40, 640, 960, 640]}]},
        {"id": "plant", "name": "stem and leaves", "outlines": [
            {"line": [500, 640, 500, 320]}, {"path": left_leaf}, {"path": mirror_path(upper_leaf, 500)}]},
        {"id": "roots", "name": "roots", "outlines": [
            {"line": [500, 640, 440, 740, 400, 780]}, {"line": [500, 640, 560, 740, 610, 790]}, {"line": [500, 650, 500, 790]}]},
        {"id": "light", "name": "sunlight", "pen": "bold", "outlines": straight_arrow(190, 200, 360, 440)},
        {"id": "co2", "name": "carbon dioxide", "pen": "bold", "outlines": straight_arrow(80, 580, 330, 510)},
        {"id": "o2", "name": "oxygen", "pen": "bold", "outlines": straight_arrow(670, 400, 900, 330)},
        {"id": "water", "name": "water", "pen": "bold", "outlines": straight_arrow(200, 800, 380, 790)},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "Plants need sunlight. Light gives them the energy to make their own food."}},
        {"type": "trace", "title": "Ground", "structure": "ground", "instruction": "Draw the ground line.",
         "note": {"text": "Above the ground, leaves meet the air and light. Below, roots meet the soil and water."}},
        {"type": "trace", "title": "Stem and leaves", "structure": "plant", "instruction": "Trace the stem and the two leaves.",
         "note": {"text": "Leaves have tiny openings that let air in and out. That's where the plant takes in carbon dioxide.",
                  "remember": "Leaves trade gases with the air."}},
        {"type": "trace", "title": "Roots", "structure": "roots", "instruction": "Trace the three roots.",
         "note": {"text": "Roots take up water, plus small amounts of minerals, from the soil. They also anchor the plant."}},
        {"type": "trace", "title": "Sunlight", "structure": "light", "instruction": "Draw the arrow of sunlight reaching the leaf.",
         "note": {"text": "Sunlight brings energy, not matter. It powers the leaf's food-making.", "remember": "Light = energy."}},
        {"type": "trace", "title": "Carbon dioxide in", "structure": "co2", "instruction": "Draw the arrow of carbon dioxide going into the leaf.",
         "note": {"text": "Carbon dioxide is a gas in the air. The plant builds it, with water, into sugar: food and new plant material.",
                  "remember": "In from the air: carbon dioxide."}},
        {"type": "trace", "title": "Water in", "structure": "water", "instruction": "Draw the arrow of water going into the roots.",
         "note": {"text": "Water travels from the roots up the stem to the leaves.", "remember": "In from the soil: water."}},
        {"type": "trace", "title": "Oxygen out", "structure": "o2", "instruction": "Draw the arrow of oxygen leaving the leaf.",
         "note": {"text": "As it makes food, the plant gives off oxygen into the air. Water vapor escapes from the leaves too.",
                  "remember": "Out to the air: oxygen."}},
        {"type": "label", "title": "Label the arrows", "instruction": "Pick the right name for each numbered arrow.",
         "targets": [
             {"n": 1, "at": [275, 320], "answer": "Sunlight", "role": "Energy for making food."},
             {"n": 2, "at": [205, 545], "answer": "Carbon dioxide", "role": "Gas taken in from the air.",
              "mistakes": {"Oxygen": "This arrow points into the leaf. The plant takes in carbon dioxide and gives out oxygen."}},
             {"n": 3, "at": [785, 365], "answer": "Oxygen", "role": "Gas given out to the air.",
              "mistakes": {"Carbon dioxide": "This arrow points out of the leaf. The plant gives off oxygen."}},
             {"n": 4, "at": [290, 795], "answer": "Water", "role": "Taken in by the roots."}],
         "vocabulary": ["Sunlight", "Carbon dioxide", "Oxygen", "Water", "Soil"],
         "commonMistakes": {"Soil": "Soil gives a plant small amounts of minerals, but these arrows show light, gases and water."}},
        {"type": "choice", "title": "Argue", "instruction": "Where does a plant's material come from?", "showsDiagram": True,
         "question": "A tiny seed grows into a huge tree. Where did most of the tree's new material come from?",
         "options": [
             {"text": "Air and water", "correct": True,
              "feedback": "Yes. The tree builds itself mostly from carbon dioxide in the air and water, using the sun's energy."},
             {"text": "The soil", "feedback": "Surprisingly, no. Soil gives only small amounts of minerals. Most of the tree is built from air and water."},
             {"text": "Sunlight", "feedback": "Sunlight gives the energy, but it isn't matter. The material comes from air and water."},
             {"text": "The seed", "feedback": "The seed was tiny. Almost all the tree's material came later, from air and water."}]},
        {"type": "choice", "title": "Give and take", "instruction": "Think about the air.", "showsDiagram": True,
         "question": "Which gas does the plant take in, and which does it give out?",
         "options": [
             {"text": "Takes in carbon dioxide, gives out oxygen", "correct": True,
              "feedback": "Right. Leaves take in carbon dioxide to make food and give off oxygen."},
             {"text": "Takes in oxygen, gives out carbon dioxide", "feedback": "That's the other way round. To make food, leaves take in carbon dioxide and give off oxygen."},
             {"text": "Takes in water, gives out sunlight", "feedback": "Sunlight comes from the sun. The gases are carbon dioxide in and oxygen out."},
             {"text": "It doesn't use gases", "feedback": "Plants do: they take in carbon dioxide and give off oxygen through their leaves."}]},
    ],
}

# ---------------------------------------------------------------- Forest food web
NWF_FOX = {"title": "National Wildlife Federation: Red Fox", "url": "https://www.nwf.org/Educational-Resources/Wildlife-Guide/Mammals/Red-Fox"}
NWF_OWL = {"title": "National Wildlife Federation: Great Horned Owl",
           "url": "https://www.nwf.org/Educational-Resources/Wildlife-Guide/Birds/Great-Horned-Owl"}
NWF_CHICKADEES = {"title": "National Wildlife: Why Birds Need Native Trees (chickadees feed caterpillars to their young)",
                  "url": "https://www.nwf.org/Magazines/National-Wildlife/2015/FebMarch/Animals/Chickadees-And-Native-Trees"}
NWF_OAKS = {"title": "National Wildlife: Want to Nurture Wildlife? Plant a Native Oak.",
            "url": "https://www.nwf.org/Magazines/National-Wildlife/2024/Fall/Gardening/Planting-Oak-Trees"}
NWF_ACORNS = {"title": "National Wildlife: When Nature Goes Nuts (mice and acorns)",
              "url": "https://www.nwf.org/Magazines/National-Wildlife/1999/When-Nature-Goes-Nuts"}
NWF_RABBITS = {"title": "National Wildlife: Bunny Boom and Bust (cottontails eat leaves and berries)",
               "url": "https://www.nwf.org/Magazines/National-Wildlife/2002/Bunny-Boom-and-Bust"}


def box(cx, cy, w=220, h=80):
    return {"rect": [cx - w / 2, cy - h / 2, w, h, 16]}


NODES = {"Owl": (350, 120), "Fox": (750, 120), "Chickadee": (150, 330), "Caterpillar": (150, 560),
         "Mouse": (470, 560), "Rabbit": (800, 560), "Oak tree": (300, 820), "Berry bush": (700, 820)}
web = {
    "id": "g5-forest-food-web", "title": "Forest food web", "grade": "5", "subject": "Life science",
    "standard": "5-LS2-1", "minutes": 9, "colorMode": "illustration",
    "sources": [LS2, ECOSYSTEMS, NWF_OAKS, NWF_CHICKADEES, NWF_ACORNS, NWF_RABBITS, NWF_FOX, NWF_OWL],
    "keywords": ["food web", "food chain", "producer", "consumer", "predator", "prey", "forest", "oak", "owl", "fox",
                 "energy", "matter", "ecosystem"],
    "printed": [{"text": name, "at": [x, y + 2], "size": 32} for name, (x, y) in NODES.items()],
    "legend": [
        {"name": "Producers", "color": "#6FA845", "meaning": "Make their own food from sunlight"},
        {"name": "Eat producers", "color": "#E7C340", "meaning": "Consumers that eat plants in this web"},
        {"name": "Eat consumers", "color": "#E0864A", "meaning": "Consumers that eat other animals in this web"},
    ],
    "structures": [
        {"id": "producers", "name": "producers", "colorName": "producers", "fill": "#6FA845", "pen": "bold",
         "outlines": [box(*NODES["Oak tree"]), box(*NODES["Berry bush"])]},
        {"id": "grazers", "name": "animals that eat producers", "colorName": "eat producers", "fill": "#E7C340",
         "outlines": [box(*NODES["Caterpillar"]), box(*NODES["Mouse"]), box(*NODES["Rabbit"])]},
        {"id": "predators", "name": "animals that eat consumers", "colorName": "eat consumers", "fill": "#E0864A",
         "outlines": [box(*NODES["Chickadee"]), box(*NODES["Owl"]), box(*NODES["Fox"])]},
        {"id": "plantArrows", "name": "arrows from plants", "outlines":
            straight_arrow(270, 778, 170, 606) + straight_arrow(330, 778, 440, 606) + straight_arrow(730, 778, 790, 606)},
        {"id": "animalArrows", "name": "arrows from animals", "outlines":
            straight_arrow(150, 518, 150, 376) + straight_arrow(190, 288, 320, 166) + straight_arrow(440, 518, 370, 166)
            + straight_arrow(510, 518, 720, 166) + straight_arrow(800, 518, 770, 166)},
    ],
    "steps": [
        {"type": "trace", "title": "Producers", "structure": "producers", "instruction": "Trace the boxes around the oak tree and the berry bush.",
         "note": {"text": "Producers make their own food from sunlight, air and water. Every food web starts with them.",
                  "remember": "Producers make their own food."}},
        {"type": "trace", "title": "Plant eaters", "structure": "grazers", "instruction": "Trace the boxes around the caterpillar, mouse and rabbit.",
         "note": {"text": "Many caterpillars feed on oaks, mice eat acorns, and rabbits eat leaves and berries. They're consumers."}},
        {"type": "trace", "title": "Predators", "structure": "predators", "instruction": "Trace the boxes around the chickadee, owl and fox.",
         "note": {"text": "These consumers eat other animals. Chickadees feed caterpillars to their chicks. Owls and foxes hunt mice and rabbits."}},
        {"type": "trace", "title": "Arrows from plants", "structure": "plantArrows", "instruction": "Draw the three arrows from the plants up to the animals that eat them.",
         "note": {"text": "Each arrow points from the food to the eater. It shows which way matter and energy move.",
                  "remember": "Arrow: from food to eater."}},
        {"type": "trace", "title": "Arrows from animals", "structure": "animalArrows", "instruction": "Draw the five arrows to the chickadee, owl and fox.",
         "note": {"text": "The mouse has two arrows leaving it: owls and foxes both eat mice. Linked food chains like this make a food web.",
                  "remember": "Many linked chains = a food web."}},
        {"type": "color", "title": "Color", "structures": ["producers", "grazers", "predators"],
         "instruction": "Color each group: producers, animals that eat producers, and animals that eat other animals."},
        {"type": "choice", "title": "Read the web", "instruction": "Follow the arrows.", "showsDiagram": True,
         "question": "In this web, which animals eat the mouse?",
         "options": [
             {"text": "The owl and the fox", "correct": True, "feedback": "Yes. Two arrows leave the mouse: one to the owl, one to the fox."},
             {"text": "The oak tree", "feedback": "The arrow goes from the oak to the mouse: the mouse eats acorns, not the other way round."},
             {"text": "The chickadee", "feedback": "No arrow joins the mouse to the chickadee. Follow the mouse's arrows: owl and fox."},
             {"text": "The rabbit", "feedback": "Rabbits eat plants. The mouse's arrows go to the owl and the fox."}]},
        {"type": "choice", "title": "Predict", "instruction": "Change the web.", "showsDiagram": True,
         "question": "A disease kills most of the owls. What would probably happen to the mice, at first?",
         "options": [
             {"text": "There would be more mice, because fewer are eaten", "correct": True,
              "feedback": "Right. With fewer owls hunting them, more mice survive. A change to one living thing ripples through the web."},
             {"text": "There would be fewer mice", "feedback": "Owls eat mice. Fewer owls means fewer mice get eaten, so mice would increase."},
             {"text": "Nothing would change", "feedback": "Everything in a web is linked. Fewer owls means more mice survive."},
             {"text": "The mice would start eating owls", "feedback": "Mice eat acorns in this web. With fewer owls hunting them, more mice survive."}]},
        {"type": "choice", "title": "Energy", "instruction": "Trace it back.", "showsDiagram": True,
         "question": "The fox gets energy by eating a rabbit. Where did that energy first come from?",
         "options": [
             {"text": "The sun, through the berry bush", "correct": True,
              "feedback": "Yes. The bush stored the sun's energy, the rabbit ate its leaves and berries, and the fox ate the rabbit."},
             {"text": "The owl", "feedback": "No arrow joins the owl and the fox. Follow the fox's arrows back: rabbit, bush, sun."},
             {"text": "The oak tree", "feedback": "No arrow joins the oak and the rabbit. The rabbit ate the berry bush, which got its energy from the sun."},
             {"text": "The fox itself", "feedback": "Animals get energy from food. Follow it back: rabbit, bush, sun."}]},
    ],
}

# ---------------------------------------------------------------- Ocean food chain
NOAA_KRILL = {"title": "NOAA Ocean Today: Animals of the Ice: Antarctic Krill", "url": "https://oceantoday.noaa.gov/animalsoftheice_krill/"}
surface = []
for i in range(0, 93):
    x = 40 + i * 10
    surface += [x, round(300 + 10 * math.sin(2 * math.pi * (x - 40) / 120), 1)]
whale_body = ("M 610 600 C 620 560 720 540 820 560 C 870 570 910 588 940 598 "
              "C 910 612 870 626 820 640 C 730 664 640 650 610 600 Z")
ocean = {
    "id": "g5-ocean-food-chain", "title": "Ocean food chain", "grade": "5", "subject": "Life science",
    "standard": "5-LS2-1", "minutes": 7,
    "sources": [LS2, NOAA_KRILL, bio("44.4", "44-4-aquatic-biomes", "Aquatic Biomes (phytoplankton are the base of the food web)"),
                ECOSYSTEMS],
    "keywords": ["food chain", "ocean", "phytoplankton", "krill", "whale", "producer", "consumer", "Antarctica", "energy", "plankton"],
    "structures": [
        sun(),
        {"id": "surface", "name": "ocean surface", "outlines": [{"line": surface}]},
        {"id": "phyto", "name": "phytoplankton", "outlines":
            [{"circle": [x, y, 12]} for x, y in [(110, 390), (160, 410), (110, 440), (160, 462), (210, 384)]]},
        {"id": "krill", "name": "krill", "outlines": [
            {"path": "M 360 500 C 376 458 470 452 500 486 C 478 516 400 526 360 500 Z"},
            {"line": [490, 486, 560, 440]}, {"line": [490, 490, 566, 470]}, {"line": [362, 500, 334, 488]}, {"line": [362, 502, 338, 520]}],
         "details": [{"circle": [476, 486, 5]}] + [{"line": [x, 512 - (x - 400) // 8, x - 6, 538 - (x - 400) // 8]} for x in (400, 424, 448)]},
        {"id": "whale", "name": "whale", "pen": "bold", "outlines": [
            {"path": whale_body}, {"path": "M 940 598 C 960 588 980 586 996 590 C 980 604 960 606 940 598 Z"},
            {"path": "M 720 652 C 730 700 760 740 800 760 C 790 720 770 680 760 650"}],
         "details": [{"circle": [664, 596, 6]}, {"line": [614, 610, 700, 622]}, {"line": [640, 632, 712, 642]}]},
        {"id": "chain", "name": "energy and matter", "pen": "bold",
         "outlines": straight_arrow(160, 220, 150, 360) + straight_arrow(230, 430, 330, 490) + straight_arrow(512, 510, 606, 580)},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "Sunlight shines into the top layer of the ocean. Ocean food chains start there."}},
        {"type": "trace", "title": "Ocean surface", "structure": "surface", "instruction": "Trace the wavy ocean surface.",
         "note": {"text": "This is the cold Southern Ocean, around Antarctica."}},
        {"type": "trace", "title": "Phytoplankton", "structure": "phyto", "instruction": "Trace the five phytoplankton near the surface.",
         "note": {"text": "Phytoplankton are tiny living things that make food from sunlight, like plants do. Shown much bigger than real.",
                  "remember": "Phytoplankton = the ocean's producers."}},
        {"type": "trace", "title": "Krill", "structure": "krill", "instruction": "Trace the krill's body, its tail fan and two long feelers.",
         "note": {"text": "Krill are small shrimp-like animals. They eat phytoplankton and algae that grow under sea ice."}},
        {"type": "trace", "title": "Krill eye and legs", "structure": "krill", "part": "details", "instruction": "Draw the krill's eye and its three legs.",
         "note": {"text": "Krill swarm in huge numbers, so many animals can feed on them."}},
        {"type": "trace", "title": "Whale", "structure": "whale", "instruction": "Trace the whale's body, tail flukes and long flipper.",
         "note": {"text": "Whales, seals, fish and penguins all depend on eating krill. Here, a whale is the next link.",
                  "remember": "Many animals depend on krill."}},
        {"type": "trace", "title": "Whale face", "structure": "whale", "part": "details", "instruction": "Draw the whale's eye, mouth and throat grooves.",
         "note": {"text": "A whale is a consumer: it can't make its own food."}},
        {"type": "trace", "title": "The chain", "structure": "chain", "instruction": "Draw the arrows: sun to phytoplankton, to krill, to whale.",
         "note": {"text": "Arrows point from the food to the eater. Matter and energy move along the chain this way.",
                  "remember": "Arrow: from food to eater."}},
        {"type": "order", "title": "Build the chain", "items": ["Sun", "Phytoplankton", "Krill", "Whale"],
         "instruction": "Tap them in order, starting where the energy begins.",
         "why": "Phytoplankton capture the sun's energy, krill eat phytoplankton, and whales eat krill.",
         "hint": "Which living thing makes its own food?"},
        {"type": "choice", "title": "Predict", "instruction": "Change the chain.", "showsDiagram": True,
         "question": "Melting sea ice means less algae for krill to eat, so there are fewer krill. What happens to the whales?",
         "options": [
             {"text": "They have less food, so it's harder for them to survive", "correct": True,
              "feedback": "Yes. Whales depend on krill. A change at the bottom of a food chain affects everything above it."},
             {"text": "Nothing: whales eat phytoplankton", "feedback": "In this chain, whales eat krill. Fewer krill means less food for whales."},
             {"text": "They have more food", "feedback": "Fewer krill means less food for whales, not more."},
             {"text": "The whales make their own food", "feedback": "Whales are consumers: they can't make food. They depend on krill."}]},
        {"type": "choice", "title": "Producers", "instruction": "Find the producer.", "showsDiagram": True,
         "question": "Which living thing in this chain is the producer?",
         "options": [
             {"text": "Phytoplankton", "correct": True, "feedback": "Right. Phytoplankton make food from sunlight, so they're the producers."},
             {"text": "Krill", "feedback": "Krill eat phytoplankton, so they're consumers. The phytoplankton make the food."},
             {"text": "Whale", "feedback": "Whales eat krill, so they're consumers. The producers are the phytoplankton."},
             {"text": "The sun", "feedback": "The sun gives the energy, but it isn't alive. The producers are the phytoplankton."}]},
    ],
}

# ---------------------------------------------------------------- Decomposers return nutrients to soil
decomposers = {
    "id": "g5-decomposers", "title": "Decomposers return nutrients to soil", "grade": "5", "subject": "Life science",
    "standard": "5-LS2-1", "minutes": 8,
    "sources": [LS2, bio("24.3", "24-3-ecology-of-fungi", "Ecology of Fungi (fungi as decomposers and recyclers)"),
                bio("22.3", "22-3-prokaryotic-metabolism", "Prokaryotic Metabolism (bacteria and fungi are decomposers)"),
                bio("44.3", "44-3-terrestrial-biomes", "Terrestrial Biomes (decaying leaf litter returns nutrients to the soil)")],
    "keywords": ["decomposers", "decomposition", "fungi", "mushrooms", "bacteria", "nutrients", "soil", "recycling",
                 "dead leaves", "log", "matter cycle"],
    "structures": [
        {"id": "ground", "name": "ground", "outlines": [{"line": [40, 600, 960, 600]}]},
        {"id": "tree", "name": "tree", "pen": "bold", "outlines": [{"line": [200, 600, 212, 343]}, {"line": [260, 600, 248, 343]}, {"circle": [230, 225, 120]}]},
        {"id": "roots", "name": "roots", "outlines": [
            {"line": [215, 600, 170, 700, 130, 740]}, {"line": [245, 600, 290, 700, 340, 750]}, {"line": [230, 610, 232, 730]}]},
        {"id": "leaves", "name": "fallen leaves", "outlines": [{"ellipse": [380, 586, 32, 11]}, {"ellipse": [454, 588, 32, 11]}]},
        {"id": "log", "name": "fallen log", "outlines": [{"rect": [560, 520, 320, 76, 38]}]},
        {"id": "fungi", "name": "mushrooms", "outlines": [
            {"line": [640, 520, 640, 482]}, {"path": "M 600 482 C 610 440 670 440 680 482 Z"},
            {"line": [760, 520, 760, 472]}, {"path": "M 724 472 C 732 436 788 436 796 472 Z"}]},
        {"id": "bacteria", "name": "bacteria", "outlines": [{"circle": [x, y, 7]} for x, y in
                                                           [(700, 750), (680, 680), (750, 645), (820, 700), (880, 655)]]},
        {"id": "cycle", "name": "nutrient cycle", "pen": "bold",
         "outlines": straight_arrow(330, 310, 380, 560) + straight_arrow(640, 620, 520, 770) + straight_arrow(480, 800, 356, 762)},
    ],
    "steps": [
        {"type": "trace", "title": "Ground", "structure": "ground", "instruction": "Draw the ground line.",
         "note": {"text": "On the forest floor, dead leaves, logs and animals pile up. Something has to break them down."}},
        {"type": "trace", "title": "Tree", "structure": "tree", "instruction": "Trace the tree's trunk and crown.",
         "note": {"text": "A tree builds its leaves and wood using air, water, and nutrients from the soil."}},
        {"type": "trace", "title": "Roots", "structure": "roots", "instruction": "Trace the three roots.",
         "note": {"text": "Roots take up water and nutrients from the soil."}},
        {"type": "trace", "title": "Fallen leaves", "structure": "leaves", "instruction": "Trace the two fallen leaves.",
         "note": {"text": "Each fall, many trees drop their leaves. The leaves still hold nutrients the tree used."}},
        {"type": "trace", "title": "Fallen log", "structure": "log", "instruction": "Trace the fallen log.",
         "note": {"text": "Dead wood is matter too. Over years, it slowly rots away."}},
        {"type": "trace", "title": "Mushrooms", "structure": "fungi", "instruction": "Trace the two mushrooms on the log.",
         "note": {"text": "Mushrooms are fungi. Fungi break down dead plants and animals, freeing nutrients that other living things need.",
                  "remember": "Fungi are decomposers."}},
        {"type": "trace", "title": "Bacteria", "structure": "bacteria", "instruction": "Trace the five bacteria in the soil.",
         "note": {"text": "Bacteria are far too small to see; these are drawn huge. Along with fungi, they break down dead matter.",
                  "remember": "Bacteria are decomposers too."}},
        {"type": "trace", "title": "The cycle", "structure": "cycle", "instruction": "Draw the arrows: leaves fall, nutrients go into the soil, roots take them up.",
         "note": {"text": "As dead leaves and wood decay, their nutrients return to the soil, where roots can take them up again.",
                  "remember": "Decomposers recycle nutrients."}},
        {"type": "order", "title": "Recycling",
         "items": ["Leaves fall to the ground", "Fungi and bacteria break them down", "Nutrients go back into the soil", "Roots take up the nutrients"],
         "instruction": "Tap the steps in order.",
         "why": "Decomposers break down dead matter, returning its nutrients to the soil for plants to use again.",
         "hint": "What happens first, in the fall?"},
        {"type": "choice", "title": "Predict", "instruction": "Imagine a forest with no decomposers.", "showsDiagram": True,
         "question": "What would happen in a forest with no fungi or bacteria?",
         "options": [
             {"text": "Dead leaves and logs would pile up, and the soil would run short of nutrients", "correct": True,
              "feedback": "Yes. Without decomposers, nutrients stay locked in dead matter instead of returning to the soil for plants."},
             {"text": "Trees would grow faster", "feedback": "Trees need the nutrients decomposers return to the soil. Without them, the soil runs short."},
             {"text": "Nothing would change", "feedback": "Decomposers recycle nutrients. Without them, dead matter piles up and soil runs short."},
             {"text": "Leaves would turn back into trees", "feedback": "Dead leaves can't do that. Decomposers break them down so their nutrients reach new plants."}]},
        {"type": "choice", "title": "Classify", "instruction": "Which one is a decomposer?", "showsDiagram": False,
         "question": "Which of these is a decomposer?",
         "options": [
             {"text": "A mushroom growing on a dead log", "correct": True,
              "feedback": "Right. Mushrooms are fungi, which break down dead matter and return nutrients to the soil."},
             {"text": "An oak tree", "feedback": "An oak is a producer: it makes its own food from sunlight."},
             {"text": "A rabbit eating leaves", "feedback": "A rabbit eats living plants, so it's a consumer, not a decomposer."},
             {"text": "An owl", "feedback": "An owl hunts animals, so it's a consumer. Decomposers break down dead matter."}]},
    ],
}

# ---------------------------------------------------------------- The water cycle
WATER = bio("46.3", "46-3-biogeochemical-cycles", "Biogeochemical Cycles (the water cycle)")
sea = []
for i in range(0, 46):
    x = 40 + i * 10
    sea += [x, round(760 + 8 * math.sin(2 * math.pi * (x - 40) / 100), 1)]
cloud = ("M 600 260 C 580 220 620 190 660 205 C 680 160 760 160 780 200 C 820 185 860 215 845 250 "
         "C 860 280 820 295 790 285 L 630 285 C 600 290 585 275 600 260 Z")
water = {
    "id": "g5-water-cycle", "title": "The water cycle", "grade": "5", "subject": "Earth & space",
    "standard": "5-ESS2-1", "minutes": 8,
    "sources": [ngss("5-ESS2-1", "Develop a model using an example to describe ways the geosphere, biosphere, hydrosphere, and/or "
                                  "atmosphere interact"), WATER],
    "keywords": ["water cycle", "evaporation", "condensation", "precipitation", "runoff", "cloud", "rain", "ocean",
                 "water vapor", "hydrosphere", "atmosphere"],
    "structures": [
        sun(),
        {"id": "sea", "name": "ocean", "outlines": [{"line": sea}]},
        {"id": "mountain", "name": "mountain", "pen": "bold", "outlines": [{"line": [480, 780, 720, 420, 960, 780]}]},
        {"id": "cloud", "name": "cloud", "outlines": [{"path": cloud}]},
        {"id": "evaporation", "name": "evaporation", "pen": "bold",
         "outlines": straight_arrow(220, 720, 220, 540) + straight_arrow(330, 720, 330, 540)},
        {"id": "condensation", "name": "condensation", "pen": "bold", "outlines": straight_arrow(330, 480, 570, 280)},
        {"id": "rain", "name": "precipitation", "outlines": [{"line": [660, 310, 645, 360]}, {"line": [720, 310, 705, 360]},
                                                              {"line": [780, 310, 765, 360]}]},
        {"id": "runoff", "name": "runoff", "pen": "bold", "outlines": straight_arrow(602, 543, 494, 708)},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "The sun's energy drives the whole water cycle by warming the ocean and other water.",
                  "remember": "The sun powers the water cycle."}},
        {"type": "trace", "title": "Ocean", "structure": "sea", "instruction": "Trace the ocean's wavy surface.",
         "note": {"text": "Most of Earth's water is in the ocean."}},
        {"type": "trace", "title": "Mountain", "structure": "mountain", "instruction": "Trace the mountain.",
         "note": {"text": "Land is part of the cycle too. Water falls on it and flows back to the sea."}},
        {"type": "trace", "title": "Evaporation", "structure": "evaporation", "instruction": "Draw the two arrows rising from the ocean.",
         "note": {"text": "Warmed by the sun, liquid water evaporates: it turns into water vapor, an invisible gas, and rises into the air.",
                  "remember": "Evaporation: liquid to gas."}},
        {"type": "trace", "title": "Cloud", "structure": "cloud", "instruction": "Trace the cloud.",
         "note": {"text": "High up, water vapor cools and condenses into tiny droplets or ice crystals. Together they make a cloud.",
                  "remember": "Condensation: gas to liquid."}},
        {"type": "trace", "title": "Condensation", "structure": "condensation", "instruction": "Draw the arrow from the rising vapor to the cloud.",
         "note": {"text": "Water vapor moves through the air: the hydrosphere and atmosphere working together."}},
        {"type": "trace", "title": "Precipitation", "structure": "rain", "instruction": "Draw the three lines of rain.",
         "note": {"text": "When the drops grow heavy, they fall as precipitation: rain or snow.", "remember": "Precipitation: rain or snow."}},
        {"type": "trace", "title": "Runoff", "structure": "runoff", "instruction": "Draw the arrow of water flowing down the mountain to the ocean.",
         "note": {"text": "Some rain soaks into the ground. Some runs off in streams and rivers, back to the ocean, and the cycle repeats.",
                  "remember": "Runoff flows back to the sea."}},
        {"type": "label", "title": "Label the cycle", "instruction": "Pick the right name for each numbered part.",
         "targets": [
             {"n": 1, "at": [275, 630], "answer": "Evaporation", "role": "Liquid water turns to vapor."},
             {"n": 2, "at": [720, 230], "answer": "Condensation", "role": "Vapor turns to droplets in a cloud.",
              "mistakes": {"Evaporation": "Evaporation happens at the ocean. Up here, vapor turns back into droplets: condensation."}},
             {"n": 3, "at": [712, 340], "answer": "Precipitation", "role": "Rain or snow falls."},
             {"n": 4, "at": [548, 626], "answer": "Runoff", "role": "Water flows back to the ocean."}],
         "vocabulary": ["Evaporation", "Condensation", "Precipitation", "Runoff", "Erosion"]},
        {"type": "order", "title": "Around the cycle", "items": ["Evaporation", "Condensation", "Precipitation", "Runoff"],
         "instruction": "Start at the ocean. Tap the steps in order.",
         "why": "Water evaporates, condenses into clouds, falls as precipitation, and runs off back to the ocean.",
         "hint": "What does the sun do to the ocean water first?"},
        {"type": "choice", "title": "Explain", "instruction": "Think about where the water goes.", "showsDiagram": True,
         "question": "A puddle disappears on a sunny day. Where did the water go?",
         "options": [
             {"text": "It evaporated into the air as water vapor", "correct": True,
              "feedback": "Yes. The sun warmed it, and it became an invisible gas in the air. Later it may condense into a cloud."},
             {"text": "It was destroyed by the sun", "feedback": "Water isn't destroyed. It evaporated into the air as water vapor."},
             {"text": "It turned into a cloud right away", "feedback": "First it evaporated into invisible vapor. Clouds form later, when vapor cools high up."},
             {"text": "It all soaked into the ground", "feedback": "Some might, but on a sunny day much of it evaporates into the air."}]},
    ],
}

RAYS = {"plant": "Light spreads out from the sun in every direction, and some reaches the plant's leaves.",
        "ocean": "Sunlight only reaches the top layer of the ocean, so that's where phytoplankton live.",
        "water": "Sunlight warms the ocean's surface water."}
for key, lesson in (("plant", plant), ("ocean", ocean), ("water", water)):
    lesson["steps"].insert(1, {"type": "trace", "title": "Sun's rays", "structure": "sun", "part": "details",
                               "instruction": "Draw the sun's rays.", "note": {"text": RAYS[key]}})

for lesson in (plant, web, ocean, decomposers, water):
    save(lesson)
