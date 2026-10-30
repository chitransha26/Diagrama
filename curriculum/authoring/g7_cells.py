"""Grade 7 cells · the compound light microscope and the bacterial cell (MS-LS1-1), and the animal cell, mitochondrion,
diffusion, and plant vs animal cells (MS-LS1-2).

Facts checked against OpenStax Biology 2e (4.1, 4.2, 4.3, 5.2, 15.4, 28.1) and OpenStax Microbiology (2.3), searched with
curriculum/tools/openstax.py.
"""
import math

from lib import save, straight_arrow, r


def bio(section, slug, title):
    return {"title": f"OpenStax Biology 2e, {section} {title}", "url": f"https://openstax.org/books/biology-2e/pages/{slug}"}


LS1_1 = {"title": "NGSS MS-LS1-1: Conduct an investigation to provide evidence that living things are made of cells; either one "
                  "cell or many different numbers and types of cells"}
LS1_2 = {"title": "NGSS MS-LS1-2: Develop and use a model to describe the function of a cell as a whole and ways the parts of "
                  "cells contribute to the function"}
EUK = bio("4.3", "4-3-eukaryotic-cells", "Eukaryotic Cells")
PROK = bio("4.2", "4-2-prokaryotic-cells", "Prokaryotic Cells")


def rrect(x, y, w, h, rad):
    return {"rect": [x, y, w, h, rad]}


def zigzag(cx, cy, half=50, amp=16, n=6):
    """Folds of a mitochondrion's inner membrane, as a zigzag across its middle."""
    return {"line": [c for k in range(n + 1) for c in (r(cx - half + 2 * half * k / n), cy + (amp if k % 2 else -amp))]}


def dots(points, radius=7):
    return [{"circle": [x, y, radius]} for x, y in points]


