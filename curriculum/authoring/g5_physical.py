"""Grade 5 physical science · particles of matter (5-PS1-1), conservation of mass (5-PS1-2),
salt dissolving (5-PS1-4), gravity toward Earth's center (5-PS2-1), and energy from the sun
in food (5-PS3-1).

Facts checked against OpenStax Chemistry 2e, University Physics Volume 1 and Biology 2e
(searched with curriculum/tools/openstax.py).
"""
import math

from lib import save, straight_arrow


def ngss(code, text):
    return {"title": f"NGSS {code}: {text}"}


def chem(section, slug, title):
    return {"title": f"OpenStax Chemistry 2e, {section} {title}",
            "url": f"https://openstax.org/books/chemistry-2e/pages/{slug}"}


PHASES = chem("1.2", "1-2-phases-and-classification-of-matter", "Phases and Classification of Matter")
IMF = chem("10.1", "10-1-intermolecular-forces", "Intermolecular Forces")
DISSOLVING = chem("11.1", "11-1-the-dissolution-process", "The Dissolution Process")
CARBONATES = chem("18.6", "18-6-occurrence-preparation-and-properties-of-carbonates",
                  "Occurrence, Preparation, and Properties of Carbonates (baking soda and acids)")


def dots(centers, radius):
    return [{"circle": [x, y, radius]} for x, y in centers]


# ---------------------------------------------------------------- Particles in a solid, liquid and gas
solid_pts = [(131 + 36 * c, 676 - 36 * row) for row in range(3) for c in range(4)]
liquid_pts = [(410, 676), (446, 670), (488, 678), (530, 672), (574, 676),
              (428, 636), (470, 640), (514, 634), (556, 640), (598, 632), (452, 598), (540, 600)]
