"""Grade 3 life science · fossils (3-LS4-1), variation (3-LS4-2), camouflage (3-LS4-3),
environment and traits (3-LS3-2), inherited traits (3-LS3-1), animals in groups (3-LS2-1)."""
from lib import save, straight_arrow


def fish(x, y, length=70, facing=1):
    """A fish: a tapered body with a pointed nose, and a forked tail.
    facing 1 = swimming right, -1 = left."""
    f, L, h = facing, length, length * 0.42
    nose, joint = x + f * 0.5 * L, x - f * 0.38 * L
    body = (f"M {nose} {y} C {x + f * 0.3 * L} {y - 0.55 * h} {x - f * 0.2 * L} {y - 0.6 * h} {joint} {y} "
            f"C {x - f * 0.2 * L} {y + 0.6 * h} {x + f * 0.3 * L} {y + 0.55 * h} {nose} {y} Z")
    tail_back = x - f * 0.66 * L
    tail = [joint, y, tail_back, y - 0.5 * h, x - f * 0.56 * L, y, tail_back, y + 0.5 * h]
    return [{"path": body}, {"polygon": [round(v, 1) for v in tail]}]


# ---------------------------------------------------------------- How a fossil forms
def skeleton(x, y):
    return [{"line": [x - 60, y, x + 60, y]}, {"circle": [x + 74, y, 13]},
            {"line": [x + 35, y - 18, x + 35, y + 18]}, {"line": [x + 10, y - 20, x + 10, y + 20]},
            {"line": [x - 15, y - 18, x - 15, y + 18]}, {"line": [x - 40, y - 14, x - 40, y + 14]},
            {"polygon": [x - 60, y, x - 90, y - 18, x - 90, y + 18]}]


def wavy(x1, x2, y, amp=6):
    pts, n = [], 8
    for i in range(n + 1):
        pts += [x1 + (x2 - x1) * i / n, y + (amp if i % 2 else -amp)]
    return {"line": pts}