# ---------------------------------------------------------------- The compound light microscope
TUBE = (420, 140, 80, 330)
microscope = {
    "id": "g7-microscope", "title": "The compound light microscope", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-1", "minutes": 9,
    "sources": [LS1_1, {"title": "OpenStax Microbiology, 2.3 Instruments of Microscopy",
                        "url": "https://openstax.org/books/microbiology/pages/2-3-instruments-of-microscopy"},
                bio("4.1", "4-1-studying-cells", "Studying Cells")],
    "keywords": ["microscope", "compound microscope", "eyepiece", "ocular lens", "objective lens", "stage", "slide",
                 "focus", "magnification", "light", "cells"],
    "structures": [
        {"id": "base", "name": "base", "pen": "bold", "outlines": [rrect(250, 840, 500, 90, 20)]},
        {"id": "arm", "name": "arm", "pen": "bold",
         "outlines": [{"path": "M 560 840 L 560 640 C 560 470 580 330 500 250 L 520 210 C 620 300 610 460 610 640 L 610 840"}]},
        {"id": "tube", "name": "body tube", "outlines": [{"rect": list(TUBE)}]},
        {"id": "eyepiece", "name": "eyepiece", "outlines": [{"rect": [435, 70, 50, 70]}]},
        {"id": "objectives", "name": "objective lenses", "outlines": [{"polygon": [400, 470, 520, 470, 505, 505, 415, 505]},
                                                                    {"rect": [414, 505, 24, 55]}, {"rect": [448, 505, 24, 72]},
                                                                    {"rect": [482, 505, 24, 55]}]},
        {"id": "stage", "name": "stage", "outlines": [{"rect": [330, 600, 320, 26]}]},
        {"id": "slide", "name": "slide", "outlines": [{"rect": [390, 584, 150, 16]}]},
        {"id": "light", "name": "light", "outlines": [{"circle": [460, 770, 34]}]},
        {"id": "knobs", "name": "focus knobs", "outlines": [{"circle": [585, 700, 36]}, {"circle": [585, 790, 22]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Base", "structure": "base", "instruction": "Trace the heavy base.",
         "note": {"text": "Carry a microscope with one hand under the base and the other on the arm."}},
        {"type": "trace", "title": "Arm", "structure": "arm", "instruction": "Trace the curved arm.",
         "note": {"text": "The arm holds the tube and lenses steady above the stage."}},
        {"type": "trace", "title": "Body tube", "structure": "tube", "instruction": "Trace the body tube.",
         "note": {"text": "Light travels up the tube from the specimen to your eye."}},
        {"type": "trace", "title": "Eyepiece", "structure": "eyepiece", "instruction": "Trace the eyepiece at the top.",
         "note": {"text": "You look through the eyepiece. Its lens, the ocular lens, usually magnifies 10 times (10×).",
                  "remember": "Eyepiece: usually 10×."}},
        {"type": "trace", "title": "Objective lenses", "structure": "objectives", "instruction": "Trace the turning nosepiece and its three objective lenses.",
         "note": {"text": "Objective lenses sit close to the specimen. They usually magnify from 4× to 100×. Turn the nosepiece to switch."}},
        {"type": "trace", "title": "Stage", "structure": "stage", "instruction": "Trace the flat stage.",
         "note": {"text": "The stage holds the slide. Raising or lowering it brings the image into focus."}},
        {"type": "trace", "title": "Slide", "structure": "slide", "instruction": "Trace the glass slide on the stage.",
         "note": {"text": "The specimen goes on a slide. It must be thin, so light can pass through it."}},
        {"type": "trace", "title": "Light", "structure": "light", "instruction": "Trace the light below the stage.",
         "note": {"text": "A bulb below the stage shines light up through the specimen and into the lenses.",
                  "remember": "Light passes up through the specimen."}},
        {"type": "trace", "title": "Focus knobs", "structure": "knobs", "instruction": "Trace the big and small focus knobs.",
         "note": {"text": "Use the big coarse knob with the low-power lenses, and the small fine knob with high power."}},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [460, 100], "answer": "Eyepiece", "synonyms": ["Ocular lens"], "role": "Where you look in."},
             {"n": 2, "at": [460, 540], "answer": "Objective lens", "role": "Lens just above the specimen.",
              "mistakes": {"Eyepiece": "The eyepiece is at the top, where you look. This lens near the slide is an objective."}},
             {"n": 3, "at": [380, 613], "answer": "Stage", "role": "Holds the slide."},
             {"n": 4, "at": [460, 770], "answer": "Light", "role": "Shines up through the slide."},
             {"n": 5, "at": [585, 700], "answer": "Coarse focus knob", "role": "Big focusing moves.",
              "mistakes": {"Fine focus knob": "The fine focus knob is the smaller one. This big knob is for coarse focusing."}}],
         "vocabulary": ["Eyepiece", "Ocular lens", "Objective lens", "Stage", "Light", "Coarse focus knob", "Fine focus knob", "Arm"]},
        {"type": "choice", "title": "Magnification", "instruction": "Multiply the two lenses.", "showsDiagram": True,
         "question": "The eyepiece magnifies 10× and the objective lens 40×. How much bigger does the specimen look?",
         "options": [
             {"text": "400 times", "correct": True, "feedback": "Yes. Total magnification = eyepiece × objective: 10 × 40 = 400."},
             {"text": "50 times", "feedback": "Don't add them. Multiply: 10 × 40 = 400."},
             {"text": "40 times", "feedback": "The eyepiece magnifies too. Multiply: 10 × 40 = 400."},
             {"text": "4 times", "feedback": "Multiply the two lenses: 10 × 40 = 400."}]},
        {"type": "choice", "title": "Evidence", "instruction": "Use the microscope as a scientist.", "showsDiagram": False,
         "question": "You look at a thin slice of onion skin, then a drop of pond water with tiny swimming creatures. What do both show?",
         "options": [
             {"text": "Living things are made of cells: some of many cells, some of just one", "correct": True,
              "feedback": "Right. The onion is built of many box-shaped cells; each tiny pond creature may be a single cell."},
             {"text": "Only plants are made of cells", "feedback": "The pond creatures are made of cells too. All living things are."},
             {"text": "Cells are big enough to see without a microscope", "feedback": "Most cells are far too small to see with your eyes alone."},
             {"text": "Water is made of cells", "feedback": "Water isn't alive. The living things in it are made of cells."}]},
    ],
}