gas_pts = [(740, 450), (880, 480), (800, 560), (720, 660), (900, 650)]
states = {
    "id": "g5-states-of-matter", "title": "Particles in a solid, liquid and gas", "grade": "5", "subject": "Chemistry",
    "standard": "5-PS1-1", "minutes": 8,
    "sources": [ngss("5-PS1-1", "Develop a model to describe that matter is made of particles too small to be seen"), PHASES, IMF],
    "keywords": ["matter", "particles", "solid", "liquid", "gas", "states of matter", "model", "air", "shape", "volume"],
    "structures": [
        {"id": "solid", "name": "solid", "outlines": [{"rect": [60, 400, 250, 300, 8]}], "details": dots(solid_pts, 16)},
        {"id": "liquidBox", "name": "liquid's container", "outlines": [{"rect": [375, 400, 250, 300, 8]}]},
        {"id": "liquid", "name": "liquid", "outlines": [{"line": [375, 560, 625, 560]}], "details": dots(liquid_pts, 16)},
        {"id": "gas", "name": "gas", "outlines": [{"rect": [690, 400, 250, 300, 8]}], "details": dots(gas_pts, 16)},
    ],
    "steps": [
        {"type": "trace", "title": "First box", "structure": "solid", "instruction": "Trace the first box.",
         "note": {"text": "All matter is made of particles far too small to see. Each dot in this model stands for one particle."}},
        {"type": "trace", "title": "Solid", "structure": "solid", "part": "details", "instruction": "Dab the particles, packed in neat rows.",
         "note": {"text": "In a solid, particles are packed tightly in a regular pattern. They only jiggle in place, so a solid keeps its shape.",
                  "remember": "Solid: tight rows, own shape."}},
        {"type": "trace", "title": "Second box", "structure": "liquidBox", "instruction": "Trace the second box.",
         "note": {"text": "Next, the same kind of model for a liquid, like water in a cup."}},
        {"type": "trace", "title": "Surface", "structure": "liquid", "instruction": "Draw the flat top of the liquid.",
         "note": {"text": "A liquid flows and takes the shape of its container, with a flat top."}},
        {"type": "trace", "title": "Liquid", "structure": "liquid", "part": "details", "instruction": "Dab the particles, close but jumbled.",
         "note": {"text": "In a liquid, particles are close together but not in rows. They slide past each other, so a liquid can flow.",
                  "remember": "Liquid: close, jumbled, flows."}},
        {"type": "trace", "title": "Third box", "structure": "gas", "instruction": "Trace the third box.",
         "note": {"text": "Last, a gas, like the air in a closed box."}},
        {"type": "trace", "title": "Gas", "structure": "gas", "part": "details", "instruction": "Dab the particles, spread far apart.",
         "note": {"text": "In a gas, particles are far apart and zoom around. A gas spreads out to fill its whole container.",
                  "remember": "Gas: far apart, fills its container."}},
        {"type": "label", "title": "Label the states", "instruction": "Pick the right name for each numbered box.",
         "targets": [
             {"n": 1, "at": [185, 450], "answer": "Solid", "role": "Particles packed in rows."},
             {"n": 2, "at": [500, 450], "answer": "Liquid", "role": "Particles close but jumbled.",
              "mistakes": {"Solid": "These particles aren't in neat rows, and they have a flat top like water. It's a liquid."}},
             {"n": 3, "at": [815, 610], "answer": "Gas", "role": "Particles far apart."}],
         "vocabulary": ["Solid", "Liquid", "Gas", "Rock"]},
        {"type": "choice", "title": "Explain", "instruction": "Use your model.", "showsDiagram": True,
         "question": "Why does a gas fill its whole container, but a solid keeps its shape?",
         "options": [
             {"text": "Gas particles are far apart and move freely; solid particles are packed in place", "correct": True,
              "feedback": "Yes. Solid particles only jiggle in place. Gas particles zoom around and spread out to fill the space."},
             {"text": "Gas particles are bigger", "feedback": "The particles aren't bigger. They're just much farther apart and free to move."},
             {"text": "Solids have no particles", "feedback": "Solids are made of particles too, packed tightly in a regular pattern."},
             {"text": "Gas is lighter than air", "feedback": "The difference is how the particles are arranged: far apart in a gas, packed in a solid."}]},
        {"type": "choice", "title": "Invisible matter", "instruction": "Think about air.", "showsDiagram": False,
         "question": "You can't see air. How can you tell air is made of matter?",
         "options": [
             {"text": "Blowing air into a balloon makes it get bigger", "correct": True,
              "feedback": "Right. The air particles take up space and push the balloon out, even though each one is too small to see."},
             {"text": "You can't: air is empty space", "feedback": "Air is matter. A balloon fills up because air particles take up space."},
             {"text": "Air has a color", "feedback": "Air has no color. But it takes up space, which is why a balloon inflates."},
             {"text": "Air stays in one shape", "feedback": "Air is a gas, so it spreads out. It still takes up space, which inflates a balloon."}]},
    ],
}

# ---------------------------------------------------------------- Conservation of mass on a balance
def scale(x):
    return [{"rect": [x, 620, 320, 120, 12]}, {"rect": [x + 70, 645, 180, 70, 8]}]


def jar(x):
    return [{"line": [x + 60, 376, x + 60, 612, x + 260, 612, x + 260, 376]}, {"rect": [x + 50, 350, 220, 26, 6]}]