fossil = {
    "id": "g3-fossil-formation", "title": "How a fossil forms", "grade": "3", "subject": "Life science",
    "standard": "3-LS4-1", "minutes": 10,
    "keywords": ["fossil", "sediment", "rock layers", "erosion", "extinct", "evidence"],
    "printed": [{"text": "1", "at": [60, 80]}, {"text": "2", "at": [540, 80]}, {"text": "3", "at": [60, 560]}, {"text": "4", "at": [540, 560]}],
    "structures": [
        {"id": "lake", "name": "lake", "outlines": [wavy(80, 450, 140), {"line": [80, 400, 450, 400]}]},
        {"id": "deadFish", "name": "fish", "outlines": fish(270, 372, 150)},
        {"id": "buried", "name": "first layers", "outlines": [{"line": [560, 400, 930, 400]}, wavy(560, 930, 330), wavy(560, 930, 280)],
         "details": skeleton(740, 372)},
        {"id": "rock", "name": "rock layers",
         "outlines": [{"line": [80, 880, 450, 880]}, wavy(80, 450, 810), wavy(80, 450, 750), wavy(80, 450, 690), wavy(80, 450, 630)],
         "details": skeleton(270, 852)},
        {"id": "exposed", "name": "eroded hillside",
         "outlines": [{"path": "M 560 880 L 930 880 L 930 640 C 860 640 820 700 760 760 C 720 800 640 820 560 830 Z"}],
         "details": skeleton(740, 852)},
    ],
    "steps": [
        {"type": "trace", "title": "Lake", "structure": "lake", "instruction": "In picture 1, trace the water's surface and the lake bottom.",
         "note": {"text": "Most fossils form in water, where mud and sand can quickly cover a body.", "remember": "Fossils need fast burial."}},
        {"type": "trace", "title": "Fish", "structure": "deadFish", "instruction": "Trace the fish lying on the lake bottom.",
         "note": {"text": "When an animal dies, its body sinks. Soon only its hard parts, like bones, teeth and shells, are left."}},
        {"type": "trace", "title": "Mud layers", "structure": "buried", "instruction": "In picture 2, trace the lake bottom and the layers of mud on top.",
         "note": {"text": "Rivers wash mud and sand over the bones, layer after layer. These layers are called sediment."}},
        {"type": "trace", "title": "Bones", "structure": "buried", "part": "details", "instruction": "Draw the skeleton under the mud.",
         "note": {"text": "Buried bones are protected from scavengers and weather, so they don't fall apart."}},
        {"type": "trace", "title": "Rock layers", "structure": "rock", "instruction": "In picture 3, trace the many layers piled on top.",
         "note": {"text": "Over millions of years the weight of new layers presses the old ones into solid rock.",
                  "remember": "Deeper layers are older."}},
        {"type": "trace", "title": "Fossil", "structure": "rock", "part": "details", "instruction": "Draw the bones, now turned to stone.",
         "note": {"text": "Minerals from water seep into the bones and slowly replace them, turning them to stone. Now it's a fossil."}},
        {"type": "trace", "title": "Erosion", "structure": "exposed", "instruction": "In picture 4, trace the worn-away hillside.",
         "note": {"text": "The rock is pushed up into land. Wind and water wear it away until the fossil reaches the surface."}},
        {"type": "trace", "title": "Found!", "structure": "exposed", "part": "details", "instruction": "Draw the fossil near the surface.",
         "note": {"text": "Scientists study fossils to learn which organisms lived long ago and what their environments were like."}},
        {"type": "order", "title": "In order", "items": ["Fish dies and sinks", "Buried by mud", "Bones turn to stone", "Erosion exposes it"],
         "instruction": "Tap the steps in the order they happen.",
         "why": "A body is buried quickly, its bones are replaced by minerals deep in rock, and erosion later brings it to the surface.",
         "hint": "What has to cover the bones first?"},
        {"type": "choice", "title": "Explain", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "Scientists find a fish fossil on top of a dry mountain. What does that tell them?",
         "options": [
             {"text": "The area was once under water", "correct": True,
              "feedback": "Yes. Fish live in water, so this rock formed in a lake or sea long ago and was later pushed up."},
             {"text": "Fish used to live on mountains", "feedback": "Fish have always needed water. The land moved, not the fish's habits."},
             {"text": "A bird dropped it there", "feedback": "The fossil formed inside the rock layers, so it formed where it lies."},
             {"text": "It tells us nothing", "feedback": "Fossils are evidence of past life and past environments."}]},
    ],
}

# ---------------------------------------------------------------- Peppered moths (camouflage)
def moth(x, y):
    return {"polygon": [x, y - 8, x + 22, y - 24, x + 58, y - 14, x + 50, y + 6, x + 26, y + 24, x, y + 12,
                        x - 26, y + 24, x - 50, y + 6, x - 58, y - 14, x - 22, y - 24]}