# ---------------------------------------------------------------- Animal cell
MEMBRANE = "M 500 130 C 700 120 880 260 870 480 C 860 700 720 880 500 870 C 280 860 120 720 130 500 C 140 280 300 140 500 130 Z"
mitos = [(720, 320), (290, 700), (730, 680)]
ribosomes = [(330, 420), (360, 610), (600, 260), (790, 500), (540, 700), (240, 540)]
animal = {
    "id": "g7-animal-cell", "title": "Animal cell", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-2", "minutes": 10,
    "sources": [LS1_2, EUK, PROK],
    "keywords": ["cell", "animal cell", "organelle", "cell membrane", "plasma membrane", "nucleus", "nucleolus", "mitochondria",
                 "lysosome", "centriole", "ribosome", "cytoplasm"],
    "structures": [
        {"id": "membrane", "name": "cell membrane", "pen": "bold", "outlines": [{"path": MEMBRANE}]},
        {"id": "nucleus", "name": "nucleus", "outlines": [{"circle": [470, 470, 120]}], "details": [{"circle": [490, 450, 34]}]},
        {"id": "mito", "name": "mitochondria", "outlines": [{"ellipse": [x, y, 70, 34]} for x, y in mitos],
         "details": [zigzag(x, y) for x, y in mitos], "focusEach": True},
        {"id": "lyso", "name": "lysosomes", "outlines": [{"circle": [270, 300, 24]}, {"circle": [640, 790, 24]}]},
        {"id": "centrioles", "name": "centrioles", "outlines": [{"rect": [620, 515, 22, 60]}, {"rect": [642, 560, 60, 22]}]},
        {"id": "ribo", "name": "ribosomes", "outlines": dots(ribosomes)},
    ],
    "steps": [
        {"type": "trace", "title": "Cell membrane", "structure": "membrane", "instruction": "Trace the cell membrane all the way round.",
         "note": {"text": "A thin, flexible layer around the cell. It controls what goes in and out. Animal cells have no cell wall.",
                  "remember": "Membrane: the cell's gatekeeper."}},
        {"type": "trace", "title": "Nucleus", "structure": "nucleus", "instruction": "Trace the nucleus.",
         "note": {"text": "The nucleus holds the cell's DNA: the instructions for building and running the cell.",
                  "remember": "Nucleus: the control center."}},
        {"type": "trace", "title": "Nucleolus", "structure": "nucleus", "part": "details", "instruction": "Draw the nucleolus inside the nucleus.",
         "note": {"text": "A dense spot in the nucleus that makes the parts of ribosomes."}},
        {"type": "trace", "title": "Mitochondria", "structure": "mito", "instruction": "Trace the three mitochondria.",
         "note": {"text": "Mitochondria use oxygen and food to make ATP, the cell's energy-carrying molecule. This is cellular respiration.",
                  "remember": "Mitochondria: energy factories."}},
        {"type": "trace", "title": "Folds", "structure": "mito", "part": "details", "instruction": "Draw the folded inner membrane in each one.",
         "note": {"text": "The inner membrane is folded, giving it lots of surface where ATP is made."}},
        {"type": "trace", "title": "Lysosomes", "structure": "lyso", "instruction": "Trace the two lysosomes.",
         "note": {"text": "Lysosomes are the cell's garbage disposal. Their enzymes break down food molecules and worn-out parts."}},
        {"type": "trace", "title": "Centrioles", "structure": "centrioles", "instruction": "Trace the pair of centrioles, at right angles.",
         "note": {"text": "Animal cells have a pair of centrioles near the nucleus. They help organize the cell when it divides."}},
        {"type": "trace", "title": "Ribosomes", "structure": "ribo", "instruction": "Dab a dot for each ribosome.",
         "note": {"text": "Ribosomes are tiny machines that build proteins. Every cell has them, even bacteria.",
                  "remember": "Ribosomes build proteins."}},
        {"type": "identify", "title": "Cytoplasm", "name": "cytoplasm", "structure": "membrane",
         "instruction": "Tap the cytoplasm: the jelly-like fluid inside the membrane, around the organelles.",
         "mistakes": {"nucleus": "That's the nucleus. The cytoplasm surrounds it but doesn't go inside.",
                      "mito": "That's a mitochondrion. It sits in the cytoplasm; tap the space around it.",
                      "lyso": "That's a lysosome. Tap the fluid around it.",
                      "centrioles": "Those are centrioles. Tap the open space around them."},
         "note": {"text": "A jelly-like fluid filling the cell around the organelles. Many of the cell's chemical reactions happen here."}},
        {"type": "label", "title": "Label the cell", "instruction": "Pick the right name for each numbered part.",
         "targets": [
             {"n": 1, "at": [500, 130], "answer": "Cell membrane", "synonyms": ["Plasma membrane"], "role": "Controls what enters and leaves.",
              "mistakes": {"Cell wall": "Animal cells have no cell wall. This flexible outer layer is the membrane."}},
             {"n": 2, "at": [420, 520], "answer": "Nucleus", "role": "Holds the DNA."},
             {"n": 3, "at": [720, 320], "answer": "Mitochondrion", "role": "Makes ATP from food and oxygen.",
              "mistakes": {"Chloroplast": "Animal cells have no chloroplasts. This organelle releases energy from food: a mitochondrion."}},
             {"n": 4, "at": [270, 300], "answer": "Lysosome", "role": "Breaks down waste."},
             {"n": 5, "at": [631, 545], "answer": "Centriole", "role": "Helps organize cell division."}],
         "vocabulary": ["Cell membrane", "Plasma membrane", "Cell wall", "Nucleus", "Mitochondrion", "Chloroplast", "Lysosome",
                        "Centriole", "Ribosome"]},
        {"type": "choice", "title": "Form fits function", "instruction": "Think about energy.", "showsDiagram": True,
         "question": "Muscle cells are packed with far more mitochondria than most cells. Why?",
         "options": [
             {"text": "Muscles need lots of energy, and mitochondria make the ATP that supplies it", "correct": True,
              "feedback": "Yes. Moving your body takes a lot of energy, so muscle cells have many mitochondria making ATP."},
             {"text": "Mitochondria store the cell's DNA", "feedback": "The nucleus holds the DNA. Mitochondria make ATP for energy."},
             {"text": "Mitochondria make muscles bigger", "feedback": "They supply energy. Busy muscle cells need a lot of it."},
             {"text": "Mitochondria break down waste", "feedback": "That's the lysosomes' job. Mitochondria make ATP."}]},
        {"type": "choice", "title": "The cell as a system", "instruction": "Think about the whole cell.", "showsDiagram": True,
         "question": "A drug stops a cell's ribosomes working. What will the cell no longer be able to do?",
         "options": [
             {"text": "Build new proteins", "correct": True,
              "feedback": "Right. Ribosomes build proteins, which the cell needs for almost everything. The parts depend on each other."},
             {"text": "Store DNA", "feedback": "The nucleus stores DNA. Ribosomes build proteins."},
             {"text": "Break down waste", "feedback": "Lysosomes do that, though their enzymes are proteins made by ribosomes."},
             {"text": "Control what enters", "feedback": "The membrane does that. Ribosomes build proteins."}]},
    ],
}