mass = {
    "id": "g5-conservation-of-mass", "title": "Ice melting on a scale: mass stays the same", "grade": "5", "subject": "Chemistry",
    "standard": "5-PS1-2", "minutes": 7,
    "sources": [ngss("5-PS1-2", "Measure and graph quantities to provide evidence that regardless of the type of change that occurs "
                                 "when heating, cooling, or mixing substances, the total weight of matter is conserved"), PHASES],
    "keywords": ["conservation of mass", "conservation of matter", "mass", "weight", "scale", "melting", "ice", "water",
                 "evaporation", "physical change"],
    "printed": [{"text": "Before", "at": [250, 290]}, {"text": "After", "at": [750, 290]},
                {"text": "100 g", "at": [250, 682], "size": 40}, {"text": "? g", "at": [750, 682], "size": 40}],
    "structures": [
        {"id": "scales", "name": "scales", "pen": "bold", "outlines": scale(90) + scale(590)},
        {"id": "jars", "name": "jars and lids", "outlines": jar(90) + jar(590)},
        {"id": "ice", "name": "ice cube", "outlines": [{"rect": [210, 528, 80, 80, 8]}]},
        {"id": "water", "name": "melted water", "outlines": [{"line": [652, 560, 848, 560]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Scales", "structure": "scales", "instruction": "Trace both scales and their screens.",
         "note": {"text": "A scale measures how much matter something has. We'll weigh the same jar before and after a change."}},
        {"type": "trace", "title": "Jars", "structure": "jars", "instruction": "Trace both jars and their lids.",
         "note": {"text": "The lids seal the jars, so nothing can get in or out.",
                  "remember": "Sealed: nothing in, nothing out."}},
        {"type": "trace", "title": "Ice cube", "structure": "ice", "instruction": "Trace the ice cube in the first jar.",
         "note": {"text": "Before: a solid ice cube in a sealed jar. The scale reads 100 grams."}},
        {"type": "trace", "title": "Water", "structure": "water", "instruction": "Draw the top of the water in the second jar.",
         "note": {"text": "After: the ice has melted into liquid water. Its particles moved apart, but none disappeared.",
                  "remember": "Melting changes the state, not the amount."}},
        {"type": "choice", "title": "Predict", "instruction": "Read the scales.", "showsDiagram": True,
         "question": "The ice melted in the sealed jar. What will the After scale read?",
         "options": [
             {"text": "100 g, the same as before", "correct": True,
              "feedback": "Yes. When matter changes from solid to liquid, the total amount of matter stays the same."},
             {"text": "Less than 100 g, because water is lighter than ice", "feedback": "The same particles are still in the jar, so the mass is still 100 g."},
             {"text": "More than 100 g, because water takes up the jar", "feedback": "No new matter got in: the jar is sealed. It still reads 100 g."},
             {"text": "0 g, because the ice is gone", "feedback": "The ice didn't vanish. It turned into water, which still weighs 100 g."}]},
        {"type": "choice", "title": "Explain", "instruction": "Now open the jar.", "showsDiagram": False,
         "question": "You take the lid off and leave the jar for a week. Now it weighs less. What happened?",
         "options": [
             {"text": "Some water evaporated: it left as a gas into the air", "correct": True,
              "feedback": "Right. The water particles weren't destroyed. They escaped into the air as a gas, so the jar holds less."},
             {"text": "Some water was destroyed", "feedback": "Matter isn't destroyed. The water evaporated and went into the air as a gas."},
             {"text": "The scale broke", "feedback": "The scale is fine. With the lid off, some water evaporated into the air."},
             {"text": "The jar got lighter", "feedback": "The jar is the same. Some water left it as a gas, so there's less matter inside."}]},
        {"type": "choice", "title": "Fair test", "instruction": "Think like a scientist.", "showsDiagram": True,
         "question": "Why did we keep the lid on while the ice melted?",
         "options": [
             {"text": "So no matter could get in or out of the jar", "correct": True,
              "feedback": "Yes. Sealing the jar means any change on the scale would show matter appearing or disappearing. None did."},
             {"text": "To keep the ice cold", "feedback": "The lid is there so nothing escapes or gets in, so we can compare fairly."},
             {"text": "To make the ice melt faster", "feedback": "The lid makes the test fair: no matter can escape or get in."},
             {"text": "Lids make things heavier", "feedback": "Both jars have a lid, so that's the same. The lid stops matter escaping."}]},
    ],
}

# ---------------------------------------------------------------- Salt dissolving in water
crystals = [{"rect": [x, 728, 16, 16, 2]} for x in (170, 206, 238, 272, 314)]
dissolved = dots([(640, 500), (720, 530), (800, 490), (870, 560), (660, 610), (720, 640), (850, 690), (700, 710)], 6)
salt = {
    "id": "g5-salt-dissolving", "title": "Salt dissolving in water", "grade": "5", "subject": "Chemistry",
    "standard": "5-PS1-4", "minutes": 7,
    "sources": [ngss("5-PS1-4", "Conduct an investigation to determine whether the mixing of two or more substances results in new "
                                 "substances"), DISSOLVING, CARBONATES],
    "keywords": ["dissolving", "dissolve", "salt", "water", "solution", "mixture", "mixing", "particles", "new substance",
                 "stirring"],
    "printed": [{"text": "Just added", "at": [250, 300], "size": 40}, {"text": "Stirred", "at": [750, 300], "size": 40}],
    "structures": [
        {"id": "glasses", "name": "glasses", "pen": "bold",
         "outlines": [{"line": [100, 380, 110, 760, 390, 760, 400, 380]}, {"line": [600, 380, 610, 760, 890, 760, 900, 380]}]},
        {"id": "water", "name": "water", "outlines": [{"line": [103, 460, 397, 460]}, {"line": [603, 460, 897, 460]}]},
        {"id": "crystals", "name": "salt crystals", "outlines": crystals},
        {"id": "spoon", "name": "spoon", "outlines": [{"line": [880, 330, 756, 680]}, {"ellipse": [748, 702, 14, 24]}]},
        {"id": "dissolved", "name": "dissolved salt", "outlines": dissolved},
    ],
    "steps": [
        {"type": "trace", "title": "Glasses", "structure": "glasses", "instruction": "Trace the two glasses.",
         "note": {"text": "Two glasses of water, each with the same spoonful of salt. Only the second one gets stirred."}},
        {"type": "trace", "title": "Water", "structure": "water", "instruction": "Draw the top of the water in each glass.",
         "note": {"text": "Water is the liquid the salt will mix into."}},
        {"type": "trace", "title": "Salt crystals", "structure": "crystals", "instruction": "Trace the salt crystals at the bottom of the first glass.",
         "note": {"text": "Just added, the salt sits at the bottom as tiny solid crystals you can see."}},
        {"type": "trace", "title": "Spoon", "structure": "spoon", "instruction": "Trace the spoon stirring the second glass.",
         "note": {"text": "Stirring helps the water break the crystals apart faster."}},
        {"type": "trace", "title": "Dissolved salt", "structure": "dissolved", "instruction": "Dab the salt particles spread through the water.",
         "note": {"text": "The salt has dissolved: it split into particles too small to see, spread evenly through the water. They won't settle out.",
                  "remember": "Dissolved = spread out, too small to see."}},
        {"type": "choice", "title": "Explain", "instruction": "Look at the stirred glass.", "showsDiagram": True,
         "question": "The salt in the stirred glass seems to disappear. Where did it go?",
         "options": [
             {"text": "It broke into particles too small to see, spread through the water", "correct": True,
              "feedback": "Yes. The salt is still there. Its particles are mixed among the water's particles, too small to see."},
             {"text": "It was destroyed", "feedback": "Matter isn't destroyed. The salt split into tiny particles spread through the water."},
             {"text": "It floated away into the air", "feedback": "Salt doesn't escape into the air. It's spread through the water in tiny particles."},
             {"text": "It turned into water", "feedback": "It's still salt. Its particles are just mixed in among the water."}]},
        {"type": "choice", "title": "New substance?", "instruction": "Compare two kinds of mixing.", "showsDiagram": False,
         "question": "Mixing baking soda with vinegar makes bubbles of a new gas. Does mixing salt into water make a new substance?",
         "options": [
             {"text": "No, it's still salt and water, just mixed together", "correct": True,
              "feedback": "Right. Dissolving makes a mixture. Baking soda and an acid like vinegar react to make carbon dioxide gas, a new substance."},
             {"text": "Yes, because the salt vanished", "feedback": "The salt only spread out into tiny particles. It's still salt mixed with water."},
             {"text": "Yes, because it makes bubbles", "feedback": "Salt in water doesn't fizz. That's baking soda and vinegar, which do make a new gas."},
             {"text": "Every mixture makes a new substance", "feedback": "Some mixing does, like baking soda and vinegar. Salt and water just mix."}]},
        {"type": "choice", "title": "Find the evidence", "instruction": "Think about mass.", "showsDiagram": False,
         "question": "You weigh salt and water, then mix them. How much will the salty water weigh?",
         "options": [
             {"text": "The same as the salt and water together before", "correct": True,
              "feedback": "Yes. When substances mix, the total amount of matter stays the same. That's evidence the salt is still there."},
             {"text": "Just as much as the water", "feedback": "The salt is still there, so it still counts. The total stays the same."},
             {"text": "Less, because the salt disappeared", "feedback": "The salt only looks gone. The salty water weighs as much as both did before."},
             {"text": "More, because mixing adds matter", "feedback": "Mixing doesn't add matter. The total stays exactly the same."}]},
    ],
}

# ---------------------------------------------------------------- Gravity pulls toward Earth's center
GRAVITY = {"title": "OpenStax University Physics Volume 1, 13.2 Gravitation Near Earth's Surface",
           "url": "https://openstax.org/books/university-physics-volume-1/pages/13-2-gravitation-near-earths-surface"}
CX, CY, R = 500, 520, 300


def around(angle, radius):
    a = math.radians(angle)
    return round(CX + radius * math.cos(a), 1), round(CY + radius * math.sin(a), 1)


ball_angles = (-90, 180, 30, 135)
gravity = {
    "id": "g5-gravity-down", "title": "Gravity pulls toward Earth's center", "grade": "5", "subject": "Physics",
    "standard": "5-PS2-1", "minutes": 7,
    "sources": [ngss("5-PS2-1", "Support an argument that the gravitational force exerted by Earth on objects is directed down"), GRAVITY],
    "keywords": ["gravity", "gravitational force", "force", "down", "Earth", "center", "falling", "weight", "planet"],
    "structures": [
        {"id": "earth", "name": "Earth", "pen": "bold", "outlines": [{"circle": [CX, CY, R]}]},
        {"id": "center", "name": "Earth's center", "outlines": [{"circle": [CX, CY, 12]}]},
        {"id": "balls", "name": "balls", "outlines": [{"circle": [*around(a, R + 50), 24]} for a in ball_angles]},
        {"id": "pulls", "name": "pull of gravity", "pen": "bold",
         "outlines": [shape for a in ball_angles for shape in straight_arrow(*around(a, R - 30), *around(a, R - 170))]},
    ],
    "steps": [
        {"type": "trace", "title": "Earth", "structure": "earth", "instruction": "Trace the round Earth.",
         "note": {"text": "Earth is a giant ball. Its gravity pulls on everything: you, a dropped ball, the ocean, even the air.",
                  "remember": "Gravity pulls on everything."}},
        {"type": "trace", "title": "Center", "structure": "center", "instruction": "Trace the dot at Earth's center.",
         "note": {"text": "A round planet pulls as if all its mass were at its center."}},
        {"type": "trace", "title": "Balls", "structure": "balls", "instruction": "Trace the four balls dropped in different places.",
         "note": {"text": "Each ball is dropped by someone standing on a different part of Earth."}},
        {"type": "trace", "title": "Gravity's pull", "structure": "pulls", "instruction": "Draw the four arrows pointing toward Earth's center.",
         "note": {"text": "Every ball falls toward Earth's center. That direction is what we call down, wherever we stand.",
                  "remember": "Down = toward Earth's center."}},
        {"type": "label", "title": "Label the model", "instruction": "Pick the right name for each numbered part.",
         "targets": [
             {"n": 1, "at": [CX, CY + 12], "answer": "Earth's center", "role": "Where gravity points."},
             {"n": 2, "at": [*around(-90, R - 100)], "answer": "Gravity", "role": "The pull on the ball."},
             {"n": 3, "at": [*around(180, R + 50)], "answer": "Ball", "role": "Falls toward the center."}],
         "vocabulary": ["Earth's center", "Gravity", "Ball", "North Pole"],
         "commonMistakes": {"North Pole": "Gravity doesn't point toward the North Pole. It pulls toward Earth's center from everywhere."}},
        {"type": "choice", "title": "Argue", "instruction": "Use the model.", "showsDiagram": True,
         "question": "A child on the other side of the world drops a ball. Which way does it fall?",
         "options": [
             {"text": "Toward Earth's center, which is down for them", "correct": True,
              "feedback": "Yes. Gravity always pulls toward Earth's center, so down points at the center from every place on Earth."},
             {"text": "Up into space", "feedback": "Gravity pulls toward Earth's center from everywhere, so it falls down toward the ground."},
             {"text": "Toward the North Pole", "feedback": "Gravity pulls toward Earth's center, not toward any pole."},
             {"text": "Sideways", "feedback": "Look at the arrows: each points to the center. That's down for whoever drops the ball."}]},
        {"type": "choice", "title": "Explain", "instruction": "One more about down.", "showsDiagram": True,
         "question": "Why don't people at the bottom of the globe fall off Earth?",
         "options": [
             {"text": "Gravity pulls them toward Earth's center too", "correct": True,
              "feedback": "Right. There's no real bottom of Earth. Gravity pulls everyone toward the center, so their feet stay on the ground."},
             {"text": "They hold on tight", "feedback": "No holding needed: gravity pulls them toward Earth's center, just like us."},
             {"text": "Gravity only works at the top", "feedback": "Gravity works all around Earth, always toward its center."},
             {"text": "They wear heavy shoes", "feedback": "Shoes don't matter. Gravity pulls everyone toward Earth's center."}]},
    ],
}

# ---------------------------------------------------------------- Energy from the sun, through a plant, into an animal
PHOTO = {"title": "OpenStax Biology 2e, 8.1 Overview of Photosynthesis",
         "url": "https://openstax.org/books/biology-2e/pages/8-1-overview-of-photosynthesis"}
ECOSYSTEMS = {"title": "OpenStax Biology 2e, 46.1 Ecology of Ecosystems",
              "url": "https://openstax.org/books/biology-2e/pages/46-1-ecology-of-ecosystems"}
sun_rays = [{"line": [round(150 + 86 * math.cos(math.radians(a)), 1), round(180 + 86 * math.sin(math.radians(a)), 1),
                      round(150 + 120 * math.cos(math.radians(a)), 1), round(180 + 120 * math.sin(math.radians(a)), 1)]}
            for a in range(0, 360, 45)]
energy = {
    "id": "g5-energy-from-sun", "title": "Energy flow: sun to plant to animal", "grade": "5", "subject": "Life science",
    "standard": "5-PS3-1", "minutes": 7,
    "sources": [ngss("5-PS3-1", "Use models to describe that energy in animals' food (used for body repair, growth, motion, and to "
                                 "maintain body warmth) was once energy from the sun"), PHOTO, ECOSYSTEMS],
    "keywords": ["energy", "sun", "sunlight", "plant", "food", "animal", "rabbit", "photosynthesis", "energy flow",
                 "food chain", "producer", "consumer"],
    "structures": [
        {"id": "sun", "name": "sun", "pen": "bold", "outlines": [{"circle": [150, 180, 68]}], "details": sun_rays},
        {"id": "ground", "name": "ground", "outlines": [{"line": [60, 800, 940, 800]}]},
        {"id": "plant", "name": "plant", "outlines": [
            {"line": [420, 800, 420, 600]},
            {"path": "M 420 712 C 384 668 336 664 300 684 C 330 724 384 732 420 712 Z"},
            {"path": "M 420 652 C 452 610 504 598 540 612 C 514 650 462 668 420 652 Z"}]},
        {"id": "rabbit", "name": "rabbit", "outlines": [
            {"ellipse": [770, 722, 110, 66]}, {"circle": [650, 650, 46]},
            {"ellipse": [630, 568, 13, 40]}, {"ellipse": [670, 568, 13, 40]}, {"circle": [884, 706, 16]}],
         "details": [{"circle": [636, 642, 6]}]},
        {"id": "flow", "name": "energy flow", "pen": "bold",
         "outlines": straight_arrow(226, 250, 380, 560) + straight_arrow(470, 720, 590, 700)},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "Almost all the energy for life on Earth starts in the sun.", "remember": "Life's energy starts with the sun."}},
        {"type": "trace", "title": "Sunlight", "structure": "sun", "part": "details", "instruction": "Draw the sun's rays.",
         "note": {"text": "Sunlight carries energy from the sun to Earth."}},
        {"type": "trace", "title": "Ground", "structure": "ground", "instruction": "Draw the ground.",
         "note": {"text": "The plant's roots grow down into the soil, where it gets water. The energy, though, comes from above."}},
        {"type": "trace", "title": "Plant", "structure": "plant", "instruction": "Trace the plant's stem and two leaves.",
         "note": {"text": "Leaves capture the sun's light energy and store it in the sugar they make. The plant makes its own food.",
                  "remember": "Plants store sunlight in food."}},
        {"type": "trace", "title": "Rabbit", "structure": "rabbit", "instruction": "Trace the rabbit's body, head, ears and tail.",
         "note": {"text": "A rabbit can't make its own food. It gets energy by eating plants."}},
        {"type": "trace", "title": "Eye", "structure": "rabbit", "part": "details", "instruction": "Dab the rabbit's eye.",
         "note": {"text": "Eating plants makes the rabbit a consumer. Plants, which make their own food, are producers."}},
        {"type": "trace", "title": "Energy flow", "structure": "flow", "instruction": "Draw the arrows: sun to plant, then plant to rabbit.",
         "note": {"text": "Arrows show which way energy moves. The energy in the rabbit's food was once energy from the sun.",
                  "remember": "Arrows point the way energy goes."}},
        {"type": "order", "title": "Energy's path",
         "items": ["Sunlight reaches the leaf", "The plant stores energy in food", "The rabbit eats the plant", "The rabbit uses the energy to hop"],
         "instruction": "Tap the steps in order.",
         "why": "The sun's energy is stored in the plant's food. When the rabbit eats the plant, that energy moves into the rabbit.",
         "hint": "Where does the energy come from first?"},
        {"type": "choice", "title": "Trace it back", "instruction": "Follow the arrows backward.", "showsDiagram": True,
         "question": "The rabbit uses energy to run, grow and stay warm. Where did that energy first come from?",
         "options": [
             {"text": "The sun", "correct": True,
              "feedback": "Yes. The plant stored the sun's energy in its food, and the rabbit got it by eating the plant."},
             {"text": "The ground", "feedback": "Soil gives plants water and nutrients, but the energy came from sunlight."},
             {"text": "The rabbit made it", "feedback": "Animals can't make energy. The rabbit got it from the plant, and the plant from the sun."},
             {"text": "The rain", "feedback": "Plants need water, but the energy in their food came from the sun."}]},
        {"type": "choice", "title": "Extend", "instruction": "Add a fox to the model.", "showsDiagram": False,
         "question": "A fox eats the rabbit. Where did the fox's energy first come from?",
         "options": [
             {"text": "The sun, passed on through the plant and the rabbit", "correct": True,
              "feedback": "Right. Even a meat-eater's energy started as sunlight, passed along from plant to rabbit to fox."},
             {"text": "Only the rabbit", "feedback": "The rabbit passed it on, but the rabbit got it from the plant, and the plant from the sun."},
             {"text": "The fox's own body", "feedback": "The fox gets energy from food. Follow it back: rabbit, plant, sun."},
             {"text": "Nowhere: foxes don't need energy", "feedback": "Every animal needs energy, and a fox's comes, in the end, from the sun."}]},
    ],
}

for lesson in (states, mass, salt, gravity, energy):
    save(lesson)