moths = {
    "id": "g3-peppered-moths", "title": "Camouflage: peppered moths on bark", "grade": "3", "subject": "Life science",
    "standard": "3-LS4-3", "minutes": 8,
    "keywords": ["camouflage", "peppered moth", "adaptation", "survive", "habitat", "predator", "natural selection"],
    "colorMode": "illustration",
    "legend": [
        {"name": "Lichen-covered bark", "color": "#C9C6B5", "meaning": "Pale gray-green, before pollution"},
        {"name": "Soot-darkened bark", "color": "#3B3833", "meaning": "Blackened by factory smoke"},
        {"name": "Light moth", "color": "#E6E1D3", "meaning": "Pale with dark speckles (speckles not shown)"},
        {"name": "Dark moth", "color": "#2A2826", "meaning": "Almost black"},
    ],
    "structures": [
        {"id": "lightBark", "name": "pale tree trunk", "colorName": "pale bark", "outlines": [{"rect": [120, 110, 300, 790, 30]}], "fill": "#C9C6B5"},
        {"id": "darkBark", "name": "dark tree trunk", "colorName": "dark bark", "outlines": [{"rect": [580, 110, 300, 790, 30]}], "fill": "#3B3833"},
        {"id": "lightMoths", "name": "light moths", "colorName": "light moths", "pen": "fine",
         "outlines": [moth(270, 330), moth(730, 330)], "fill": "#E6E1D3"},
        {"id": "darkMoths", "name": "dark moths", "colorName": "dark moths", "pen": "fine",
         "outlines": [moth(270, 650), moth(730, 650)], "fill": "#2A2826"},
    ],
    "steps": [
        {"type": "trace", "title": "Pale trunk", "structure": "lightBark", "instruction": "Trace the tree trunk on the left.",
         "note": {"text": "In clean air, tree bark is covered in pale lichen. This was normal in England before the 1800s."}},
        {"type": "trace", "title": "Dark trunk", "structure": "darkBark", "instruction": "Trace the tree trunk on the right.",
         "note": {"text": "Factory smoke in the 1800s killed the lichen and coated bark in black soot."}},
        {"type": "trace", "title": "Light moths", "structure": "lightMoths", "instruction": "Trace a light moth on each tree.",
         "note": {"text": "Most peppered moths were pale and speckled, a perfect match for lichen-covered bark.",
                  "remember": "Camouflage: blending in to stay hidden."}},
        {"type": "trace", "title": "Dark moths", "structure": "darkMoths", "instruction": "Trace a dark moth on each tree.",
         "note": {"text": "A few peppered moths are born dark. On pale bark, birds spot and eat them easily."}},
        {"type": "color", "title": "Color", "structures": ["lightBark", "darkBark", "lightMoths", "darkMoths"],
         "instruction": "Color the trees and moths, then look at which moths are easy to see."},
        {"type": "choice", "title": "Spot the moth", "instruction": "Look at the colored trees.", "showsDiagram": True,
         "question": "On the dark, sooty tree, which moth is a hungry bird more likely to catch?",
         "options": [
             {"text": "The light moth", "correct": True, "feedback": "Yes. It stands out against the dark bark, while the dark moth blends in."},
             {"text": "The dark moth", "feedback": "The dark moth matches the sooty bark, so it's hidden. The light one stands out."},
             {"text": "Both equally", "feedback": "Look at the colors: one moth matches the bark and one doesn't."},
             {"text": "Neither: birds don't eat moths", "feedback": "Many birds eat moths. That's why camouflage matters."}]},
        {"type": "choice", "title": "Explain", "instruction": "Think about many generations.", "showsDiagram": True,
         "question": "As the trees got darker, what happened to the moths over many years?",
         "options": [
             {"text": "Dark moths became more common, because more of them survived to have young", "correct": True,
              "feedback": "Right. Dark moths survived better, so more young were dark. When the air was cleaned up, pale moths became common again."},
             {"text": "Each light moth turned dark", "feedback": "A moth can't change its color. More dark moths survived and passed their color on."},
             {"text": "All the moths died", "feedback": "The moths that matched the bark survived and kept the species going."},
             {"text": "Nothing changed", "feedback": "Scientists recorded a big change: dark moths went from rare to common."}]},
    ],
}

# ---------------------------------------------------------------- Beetle variation
def beetle(x, y):
    return [{"ellipse": [x, y + 10, 30, 44]}, {"circle": [x, y - 42, 15]}]


def beetle_legs(x, y):
    legs = []
    for dy in (-10, 12, 34):
        legs += [{"line": [x - 30, y + dy, x - 52, y + dy - 10]}, {"line": [x + 30, y + dy, x + 52, y + dy - 10]}]
    return legs + [{"line": [x, y - 30, x, y + 52]}]