# ---------------------------------------------------------------- Bacterial cell (prokaryote)
flagellum = []
for i in range(0, 26):
    x = 140 - i * 5
    flagellum += [x, round(500 + 22 * math.sin(2 * math.pi * i / 13), 1)]
pili = [{"line": [x, 330, x + dx, 282]} for x, dx in ((350, -10), (500, 0), (650, 10))] + \
       [{"line": [x, 670, x + dx, 718]} for x, dx in ((350, -10), (500, 0), (650, 10))]
NUCLEOID = ("M 420 470 C 460 420 520 540 560 470 C 600 410 650 520 600 545 C 560 565 520 500 470 560 "
            "C 420 615 375 520 420 470 Z")
bacterium = {
    "id": "g7-bacterium", "title": "Bacterial cell (prokaryote)", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-1", "minutes": 9,
    "sources": [LS1_1, PROK],
    "keywords": ["bacteria", "bacterium", "prokaryote", "single-celled", "unicellular", "cell wall", "capsule", "nucleoid",
                 "DNA", "flagellum", "pili", "ribosomes"],
    "printed": [{"text": "Not to scale", "at": [140, 940], "size": 26}],
    "structures": [
        {"id": "capsule", "name": "capsule", "pen": "fine", "outlines": [rrect(140, 330, 720, 340, 170)]},
        {"id": "wall", "name": "cell wall", "pen": "bold", "outlines": [rrect(165, 355, 670, 290, 145)]},
        {"id": "membrane", "name": "cell membrane", "pen": "fine", "outlines": [rrect(187, 377, 626, 246, 123)]},
        {"id": "dna", "name": "nucleoid", "outlines": [{"path": NUCLEOID}]},
        {"id": "ribo", "name": "ribosomes", "outlines": dots([(280, 440), (300, 560), (330, 500), (700, 440), (720, 560), (680, 600)])},
        {"id": "flagellum", "name": "flagellum", "outlines": [{"line": flagellum}]},
        {"id": "pili", "name": "pili", "outlines": pili},
    ],
    "steps": [
        {"type": "trace", "title": "Capsule", "structure": "capsule", "instruction": "Trace the outer capsule.",
         "note": {"text": "Many bacteria have a sticky capsule that lets them cling to surfaces."}},
        {"type": "trace", "title": "Cell wall", "structure": "wall", "instruction": "Trace the cell wall.",
         "note": {"text": "The cell wall protects the cell, holds its shape and stops it drying out."}},
        {"type": "trace", "title": "Cell membrane", "structure": "membrane", "instruction": "Trace the membrane just inside the wall.",
         "note": {"text": "Every cell has a membrane, cytoplasm, DNA and ribosomes, from bacteria to you.",
                  "remember": "All cells share four parts."}},
        {"type": "trace", "title": "DNA", "structure": "dna", "instruction": "Trace the tangled loop of DNA in the middle.",
         "note": {"text": "A bacterium has no nucleus. Its DNA sits loose in the middle, in an area called the nucleoid.",
                  "remember": "Prokaryote: no nucleus."}},
        {"type": "trace", "title": "Ribosomes", "structure": "ribo", "instruction": "Dab a dot for each ribosome.",
         "note": {"text": "Ribosomes build the cell's proteins."}},
        {"type": "trace", "title": "Flagellum", "structure": "flagellum", "instruction": "Draw the wavy flagellum at the end.",
         "note": {"text": "Some bacteria swim with a whip-like flagellum."}},
        {"type": "trace", "title": "Pili", "structure": "pili", "instruction": "Draw the six short pili.",
         "note": {"text": "Pili are short hairs. Bacteria use them to pass DNA to each other."}},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [500, 500], "answer": "Nucleoid", "role": "Where the DNA is.",
              "mistakes": {"Nucleus": "Bacteria have no nucleus. Their DNA sits loose in the nucleoid."}},
             {"n": 2, "at": [500, 355], "answer": "Cell wall", "role": "Protects and shapes the cell."},
             {"n": 3, "at": [80, 500], "answer": "Flagellum", "role": "Used for swimming."},
             {"n": 4, "at": [500, 282], "answer": "Pilus", "synonyms": ["Pili"], "role": "Passes DNA to another bacterium."}],
         "vocabulary": ["Nucleoid", "Nucleus", "Cell wall", "Flagellum", "Pilus", "Capsule", "Mitochondrion"]},
        {"type": "choice", "title": "Compare", "instruction": "Compare with your own cells.", "showsDiagram": True,
         "question": "What's the biggest difference between a bacterium and one of your body's cells?",
         "options": [
             {"text": "The bacterium has no nucleus or other membrane-bound organelles", "correct": True,
              "feedback": "Yes. That's what makes it a prokaryote. Your cells keep their DNA in a nucleus."},
             {"text": "The bacterium has no DNA", "feedback": "All cells have DNA. A bacterium's just isn't inside a nucleus."},
             {"text": "The bacterium has no ribosomes", "feedback": "All cells have ribosomes. The difference is the missing nucleus."},
             {"text": "The bacterium is bigger", "feedback": "Bacteria are usually much smaller: 0.1 to 5 micrometres, versus 10 to 100 for our cells."}]},
        {"type": "choice", "title": "Alive?", "instruction": "Think about what a cell is.", "showsDiagram": False,
         "question": "A bacterium is a single cell. Is it a living thing?",
         "options": [
             {"text": "Yes: a single cell can be a whole living organism", "correct": True,
              "feedback": "Right. Some living things are one cell; others, like you, are made of trillions."},
             {"text": "No: living things need many cells", "feedback": "Bacteria are alive, and each is just one cell."},
             {"text": "Only when it swims", "feedback": "A bacterium is alive whether it's moving or not."},
             {"text": "No, it's too small", "feedback": "Size doesn't decide it. A single bacterial cell is a living organism."}]},
    ],
}

# ---------------------------------------------------------------- Mitochondrion (simple)
OX, OY, IRX, IRY = 500, 500, 360, 182


def inner_y(x, top):
    v = IRY * math.sqrt(max(0.0, 1 - ((x - OX) / IRX) ** 2))
    return r(OY - v if top else OY + v)


def crista(x, top, depth=175, half=14):
    """One fold of the inner membrane, poking into the matrix from the top or bottom."""
    sgn = 1 if top else -1
    y0, y1 = inner_y(x - half, top), inner_y(x + half, top)
    tip = r((y0 + y1) / 2 + sgn * depth)
    return {"path": f"M {x - half} {y0} L {x - half} {tip} A {half} {half} 0 0 {0 if top else 1} {x + half} {tip} L {x + half} {y1}"}


cristae = [crista(x, k % 2 == 0) for k, x in enumerate((260, 380, 500, 620, 740))]
mito = {
    "id": "g7-mitochondrion", "title": "Mitochondrion (simple)", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-2", "minutes": 8,
    "sources": [LS1_2, EUK, bio("15.4", "15-4-rna-processing-in-eukaryotes", "RNA Processing in Eukaryotes (mitochondrial DNA)")],
    "keywords": ["mitochondrion", "mitochondria", "ATP", "energy", "cellular respiration", "cristae", "matrix", "inner membrane",
                 "outer membrane", "oxygen", "carbon dioxide"],
    "structures": [
        {"id": "outer", "name": "outer membrane", "pen": "bold", "outlines": [{"ellipse": [OX, OY, 410, 230]}]},
        {"id": "inner", "name": "inner membrane", "outlines": [{"ellipse": [OX, OY, IRX, IRY]}], "details": cristae},
    ],
    "steps": [
        {"type": "trace", "title": "Outer membrane", "structure": "outer", "instruction": "Trace the smooth outer membrane.",
         "note": {"text": "A mitochondrion has two membranes. The outer one is smooth and wraps the whole organelle."}},
        {"type": "trace", "title": "Inner membrane", "structure": "inner", "instruction": "Trace the inner membrane.",
         "note": {"text": "The inner membrane is where most ATP, the cell's energy-carrying molecule, is made."}},
        {"type": "trace", "title": "Cristae", "structure": "inner", "part": "details", "instruction": "Draw the five folds poking into the middle.",
         "note": {"text": "The inner membrane folds into cristae. Folding packs far more membrane into a small space, so more ATP can be made.",
                  "remember": "Folds = more surface = more ATP."}},
        {"type": "identify", "title": "Matrix", "name": "matrix", "structure": "inner",
         "instruction": "Tap the matrix: the space inside the inner membrane.",
         "mistakes": {"outer": "That's the gap between the two membranes. The matrix is inside the inner membrane."},
         "insideDetailsMistake": "That's inside a fold of the membrane. Tap the open space of the matrix.",
         "note": {"text": "The matrix is the fluid inside the inner membrane. Mitochondria even have their own DNA."}},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [500, 270], "answer": "Outer membrane", "role": "Smooth outer covering."},
             {"n": 2, "at": [260, 500], "answer": "Crista", "synonyms": ["Cristae"], "role": "A fold of the inner membrane.",
              "mistakes": {"Outer membrane": "The outer membrane is smooth. These folds belong to the inner membrane: cristae."}},
             {"n": 3, "at": [440, 600], "answer": "Matrix", "role": "Fluid inside the inner membrane."}],
         "vocabulary": ["Outer membrane", "Inner membrane", "Crista", "Matrix", "Nucleus"]},
        {"type": "choice", "title": "What it does", "instruction": "Think about the whole cell.", "showsDiagram": True,
         "question": "What does a mitochondrion do for the cell?",
         "options": [
             {"text": "It releases energy from food, using oxygen, to make ATP", "correct": True,
              "feedback": "Yes. This is cellular respiration. It also gives off carbon dioxide, the CO2 you breathe out."},
             {"text": "It makes food from sunlight", "feedback": "That's photosynthesis, in chloroplasts. Mitochondria release energy from food."},
             {"text": "It stores the cell's main DNA", "feedback": "The nucleus does that. Mitochondria make ATP."},
             {"text": "It builds proteins", "feedback": "Ribosomes build proteins. Mitochondria make ATP."}]},
        {"type": "choice", "title": "Inputs and outputs", "instruction": "Follow the gases.", "showsDiagram": False,
         "question": "Which gas do mitochondria use up, and which do they give off?",
         "options": [
             {"text": "Use oxygen, give off carbon dioxide", "correct": True,
              "feedback": "Right. That's why you breathe in oxygen and breathe out carbon dioxide."},
             {"text": "Use carbon dioxide, give off oxygen", "feedback": "That's photosynthesis in plants. Respiration is the reverse."},
             {"text": "Use nitrogen, give off oxygen", "feedback": "Nitrogen isn't used. Mitochondria use oxygen and release carbon dioxide."},
             {"text": "They don't use any gas", "feedback": "They need oxygen to release energy from food, and release carbon dioxide."}]},
    ],
}