gen1 = [(170, 300), (335, 300), (500, 300), (665, 300), (830, 300)]
gen2 = [(170, 720), (335, 720), (500, 720), (665, 720), (830, 720)]
beetles = {
    "id": "g3-beetle-variation", "title": "Variation: beetles of different colors", "grade": "3", "subject": "Life science",
    "standard": "3-LS4-2", "minutes": 9,
    "keywords": ["variation", "traits", "beetle", "survival", "advantage", "generations", "camouflage"],
    "colorMode": "illustration",
    "printed": [{"text": "Long ago", "at": [500, 170]}, {"text": "Many generations later", "at": [500, 590]}],
    "legend": [
        {"name": "Green beetle", "color": "#5E9E3E", "meaning": "Matches green leaves"},
        {"name": "Brown beetle", "color": "#7A5230", "meaning": "Stands out on green leaves"},
    ],
    "structures": [
        {"id": "greenOld", "name": "green beetles", "colorName": "green beetles",
         "outlines": beetle(*gen1[0]) + beetle(*gen1[2]), "fill": "#5E9E3E"},
        {"id": "brownOld", "name": "brown beetles", "colorName": "brown beetles",
         "outlines": beetle(*gen1[1]) + beetle(*gen1[3]) + beetle(*gen1[4]), "fill": "#7A5230",
         "details": sum((beetle_legs(*p) for p in gen1), [])},
        {"id": "greenNew", "name": "green beetles", "colorName": "green beetles",
         "outlines": sum((beetle(*p) for p in gen2[:4]), []), "fill": "#5E9E3E"},
        {"id": "brownNew", "name": "brown beetle", "colorName": "brown beetle",
         "outlines": beetle(*gen2[4]), "fill": "#7A5230", "details": sum((beetle_legs(*p) for p in gen2), [])},
    ],
    "steps": [
        {"type": "trace", "title": "Green beetles", "structure": "greenOld", "instruction": "In the top row, trace the two green beetles.",
         "note": {"text": "Beetles of the same kind can differ in color. Differences like this are called variation.",
                  "remember": "Same species, different traits."}},
        {"type": "trace", "title": "Brown beetles", "structure": "brownOld", "instruction": "Trace the three brown beetles in the top row.",
         "note": {"text": "Long ago, most of these beetles were brown. They live on green leaves."}},
        {"type": "trace", "title": "Legs", "structure": "brownOld", "part": "details", "instruction": "Draw the legs and wing line on every top-row beetle.",
         "note": {"text": "Like all insects, each beetle has six legs. Its hard front wings meet in a line down its back."}},
        {"type": "trace", "title": "Green beetles", "structure": "greenNew", "instruction": "In the bottom row, trace the four green beetles.",
         "note": {"text": "Birds eat the beetles they can see. Green beetles were harder to spot on leaves, so more survived and had young."}},
        {"type": "trace", "title": "Brown beetle", "structure": "brownNew", "instruction": "Trace the last beetle in the bottom row.",
         "note": {"text": "Young beetles inherit their parents' color. Over many generations, green became the common color.",
                  "remember": "Traits that help survival get passed on more."}},
        {"type": "trace", "title": "Legs", "structure": "brownNew", "part": "details", "instruction": "Draw the legs and wing line on every bottom-row beetle.",
         "note": {"text": "The beetles still look alike in every other way. Only the share of each color changed."}},
        {"type": "color", "title": "Color", "structures": ["greenOld", "brownOld", "greenNew", "brownNew"],
         "instruction": "Color the beetles to compare the two rows."},
        {"type": "choice", "title": "Explain", "instruction": "Compare the two rows.", "showsDiagram": True,
         "question": "Why are most beetles green many generations later?",
         "options": [
             {"text": "Green beetles were hidden from birds, so more survived to have young", "correct": True,
              "feedback": "Yes. Being green gave them an advantage on green leaves, and they passed the trait on."},
             {"text": "Brown beetles painted themselves green", "feedback": "Beetles can't change their color. More green ones survived and reproduced."},
             {"text": "Birds only eat green beetles", "feedback": "It's the opposite: birds catch the beetles they can see, the brown ones."},
             {"text": "Leaves made the beetles green", "feedback": "Color is inherited from parents, not caused by leaves."}]},
    ],
}

# ---------------------------------------------------------------- Plants in light vs dark
sun_rays = [{"line": [140 + dx * 46, 150 + dy * 46, 140 + dx * 72, 150 + dy * 72]}
            for dx, dy in [(1, 0), (0.7, 0.7), (0, 1), (-0.7, 0.7), (-1, 0), (-0.7, -0.7), (0, -1), (0.7, -0.7)]]