# ---------------------------------------------------------------- Diffusion across a membrane
before_left = [(170, 160), (240, 210), (320, 150), (400, 200), (180, 290), (270, 330), (360, 280), (430, 360), (200, 390), (330, 400)]
before_right = [(640, 250), (790, 350)]
after_left = [(180, 640), (300, 700), (420, 620), (220, 800), (360, 840), (430, 760)]
after_right = [(580, 650), (720, 620), (840, 700), (620, 800), (760, 840), (860, 800)]


def pores(top, bottom, n=5):
    """A membrane drawn as a broken line: the gaps are where molecules can pass."""
    step = (bottom - top) / n
    return [{"line": [500, r(top + k * step + 12), 500, r(top + (k + 1) * step - 12)]} for k in range(n)]


diffusion = {
    "id": "g7-diffusion", "title": "Diffusion across a membrane", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-2", "minutes": 8,
    "sources": [LS1_2, bio("5.2", "5-2-passive-transport", "Passive Transport"), bio("28.1", "28-1-phylum-porifera", "Phylum Porifera (oxygen by diffusion)")],
    "keywords": ["diffusion", "membrane", "concentration", "high concentration", "low concentration", "equilibrium",
                 "passive transport", "molecules", "cell membrane", "oxygen"],
    "printed": [{"text": "Before", "at": [500, 60], "size": 30}, {"text": "Later", "at": [500, 520], "size": 30}],
    "structures": [
        {"id": "box1", "name": "first box", "outlines": [{"rect": [100, 100, 800, 340]}]},
        {"id": "wall1", "name": "membrane", "pen": "bold", "outlines": pores(100, 440)},
        {"id": "dots1", "name": "molecules", "outlines": dots(before_left + before_right, 10)},
        {"id": "net", "name": "net movement", "outlines": straight_arrow(560, 160, 760, 160, head=22)},
        {"id": "box2", "name": "second box", "outlines": [{"rect": [100, 560, 800, 340]}]},
        {"id": "wall2", "name": "membrane", "pen": "bold", "outlines": pores(560, 900)},
        {"id": "dots2", "name": "molecules", "outlines": dots(after_left + after_right, 10)},
    ],
    "steps": [
        {"type": "trace", "title": "Before", "structure": "box1", "instruction": "Trace the top box.",
         "note": {"text": "This is a close-up of a membrane with water on both sides."}},
        {"type": "trace", "title": "Membrane", "structure": "wall1", "instruction": "Trace the membrane down the middle, with its gaps.",
         "note": {"text": "Some small molecules can pass through a cell membrane on their own."}},
        {"type": "trace", "title": "Molecules", "structure": "dots1", "instruction": "Dab a dot for every molecule.",
         "note": {"text": "There are many molecules on the left: a high concentration. Few on the right: a low concentration."}},
        {"type": "trace", "title": "Net movement", "structure": "net", "instruction": "Draw the arrow from left to right.",
         "note": {"text": "Molecules move randomly all the time, but more cross from the crowded side to the emptier side. This is diffusion.",
                  "remember": "Diffusion: high to low concentration."}},
        {"type": "trace", "title": "Later", "structure": "box2", "instruction": "Trace the bottom box.",
         "note": {"text": "This is the same place a while later."}},
        {"type": "trace", "title": "Membrane", "structure": "wall2", "instruction": "Trace the membrane again.",
         "note": {"text": "Diffusion needs no energy from the cell. It's a kind of passive transport."}},
        {"type": "trace", "title": "Spread out", "structure": "dots2", "instruction": "Dab a dot for every molecule.",
         "note": {"text": "Now the concentration is equal on both sides. Molecules still move, but there's no net movement: equilibrium.",
                  "remember": "Equal on both sides = equilibrium."}},
        {"type": "choice", "title": "Which way?", "instruction": "Use the top picture.", "showsDiagram": True,
         "question": "Which way do the molecules diffuse overall?",
         "options": [
             {"text": "From the crowded left side to the emptier right side", "correct": True,
              "feedback": "Yes. Diffusion goes from high concentration to low until it evens out."},
             {"text": "From right to left", "feedback": "That's from low to high. Diffusion goes from high to low concentration."},
             {"text": "They don't move", "feedback": "Molecules are always moving. Overall, more cross from the crowded side."},
             {"text": "Only when the cell pushes them", "feedback": "Diffusion needs no push from the cell. It happens on its own."}]},
        {"type": "choice", "title": "Speed", "instruction": "Think about energy.", "showsDiagram": False,
         "question": "How would warming the water change diffusion?",
         "options": [
             {"text": "It would speed up, because molecules move faster when warmer", "correct": True,
              "feedback": "Right. Higher temperature gives molecules more energy, so they spread out faster."},
             {"text": "It would slow down", "feedback": "Warmer molecules move faster, so diffusion speeds up."},
             {"text": "It would stop", "feedback": "Warmth speeds molecules up. Diffusion goes faster."},
             {"text": "No change", "feedback": "Temperature matters: warmer molecules move faster, so diffusion speeds up."}]},
        {"type": "choice", "title": "In living things", "instruction": "Apply it.", "showsDiagram": False,
         "question": "A sponge's cells use up oxygen. How does more oxygen get into them from the seawater?",
         "options": [
             {"text": "It diffuses in, from the water where there's more oxygen to the cells where there's less", "correct": True,
              "feedback": "Yes. Sponges get oxygen by diffusion, and carbon dioxide diffuses out the same way."},
             {"text": "The cells make their own oxygen", "feedback": "Sponge cells use oxygen; they don't make it. It diffuses in from the water."},
             {"text": "Oxygen moves from low to high", "feedback": "Diffusion goes from high to low: from the water into the cells."},
             {"text": "They don't need oxygen", "feedback": "Their mitochondria need oxygen, which diffuses in from the water."}]},
    ],
}

# ---------------------------------------------------------------- Plant vs animal cell
GREEN = "#4D9E38"
chloros = [(130, 520), (150, 720), (330, 745)]
ANIMAL = "M 750 290 C 870 290 950 380 945 500 C 940 630 860 715 750 712 C 630 710 555 630 555 500 C 555 370 640 290 750 290 Z"
compare = {
    "id": "g7-plant-vs-animal", "title": "Plant vs animal cell", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-2", "minutes": 10, "colorMode": "microscope",
    "sources": [LS1_2, EUK],
    "keywords": ["plant cell", "animal cell", "compare", "cell wall", "chloroplast", "vacuole", "nucleus", "mitochondria",
                 "cell membrane", "centriole", "lysosome"],
    "printed": [{"text": "Plant cell", "at": [260, 150], "size": 32}, {"text": "Animal cell", "at": [750, 240], "size": 32}],
    "legend": [{"name": "Chloroplasts", "color": GREEN, "meaning": "Green from chlorophyll: the only clearly colored part"},
               {"name": "Everything else", "color": None, "meaning": "Nearly colorless in a fresh, unstained cell"}],
    "structures": [
        {"id": "wall", "name": "cell wall", "pen": "bold", "outlines": [rrect(50, 200, 420, 600, 30)]},
        {"id": "pmem", "name": "plant cell membrane", "pen": "fine", "outlines": [rrect(70, 220, 380, 560, 18)]},
        {"id": "vacuole", "name": "central vacuole", "outlines": [rrect(200, 260, 225, 420, 80)]},
        {"id": "pnuc", "name": "plant nucleus", "outlines": [{"circle": [130, 320, 46]}]},
        {"id": "chloro", "name": "chloroplasts", "colorName": "chloroplasts", "fill": GREEN,
         "outlines": [{"ellipse": [x, y, 40, 20]} for x, y in chloros]},
        {"id": "pmito", "name": "plant mitochondrion", "outlines": [{"ellipse": [130, 620, 34, 18]}]},
        {"id": "amem", "name": "animal cell membrane", "pen": "bold", "outlines": [{"path": ANIMAL}]},
        {"id": "anuc", "name": "animal nucleus", "outlines": [{"circle": [740, 490, 70]}]},
        {"id": "amito", "name": "animal mitochondrion", "outlines": [{"ellipse": [660, 640, 34, 18]}]},
        {"id": "cent", "name": "centrioles", "outlines": [{"rect": [855, 405, 16, 44]}, {"rect": [871, 440, 44, 16]}]},
        {"id": "lyso", "name": "lysosome", "outlines": [{"circle": [860, 610, 20]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Cell wall", "structure": "wall", "instruction": "Trace the plant cell's wall.",
         "note": {"text": "Only the plant cell has a rigid cell wall. It gives the cell its boxy shape.", "remember": "Wall: plants only."}},
        {"type": "trace", "title": "Plant membrane", "structure": "pmem", "instruction": "Trace the membrane just inside the wall.",
         "note": {"text": "Both cells have a cell membrane controlling what goes in and out."}},
        {"type": "trace", "title": "Central vacuole", "structure": "vacuole", "instruction": "Trace the big central vacuole.",
         "note": {"text": "Plant cells have one large central vacuole full of water that keeps the cell firm."}},
        {"type": "trace", "title": "Plant nucleus", "structure": "pnuc", "instruction": "Trace the plant cell's nucleus.",
         "note": {"text": "Both cells have a nucleus holding their DNA."}},
        {"type": "trace", "title": "Chloroplasts", "structure": "chloro", "instruction": "Trace the three chloroplasts.",
         "note": {"text": "Only plant cells have chloroplasts, which capture light energy to make food.", "remember": "Chloroplasts: plants only."}},
        {"type": "trace", "title": "Plant mitochondrion", "structure": "pmito", "instruction": "Trace the mitochondrion.",
         "note": {"text": "Plant cells have mitochondria too. They release energy from the food the chloroplasts make."}},
        {"type": "trace", "title": "Animal membrane", "structure": "amem", "instruction": "Trace the animal cell's membrane.",
         "note": {"text": "With no wall, the animal cell's shape is rounder and more flexible."}},
        {"type": "trace", "title": "Animal nucleus", "structure": "anuc", "instruction": "Trace the animal cell's nucleus.",
         "note": {"text": "Same job as in the plant cell: it holds the DNA."}},
        {"type": "trace", "title": "Animal mitochondrion", "structure": "amito", "instruction": "Trace the mitochondrion.",
         "note": {"text": "Both kinds of cell have mitochondria to make ATP."}},
        {"type": "trace", "title": "Centrioles", "structure": "cent", "instruction": "Trace the pair of centrioles.",
         "note": {"text": "Animal cells have centrioles; most plant cells don't.", "remember": "Centrioles: animals."}},
        {"type": "trace", "title": "Lysosome", "structure": "lyso", "instruction": "Trace the lysosome.",
         "note": {"text": "Animal cells have lysosomes to digest waste. In plant cells, that happens in the vacuole."}},
        {"type": "color", "title": "Color", "structures": ["chloro"], "instruction": "In fresh, unstained cells, only the chloroplasts have color."},
        {"type": "choice", "title": "Shared parts", "instruction": "Compare the two cells.", "showsDiagram": True,
         "question": "Which parts do BOTH plant and animal cells have?",
         "options": [
             {"text": "Cell membrane, nucleus and mitochondria", "correct": True,
              "feedback": "Yes. All plant and animal cells need these to control what enters, hold DNA, and release energy."},
             {"text": "Cell wall and chloroplasts", "feedback": "Those are only in plant cells."},
             {"text": "Centrioles and lysosomes", "feedback": "Those are in animal cells; most plant cells don't have them."},
             {"text": "Chloroplasts and mitochondria", "feedback": "Both have mitochondria, but only plants have chloroplasts."}]},
        {"type": "choice", "title": "Why the difference?", "instruction": "Think about how each lives.", "showsDiagram": True,
         "question": "Why do plant cells need chloroplasts, but animal cells don't?",
         "options": [
             {"text": "Plants make their own food from light; animals eat food", "correct": True,
              "feedback": "Right. Chloroplasts capture light to make sugar. Animals get their food by eating."},
             {"text": "Animals live in the dark", "feedback": "Many animals live in sunlight. They get food by eating instead of making it."},
             {"text": "Chloroplasts hold up the plant", "feedback": "The cell wall does that. Chloroplasts make food from light."},
             {"text": "Animal cells are too small", "feedback": "Size isn't the reason. Animals get food by eating, not from light."}]},
    ],
}

for lesson in (microscope, animal, bacterium, mito, diffusion, compare):
    save(lesson)