light = {
    "id": "g3-plant-light-dark", "title": "Environment changes traits: plant in light vs dark", "grade": "3", "subject": "Life science",
    "standard": "3-LS3-2", "minutes": 8,
    "keywords": ["environment", "traits", "light", "chlorophyll", "etiolated", "plant growth"],
    "colorMode": "illustration",
    "legend": [
        {"name": "Leaves in light", "color": "#4F8F34", "meaning": "Deep green with chlorophyll"},
        {"name": "Leaves in the dark", "color": "#E3DD9A", "meaning": "Pale yellow: no chlorophyll made"},
        {"name": "Flowerpot", "color": "#C0643A", "meaning": "Terracotta clay"},
    ],
    "structures": [
        {"id": "sun", "name": "sun", "outlines": [{"circle": [140, 150, 34]}], "details": sun_rays},
        {"id": "cupboard", "name": "dark cupboard", "pen": "bold", "outlines": [{"rect": [540, 90, 400, 830, 10]}]},
        {"id": "pots", "name": "pots", "colorName": "pots",
         "outlines": [{"polygon": [200, 760, 400, 760, 370, 890, 230, 890]}, {"polygon": [640, 760, 840, 760, 810, 890, 670, 890]}],
         "fill": "#C0643A"},
        {"id": "greenPlant", "name": "plant in the light", "colorName": "green leaves",
         "outlines": [{"path": "M 300 640 C 250 600 214 612 208 632 C 240 652 276 650 300 640 Z"},
                      {"path": "M 300 590 C 350 550 386 562 392 582 C 360 602 324 600 300 590 Z"},
                      {"path": "M 300 690 C 352 660 382 676 386 694 C 352 712 320 706 300 690 Z"}],
         "fill": "#4F8F34", "details": [{"line": [300, 760, 300, 560]}]},
        {"id": "palePlant", "name": "plant in the dark", "colorName": "pale leaves",
         "outlines": [{"path": "M 740 240 C 712 222 692 228 690 240 C 708 252 728 250 740 240 Z"},
                      {"path": "M 740 300 C 768 282 788 288 790 300 C 772 312 752 310 740 300 Z"}],
         "fill": "#E3DD9A", "details": [{"line": [740, 760, 744, 600, 736, 440, 742, 220]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "The left plant grows in sunlight. Plants use light to make their food."}},
        {"type": "trace", "title": "Sunlight", "structure": "sun", "part": "details", "instruction": "Draw the sun's rays.",
         "note": {"text": "Light also triggers the plant to make chlorophyll, the green pigment in its leaves."}},
        {"type": "trace", "title": "Dark cupboard", "structure": "cupboard", "instruction": "Trace the cupboard around the right side.",
         "note": {"text": "The right plant grows from the same kind of seed, but in a dark cupboard with no light."}},
        {"type": "trace", "title": "Pots", "structure": "pots", "instruction": "Trace both flowerpots.",
         "note": {"text": "Same seeds, same soil, same water. The only difference is light. That makes it a fair test."}},
        {"type": "trace", "title": "Plant in light", "structure": "greenPlant", "instruction": "Trace the leaves of the plant in the light.",
         "note": {"text": "In light, the plant grows short and sturdy, with large, deep-green leaves."}},
        {"type": "trace", "title": "Stem", "structure": "greenPlant", "part": "details", "instruction": "Draw its short, strong stem.",
         "note": {"text": "A sturdy stem holds the leaves up toward the light."}},
        {"type": "trace", "title": "Plant in the dark", "structure": "palePlant", "instruction": "Trace the small leaves at the top of the dark plant.",
         "note": {"text": "In the dark, leaves stay small and pale yellow, because the plant can't make chlorophyll without light.",
                  "remember": "No light, no green."}},
        {"type": "trace", "title": "Long stem", "structure": "palePlant", "part": "details", "instruction": "Draw its long, thin stem.",
         "note": {"text": "It grows tall and spindly, stretching to find light, using up the food stored in its seed."}},
        {"type": "color", "title": "Color", "structures": ["pots", "greenPlant", "palePlant"],
         "instruction": "Color both plants to compare them."},
        {"type": "choice", "title": "Explain", "instruction": "Compare the two plants.", "showsDiagram": True,
         "question": "Both plants came from the same kind of seed. Why do they look so different?",
         "options": [
             {"text": "Their environment was different: one had light and one didn't", "correct": True,
              "feedback": "Yes. Plants inherit traits from their parents, but their environment changes how those traits show up."},
             {"text": "They had different parents", "feedback": "They're the same kind of plant. Only the light was different."},
             {"text": "The pale one got too much water", "feedback": "Both got the same water. Light was the only difference."},
             {"text": "The pale one is a different species", "feedback": "Same seeds, same species. The darkness changed how it grew."}]},
    ],
}

# ---------------------------------------------------------------- Inherited flower color (Mendel's peas)
def pea_flower(x, y):
    return [{"path": f"M {x - 44} {y} C {x - 44} {y - 60} {x + 44} {y - 60} {x + 44} {y} Z"},
            {"ellipse": [x - 22, y + 18, 24, 16]}, {"ellipse": [x + 22, y + 18, 24, 16]}]


parents = [(320, 250), (680, 250)]
kids = [(200, 720), (400, 720), (600, 720), (800, 720)]
inherit = {
    "id": "g3-inherited-flower-color", "title": "Inherited traits: flower color in a family", "grade": "3", "subject": "Life science",
    "standard": "3-LS3-1", "minutes": 8,
    "keywords": ["inheritance", "traits", "parents", "offspring", "pea plant", "Mendel", "flower color"],
    "colorMode": "illustration",
    "printed": [{"text": "Parents", "at": [500, 130]}, {"text": "Offspring", "at": [500, 820]}],
    "legend": [
        {"name": "Purple pea flower", "color": "#7B4F9E", "meaning": "Purple petals"},
        {"name": "White pea flower", "color": "#F4F1EA", "meaning": "White petals"},
    ],
    "structures": [
        {"id": "purpleParent", "name": "purple parent", "colorName": "purple flower", "outlines": pea_flower(*parents[0]), "fill": "#7B4F9E"},
        {"id": "whiteParent", "name": "white parent", "colorName": "white flower", "outlines": pea_flower(*parents[1]), "fill": "#F4F1EA"},
        {"id": "family", "name": "family lines",
         "outlines": [{"line": [320, 300, 320, 420, 680, 420, 680, 300]}, {"line": [500, 420, 500, 520]},
                      {"line": [200, 640, 200, 520, 800, 520, 800, 640]}, {"line": [400, 520, 400, 640]}, {"line": [600, 520, 600, 640]}]},
        {"id": "offspring", "name": "offspring", "colorName": "offspring flowers", "outlines": sum((pea_flower(*k) for k in kids), []),
         "fill": "#7B4F9E"},
    ],
    "steps": [
        {"type": "trace", "title": "Purple parent", "structure": "purpleParent", "instruction": "Trace the first parent's flower.",
         "note": {"text": "Pea plants were studied by Gregor Mendel in the 1860s. This parent plant has purple flowers."}},
        {"type": "trace", "title": "White parent", "structure": "whiteParent", "instruction": "Trace the second parent's flower.",
         "note": {"text": "This parent has white flowers. Flower color is a trait, a feature passed from parents to offspring."}},
        {"type": "trace", "title": "Family lines", "structure": "family", "instruction": "Draw the lines joining the parents to their offspring.",
         "note": {"text": "A family tree shows who came from whom. All four offspring come from these two parents."}},
        {"type": "trace", "title": "Offspring", "structure": "offspring", "instruction": "Trace the four offspring flowers.",
         "note": {"text": "Offspring inherit traits from both parents, so they look like their parents.",
                  "remember": "Traits are passed from parents to offspring."}},
        {"type": "color", "title": "Color", "structures": ["purpleParent", "whiteParent", "offspring"],
         "instruction": "Color the flowers to see which color the offspring inherited."},
        {"type": "choice", "title": "Explain", "instruction": "Look at the colors.", "showsDiagram": True,
         "question": "Mendel saw that when he crossed purple and white pea plants, all the offspring were purple. What does that show?",
         "options": [
             {"text": "Offspring inherit traits from their parents, and some traits can hide others", "correct": True,
              "feedback": "Yes. The offspring got a color from their parents. White was hidden this time, but it can reappear in later generations."},
             {"text": "The white parent passed on nothing", "feedback": "Both parents passed on traits. The white trait was hidden, not lost: it shows up again in the next generation."},
             {"text": "Flower color is random", "feedback": "Mendel found clear patterns. Color is inherited, not random."},
             {"text": "Sunlight turned them purple", "feedback": "These plants grew in the same conditions. The color came from their parents."}]},
    ],
}

# ---------------------------------------------------------------- School of fish
school_positions = [(600, 360), (770, 380), (650, 500), (820, 520), (600, 640), (770, 660)]
school = {
    "id": "g3-school-of-fish", "title": "Animals in groups: a school of fish", "grade": "3", "subject": "Life science",
    "standard": "3-LS2-1", "minutes": 7,
    "keywords": ["group", "school", "fish", "predator", "survival", "behavior", "herd", "flock"],
    "structures": [
        {"id": "school", "name": "school of fish", "pen": "fine", "outlines": sum((fish(x, y, 120, 1) for x, y in school_positions), [])},
        {"id": "predator", "name": "predator", "pen": "bold", "outlines": fish(250, 500, 260, 1),
         "details": [{"circle": [330, 490, 9]}, {"line": [352, 512, 376, 506]}]},
        {"id": "escape", "name": "escape arrows", "outlines": straight_arrow(870, 300, 950, 230) + straight_arrow(880, 740, 950, 810)},
    ],
    "steps": [
        {"type": "trace", "title": "School of fish", "structure": "school", "instruction": "Trace every small fish in the group.",
         "note": {"text": "Many small fish swim close together in a group called a school. They turn and move as one.",
                  "remember": "Safety in numbers."}},
        {"type": "trace", "title": "Predator", "structure": "predator", "instruction": "Trace the big fish hunting them.",
         "note": {"text": "A predator hunts other animals for food. A big fish like a tuna hunts small fish."}},
        {"type": "trace", "title": "Eye and mouth", "structure": "predator", "part": "details", "instruction": "Draw the predator's eye and mouth.",
         "note": {"text": "A predator needs to pick out one fish to catch, but a swirling school makes that hard."}},
        {"type": "trace", "title": "Escape", "structure": "escape", "instruction": "Draw the arrows showing the school splitting to escape.",
         "note": {"text": "Many eyes spot danger sooner, and the group splits and swirls to confuse the predator.",
                  "remember": "Groups help animals find food, defend themselves and survive."}},
        {"type": "choice", "title": "Explain", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "How does swimming in a school help small fish survive?",
         "options": [
             {"text": "It's harder for a predator to pick out and catch one fish", "correct": True,
              "feedback": "Yes. Many moving fish confuse the predator, and many eyes spot it sooner."},
             {"text": "The school can fight off the big fish", "feedback": "Small fish can't fight a tuna. They escape by confusing it."},
             {"text": "Fish in a school don't need food", "feedback": "They still need food. Groups can even help them find it."},
             {"text": "It makes the fish grow bigger", "feedback": "Groups help with safety and finding food, not size."}]},
        {"type": "choice", "title": "Other groups", "instruction": "Think about other animals.", "showsDiagram": False,
         "question": "Which of these is another animal group that helps its members survive?",
         "options": [
             {"text": "A wolf pack hunting together", "correct": True,
              "feedback": "Yes. Wolves cooperate to catch animals much bigger than one wolf could."},
             {"text": "A single bear sleeping in a cave", "feedback": "That's one animal alone. Look for animals working together."},
             {"text": "A spider alone in its web", "feedback": "Most spiders hunt alone. A group means animals working together."},
             {"text": "A rock covered in moss", "feedback": "A rock isn't alive. Look for animals in a group."}]},
    ],
}

for lesson in (fossil, moths, beetles, light, inherit, school):
    save(lesson)
