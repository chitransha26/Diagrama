"""Grade 7 · DNA, genes and chromosomes (MS-LS3-1), a Punnett square and asexual reproduction (MS-LS3-2), homologous
forelimbs (MS-LS4-2) and natural selection in finch beaks (MS-LS4-4).

Facts checked against OpenStax Biology 2e (10.1, 10.5, 12.2, 14.2, 18.1, 24.1, 27.1, 32.3), searched with
curriculum/tools/openstax.py.
"""
import math

from lib import save, straight_arrow, mirror_path, r


def bio(section, slug, title):
    return {"title": f"OpenStax Biology 2e, {section} {title}", "url": f"https://openstax.org/books/biology-2e/pages/{slug}"}


def rrect(x, y, w, h, rad):
    return {"rect": [x, y, w, h, rad]}


def arrows(*specs, head=24):
    out = []
    for s in specs:
        out += straight_arrow(*s, head=head)
    return out


LS3_1 = {"title": "NGSS MS-LS3-1: Develop and use a model to describe why structural changes to genes (mutations) located on "
                  "chromosomes may affect proteins and may result in harmful, beneficial, or neutral effects to the "
                  "structure and function of the organism"}
LS3_2 = {"title": "NGSS MS-LS3-2: Develop and use a model to describe why asexual reproduction results in offspring with "
                  "identical genetic information and sexual reproduction results in offspring with genetic variation"}
LS4_2 = {"title": "NGSS MS-LS4-2: Apply scientific ideas to construct an explanation for the anatomical similarities and "
                  "differences among modern organisms and between modern and fossil organisms to infer evolutionary relationships"}
LS4_4 = {"title": "NGSS MS-LS4-4: Construct an explanation based on evidence that describes how genetic variations of traits "
                  "in a population increase some individuals' probability of surviving and reproducing in a specific environment"}
CELL_DIVISION = bio("10.1", "10-1-cell-division", "Cell Division")
TRAITS = bio("12.2", "12-2-characteristics-and-traits", "Characteristics and Traits")
EVOLUTION = bio("18.1", "18-1-understanding-evolution", "Understanding Evolution")

# ---------------------------------------------------------------- DNA, genes and chromosomes
CHROMATID = ("M 350 330 C 350 312 378 308 382 326 C 400 410 432 470 436 500 C 432 530 400 590 382 674 "
             "C 378 692 350 688 350 670 C 368 590 404 530 408 500 C 404 470 368 410 350 330 Z")


def strand(sign):
    pts = []
    for i in range(0, 121):
        y = 200 + i * 5
        pts += [r(800 + sign * 70 * math.sin(2 * math.pi * (y - 200) / 300)), y]
    return {"line": pts}


rungs = []
for y in range(215, 800, 24):
    s = math.sin(2 * math.pi * (y - 200) / 300)
    if abs(s) > 0.45:
        rungs.append({"line": [r(800 - 70 * s * 0.85), y, r(800 + 70 * s * 0.85), y]})
dna = {
    "id": "g7-dna-genes-chromosomes", "title": "DNA, genes and chromosomes", "grade": "7", "subject": "Life science",
    "standard": "MS-LS3-1", "minutes": 9,
    "sources": [LS3_1, CELL_DIVISION, bio("14.2", "14-2-dna-structure-and-sequencing", "DNA Structure and Sequencing"),
                bio("14.0", "14-introduction", "Introduction to DNA Structure and Function (genes)")],
    "keywords": ["DNA", "gene", "genes", "chromosome", "chromosomes", "nucleus", "double helix", "base pairs", "protein",
                 "mutation", "heredity", "traits", "46 chromosomes"],
    "structures": [
        {"id": "cell", "name": "cell", "outlines": [{"circle": [150, 500, 120]}]},
        {"id": "nucleus", "name": "nucleus", "pen": "bold", "outlines": [{"circle": [150, 500, 55]}]},
        {"id": "chromosome", "name": "chromosome", "pen": "bold", "outlines": [{"path": CHROMATID}, {"path": mirror_path(CHROMATID, 450)}]},
        {"id": "zoom", "name": "zoom arrows", "pen": "fine", "outlines": arrows((280, 500, 340, 500), (560, 500, 640, 500))},
        {"id": "helix", "name": "DNA double helix", "outlines": [strand(1), strand(-1)], "details": rungs},
        {"id": "gene", "name": "gene", "pen": "bold", "outlines": [{"line": [890, 400, 915, 400, 915, 600, 890, 600]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Cell", "structure": "cell", "instruction": "Trace the cell.",
         "note": {"text": "Every cell in your body carries a full set of instructions for building and running you."}},
        {"type": "trace", "title": "Nucleus", "structure": "nucleus", "instruction": "Trace the nucleus.",
         "note": {"text": "The instructions are stored in the nucleus, on chromosomes.", "remember": "Nucleus holds the chromosomes."}},
        {"type": "trace", "title": "Zoom in", "structure": "zoom", "instruction": "Draw the two arrows zooming in.",
         "note": {"text": "Each arrow zooms in closer: from the nucleus to one chromosome, then to its DNA."}},
        {"type": "trace", "title": "Chromosome", "structure": "chromosome", "instruction": "Trace the X-shaped chromosome.",
         "note": {"text": "A chromosome is DNA wrapped tightly around proteins. Human body cells have 46 chromosomes, in 23 pairs.",
                  "remember": "Humans: 46 chromosomes."}},
        {"type": "trace", "title": "DNA", "structure": "helix", "instruction": "Trace the two twisting strands of DNA.",
         "note": {"text": "DNA is two strands twisted around each other, a shape called a double helix."}},
        {"type": "trace", "title": "Base pairs", "structure": "helix", "part": "details", "instruction": "Draw the rungs between the strands.",
         "note": {"text": "The rungs are pairs of bases: A always pairs with T, and C with G. Their order spells out the instructions.",
                  "remember": "A with T, C with G."}},
        {"type": "trace", "title": "Gene", "structure": "gene", "instruction": "Draw the bracket marking one section of the DNA.",
         "note": {"text": "A gene is a section of DNA that codes for one product, usually a protein. Each chromosome carries thousands."}},
        {"type": "order", "title": "Biggest to smallest", "instruction": "Tap from biggest to smallest.",
         "items": ["Cell", "Nucleus", "Chromosome", "Gene"],
         "why": "A cell has a nucleus, the nucleus holds chromosomes, and each chromosome carries thousands of genes.",
         "hint": "Each one is inside the one before it."},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [150, 500], "answer": "Nucleus", "role": "Holds the chromosomes."},
             {"n": 2, "at": [450, 400], "answer": "Chromosome", "role": "Tightly packed DNA.",
              "mistakes": {"Gene": "A gene is a short section of DNA. This whole packed X is a chromosome."}},
             {"n": 3, "at": [800, 250], "answer": "DNA", "role": "A double helix."},
             {"n": 4, "at": [945, 500], "answer": "Gene", "role": "Codes for a protein."}],
         "vocabulary": ["Nucleus", "Chromosome", "DNA", "Gene", "Protein", "Cell membrane"]},
        {"type": "choice", "title": "Mutations", "instruction": "Think about the instructions.", "showsDiagram": True,
         "question": "A mutation changes the order of bases in one gene. What could happen?",
         "options": [
             {"text": "The protein that gene codes for may change, which could be harmful, helpful or have no effect", "correct": True,
              "feedback": "Yes. Changed instructions can change a protein, and so a trait. Many mutations have no effect at all."},
             {"text": "Every mutation is harmful", "feedback": "Some are harmful, but some are helpful and many have no effect."},
             {"text": "The whole chromosome disappears", "feedback": "A mutation changes the DNA's code. The chromosome is still there."},
             {"text": "Nothing can ever change", "feedback": "Changing the code of a gene can change the protein it makes."}]},
    ],
}

# ---------------------------------------------------------------- A Punnett square
VIOLET = "#8E5BB5"
punnett = {
    "id": "g7-punnett-square", "title": "A Punnett square", "grade": "7", "subject": "Life science", "standard": "MS-LS3-2",
    "minutes": 9,
    "sources": [LS3_2, TRAITS, bio("12.1", "12-1-mendels-experiments-and-the-laws-of-probability",
                                    "Mendel's Experiments and the Laws of Probability")],
    "keywords": ["Punnett square", "genetics", "alleles", "dominant", "recessive", "genotype", "phenotype", "Mendel",
                 "pea plants", "heredity", "probability", "traits"],
    "printed": [{"text": "Parent 1: Vv", "at": [500, 140], "size": 30}, {"text": "Parent 2: Vv", "at": [120, 500], "size": 30},
                {"text": "V", "at": [400, 255], "size": 40}, {"text": "v", "at": [600, 255], "size": 40},
                {"text": "V", "at": [250, 400], "size": 40}, {"text": "v", "at": [250, 600], "size": 40},
                {"text": "V = violet flowers (dominant)   v = white (recessive)", "at": [500, 820], "size": 26}],
    "structures": [
        {"id": "box", "name": "square", "pen": "bold", "outlines": [rrect(300, 300, 400, 400, 8)]},
        {"id": "grid", "name": "dividing lines", "outlines": [{"line": [500, 300, 500, 700]}, {"line": [300, 500, 700, 500]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Square", "structure": "box", "instruction": "Trace the big square.",
         "note": {"text": "A Punnett square predicts the offspring of two parents. Here, two pea plants with violet flowers."}},
        {"type": "trace", "title": "Four boxes", "structure": "grid", "instruction": "Draw the lines that divide it into four boxes.",
         "note": {"text": "Each parent has two copies of the flower-color gene, called alleles. Each passes one on, by chance.",
                  "remember": "One allele from each parent."}},
        {"type": "label", "title": "Fill it in", "instruction": "Combine the letter above with the letter at the side for each box.",
         "targets": [
             {"n": 1, "at": [400, 400], "answer": "VV", "role": "Two violet alleles."},
             {"n": 2, "at": [600, 400], "answer": "Vv", "synonyms": ["vV"], "role": "One of each."},
             {"n": 3, "at": [400, 600], "answer": "Vv", "synonyms": ["vV"], "role": "One of each."},
             {"n": 4, "at": [600, 600], "answer": "vv", "role": "Two white alleles.",
              "mistakes": {"Vv": "This box gets v from the top and v from the side: vv."}}],
         "vocabulary": ["VV", "Vv", "vv"]},
        {"type": "choice", "title": "Dominant", "instruction": "Read the key.", "showsDiagram": True,
         "question": "A plant is Vv. What color are its flowers?",
         "options": [
             {"text": "Violet, because V is dominant", "correct": True,
              "feedback": "Yes. One dominant allele is enough to show the trait. The white allele is hidden."},
             {"text": "White", "feedback": "White shows only with two recessive alleles, vv."},
             {"text": "Half violet, half white", "feedback": "In peas, V is fully dominant. Vv flowers are violet."},
             {"text": "Light purple", "feedback": "For pea flower color, V is fully dominant, so Vv is violet."}]},
        {"type": "choice", "title": "Predict", "instruction": "Count the boxes.", "showsDiagram": True,
         "question": "What is the chance that an offspring has white flowers?",
         "options": [
             {"text": "1 in 4, or 25%", "correct": True,
              "feedback": "Right. Only the vv box gives white flowers. The other three give violet: about 3 violet to 1 white."},
             {"text": "0%: both parents are violet", "feedback": "Both parents carry a hidden v. One box in four is vv: white."},
             {"text": "50%", "feedback": "Two boxes are Vv, but those are violet. Only vv, one box in four, is white."},
             {"text": "100%", "feedback": "Three of the four boxes have at least one V, so they're violet."}]},
        {"type": "choice", "title": "Variation", "instruction": "Compare with the parents.", "showsDiagram": True,
         "question": "Why can two violet parents have a white-flowered offspring?",
         "options": [
             {"text": "Each parent passes on one allele, and both can pass on their hidden v", "correct": True,
              "feedback": "Yes. Sexual reproduction mixes alleles from two parents, so offspring can differ from both."},
             {"text": "The flower changed color as it grew", "feedback": "The color comes from the alleles it inherited: vv gives white."},
             {"text": "It's a mistake", "feedback": "It's expected. Mixing alleles from two parents creates variation."},
             {"text": "White is dominant", "feedback": "White is recessive. It shows when an offspring gets v from both parents."}]},
    ],
}

# ---------------------------------------------------------------- Asexual reproduction: budding and fission
TAN = "#E9D9A6"
dna_loop = lambda x, y: {"path": f"M {x - 30} {y} C {x - 20} {y - 20} {x - 5} {y + 20} {x + 5} {y} C {x + 15} {y - 20} {x + 25} {y + 15} {x + 30} {y}"}
asexual = {
    "id": "g7-asexual-reproduction", "title": "Asexual reproduction: budding and fission", "grade": "7",
    "subject": "Life science", "standard": "MS-LS3-2", "minutes": 8,
    "sources": [LS3_2, bio("10.5", "10-5-prokaryotic-cell-division", "Prokaryotic Cell Division"),
                bio("24.1", "24-1-characteristics-of-fungi", "Characteristics of Fungi (yeast budding)"),
                bio("27.1", "27-1-features-of-the-animal-kingdom", "Features of the Animal Kingdom (budding)"),
                bio("32.3", "32-3-asexual-reproduction", "Asexual Reproduction")],
    "keywords": ["asexual reproduction", "binary fission", "fission", "budding", "bacteria", "yeast", "identical",
                 "clone", "offspring", "one parent", "genetic variation"],
    "printed": [{"text": "Bacterium: binary fission", "at": [500, 120], "size": 28}, {"text": "Yeast: budding", "at": [500, 560], "size": 28}],
    "structures": [
        {"id": "f1", "name": "bacterium", "outlines": [rrect(60, 215, 160, 70, 35)], "details": [dna_loop(140, 250)]},
        {"id": "f2", "name": "bacterium stretching", "outlines": [rrect(320, 215, 240, 70, 35)],
         "details": [dna_loop(390, 250), dna_loop(490, 250)]},
        {"id": "f3", "name": "two bacteria", "outlines": [rrect(660, 215, 140, 70, 35), rrect(820, 215, 140, 70, 35)]},
        {"id": "b1", "name": "yeast cell", "outlines": [{"ellipse": [140, 720, 80, 60]}]},
        {"id": "b2", "name": "yeast with a bud", "outlines": [{"ellipse": [440, 720, 80, 60]}, {"circle": [540, 706, 32]}]},
        {"id": "b3", "name": "two yeast cells", "outlines": [{"ellipse": [760, 720, 80, 60]}, {"circle": [905, 706, 38]}]},
        {"id": "steps", "name": "arrows", "pen": "fine",
         "outlines": arrows((235, 250, 300, 250), (575, 250, 640, 250), (235, 720, 340, 720), (590, 720, 662, 720), head=20)},
    ],
    "steps": [
        {"type": "trace", "title": "Bacterium", "structure": "f1", "instruction": "Trace the bacterium at the top left.",
         "note": {"text": "Bacteria reproduce by binary fission: one cell splits into two."}},
        {"type": "trace", "title": "Its DNA", "structure": "f1", "part": "details", "instruction": "Draw its loop of DNA.",
         "note": {"text": "A bacterium has one loop-shaped chromosome."}},
        {"type": "trace", "title": "Copying", "structure": "f2", "instruction": "Trace the longer cell.",
         "note": {"text": "The cell copies its DNA and grows longer."}},
        {"type": "trace", "title": "Two copies", "structure": "f2", "part": "details", "instruction": "Draw the two copies of the DNA.",
         "note": {"text": "Each copy is exact, so each new cell gets the same instructions.", "remember": "DNA copied exactly."}},
        {"type": "trace", "title": "Split", "structure": "f3", "instruction": "Trace the two new bacteria.",
         "note": {"text": "A new wall forms across the middle and the cell splits into two identical daughter cells."}},
        {"type": "trace", "title": "Yeast", "structure": "b1", "instruction": "Trace the yeast cell.",
         "note": {"text": "Yeast is a single-celled fungus. It reproduces by budding."}},
        {"type": "trace", "title": "Bud", "structure": "b2", "instruction": "Trace the yeast cell with a bud bulging out.",
         "note": {"text": "A bulge forms on the side of the cell. The nucleus divides, and one copy moves into the bud."}},
        {"type": "trace", "title": "New cell", "structure": "b3", "instruction": "Trace the parent and the bud that broke off.",
         "note": {"text": "The bud detaches as a new yeast cell.", "remember": "Asexual: one parent, identical offspring."}},
        {"type": "trace", "title": "Steps", "structure": "steps", "instruction": "Draw the arrows between the steps.",
         "note": {"text": "Each arrow is one step in time. Both processes need just one parent."}},
        {"type": "choice", "title": "Identical", "instruction": "Compare the offspring with the parent.", "showsDiagram": True,
         "question": "How do the offspring's genes compare with the parent's?",
         "options": [
             {"text": "They're identical, because there's only one parent and its DNA is copied", "correct": True,
              "feedback": "Yes. Asexual reproduction makes genetically identical offspring, unless a rare mutation happens."},
             {"text": "Half from each of two parents", "feedback": "That's sexual reproduction. Here there's only one parent."},
             {"text": "Completely different", "feedback": "The DNA is copied, so the offspring match the parent."},
             {"text": "They have no genes", "feedback": "Every cell needs DNA. The offspring get an exact copy."}]},
        {"type": "choice", "title": "Trade-off", "instruction": "Compare with sexual reproduction.", "showsDiagram": False,
         "question": "A new disease kills one strain of bacteria. Why might a whole colony made by fission die?",
         "options": [
             {"text": "They're all identical, so if one can't survive it, none can", "correct": True,
              "feedback": "Right. Sexual reproduction makes varied offspring, so some may survive a change. Identical ones can't."},
             {"text": "Fission makes weak cells", "feedback": "The cells are healthy. The problem is that they're all the same."},
             {"text": "Bacteria can't get diseases", "feedback": "They can. And identical cells all share the same weakness."},
             {"text": "Fission is too slow", "feedback": "Fission is fast. The risk is that every cell is identical."}]},
    ],
}

# ---------------------------------------------------------------- Homologous forelimbs
UPPER, LOWER, HAND = "#D97B5A", "#E8C15A", "#7FA7D9"


def limb(cx, upper, lower, gap, hand_lines):
    """Upper bone (x, y0, w, h), two lower bones (y0, w, h) with gap between them, and hand bones as lines."""
    uy, uw, uh = upper
    ly, lw, lh = lower
    return ([rrect(cx - uw / 2, uy, uw, uh, uw / 2)],
            [rrect(cx - gap / 2 - lw, ly, lw, lh, lw / 2), rrect(cx + gap / 2, ly, lw, lh, lw / 2)],
            [{"line": l} for l in hand_lines])


human = limb(125, (150, 30, 250), (420, 22, 210), 18, [[125 + d, 650, 125 + d * 1.8, 830] for d in (-36, -18, 0, 18, 36)])
dog = limb(375, (150, 34, 220), (390, 22, 240), 18, [[375 + d, 650, 375 + d * 1.3, 760] for d in (-30, -10, 10, 30)])
bird = limb(625, (150, 30, 240), (410, 18, 260), 22, [[625, 690, 625, 860], [607, 690, 590, 780]])
whale = limb(875, (150, 52, 120), (290, 34, 110), 18, [[875 + d, 420, 875 + d * 1.5, 420 + 300 - abs(d) * 3] for d in (-40, -20, 0, 20, 40)])
limbs = [human, dog, bird, whale]
forelimbs = {
    "id": "g7-homologous-forelimbs", "title": "Homologous forelimbs", "grade": "7", "subject": "Life science",
    "standard": "MS-LS4-2", "minutes": 9, "colorMode": "illustration",
    "sources": [LS4_2, EVOLUTION],
    "keywords": ["homologous structures", "forelimbs", "evolution", "common ancestor", "bones", "human arm", "dog leg",
                 "bird wing", "whale flipper", "anatomy", "evidence"],
    "printed": [{"text": t, "at": [x, 940], "size": 28} for t, x in (("Human", 125), ("Dog", 375), ("Bird", 625), ("Whale", 875))],
    "legend": [{"name": "Upper arm bone", "color": UPPER, "meaning": "One bone, in every limb"},
               {"name": "Forearm bones", "color": LOWER, "meaning": "Two bones, in every limb"},
               {"name": "Wrist and hand", "color": None, "meaning": "Drawn as lines; many small bones"}],
    "structures": [
        {"id": "upper", "name": "upper arm bones", "colorName": "upper arm bone", "fill": UPPER, "pen": "bold",
         "outlines": [s for l in limbs for s in l[0]]},
        {"id": "lower", "name": "forearm bones", "colorName": "forearm bones", "fill": LOWER, "outlines": [s for l in limbs for s in l[1]]},
        {"id": "hand", "name": "hand bones", "pen": "fine", "outlines": [s for l in limbs for s in l[2]]},
    ],
    "steps": [
        {"type": "trace", "title": "Upper arm", "structure": "upper", "instruction": "Trace the upper arm bone in all four limbs.",
         "note": {"text": "A human arm, a dog's front leg, a bird's wing and a whale's flipper all start with one upper bone.",
                  "remember": "One bone at the top."}},
        {"type": "trace", "title": "Forearm", "structure": "lower", "instruction": "Trace the pair of forearm bones in each limb.",
         "note": {"text": "Next come two forearm bones, side by side, in all four.", "remember": "Then two bones."}},
        {"type": "trace", "title": "Hand", "structure": "hand", "instruction": "Draw the hand bones in each limb.",
         "note": {"text": "Then come wrist and hand bones: long fingers in the flipper, few and fused in the wing."}},
        {"type": "color", "title": "Color", "structures": ["upper", "lower"], "instruction": "Color the matching bones the same color in every limb."},
        {"type": "choice", "title": "Same plan", "instruction": "Compare the four limbs.", "showsDiagram": True,
         "question": "These limbs do very different jobs. Why do they have the same layout of bones?",
         "options": [
             {"text": "They were inherited from a common ancestor", "correct": True,
              "feedback": "Yes. Parts with the same basic structure from a shared ancestor are called homologous structures."},
             {"text": "They all do the same job", "feedback": "They don't: grabbing, running, flying, swimming. The layout comes from a shared ancestor."},
             {"text": "It's a coincidence", "feedback": "The same bones in the same order in so many animals points to a common ancestor."},
             {"text": "Bones can only grow one way", "feedback": "Bones vary hugely. These match because of shared ancestry."}]},
        {"type": "choice", "title": "Differences", "instruction": "Look at the shapes and sizes.", "showsDiagram": True,
         "question": "Why are the bones different shapes and sizes in each animal?",
         "options": [
             {"text": "Over time, evolution changed them to suit each animal's way of life", "correct": True,
              "feedback": "Right. The layout stayed the same, but shapes and sizes changed for swimming, flying, running or grabbing."},
             {"text": "They come from different ancestors", "feedback": "The shared layout shows a common ancestor. The shapes changed over time."},
             {"text": "Each animal grows its bones however it likes", "feedback": "Bone shapes are inherited. They changed over many generations."},
             {"text": "The bones aren't really different", "feedback": "Compare the flipper's short upper bone with the human's long one."}]},
        {"type": "choice", "title": "Infer", "instruction": "Use the evidence.", "showsDiagram": False,
         "question": "Whales live in water like fish. What do their flipper bones suggest?",
         "options": [
             {"text": "Whales are more closely related to land mammals than to fish", "correct": True,
              "feedback": "Yes. Their flippers hide the same arm bones as a human or dog, inherited from mammal ancestors."},
             {"text": "Whales are a kind of fish", "feedback": "Their limb bones match mammals' arms, not fish fins. Whales are mammals."},
             {"text": "Whales have no ancestors", "feedback": "Every species has ancestors. The bones point to land-mammal relatives."},
             {"text": "Flippers prove nothing", "feedback": "Homologous bones are strong evidence of shared ancestry."}]},
    ],
}

# ---------------------------------------------------------------- Natural selection in finch beaks
HEAD_L, HEAD_R = (220, 340), (720, 340)
finches = {
    "id": "g7-finch-beaks", "title": "Natural selection in finch beaks", "grade": "7", "subject": "Life science",
    "standard": "MS-LS4-4", "minutes": 9,
    "sources": [LS4_4, EVOLUTION, bio("19.1", "19-1-population-evolution", "Population Evolution")],
    "keywords": ["natural selection", "finches", "Galápagos", "Darwin", "beaks", "variation", "adaptation", "evolution",
                 "Grants", "El Niño", "seeds", "survival"],
    "printed": [{"text": "Wide, deep beak", "at": [260, 540], "size": 26}, {"text": "Thinner beak", "at": [760, 540], "size": 26},
                {"text": "Large, hard seeds", "at": [260, 870], "size": 24}, {"text": "Small, soft seeds", "at": [760, 870], "size": 24},
                {"text": "Medium ground finches, Daphne Major", "at": [500, 70], "size": 26}],
    "structures": [
        {"id": "heads", "name": "two finches' heads", "pen": "bold",
         "outlines": [{"circle": [HEAD_L[0], HEAD_L[1], 120]}, {"circle": [HEAD_R[0], HEAD_R[1], 120]}],
         "details": [{"circle": [HEAD_L[0] + 40, HEAD_L[1] - 40, 12]}, {"circle": [HEAD_R[0] + 40, HEAD_R[1] - 40, 12]}]},
        {"id": "big", "name": "wide, deep beak", "pen": "bold", "outlines": [{"polygon": [335, 270, 450, 340, 335, 420]}]},
        {"id": "thin", "name": "thinner beak", "pen": "bold", "outlines": [{"polygon": [836, 310, 960, 342, 836, 372]}]},
        {"id": "hard", "name": "large seeds", "outlines": [{"ellipse": [200, 760, 50, 34]}, {"ellipse": [320, 770, 46, 32]}]},
        {"id": "soft", "name": "small seeds", "outlines": [{"circle": [x, y, 12]} for x, y in ((700, 750), (740, 780), (780, 750), (820, 785))]},
    ],
    "steps": [
        {"type": "trace", "title": "Two finches", "structure": "heads", "instruction": "Trace the two finches' heads.",
         "note": {"text": "Peter and Rosemary Grant have studied the finches on one Galápagos island every year since 1976."}},
        {"type": "trace", "title": "Eyes", "structure": "heads", "part": "details", "instruction": "Dab an eye on each.",
         "note": {"text": "These two birds belong to the same species, the medium ground finch."}},
        {"type": "trace", "title": "Wide beak", "structure": "big", "instruction": "Trace the wide, deep beak.",
         "note": {"text": "Beak size varies from bird to bird, and it's inherited: parents pass it to their young.",
                  "remember": "Variation + inheritance."}},
        {"type": "trace", "title": "Thin beak", "structure": "thin", "instruction": "Trace the thinner beak.",
         "note": {"text": "Some birds in the same population have thinner beaks."}},
        {"type": "trace", "title": "Large seeds", "structure": "hard", "instruction": "Trace the large, hard seeds.",
         "note": {"text": "Wide, deep beaks are good at cracking large, hard seeds."}},
        {"type": "trace", "title": "Small seeds", "structure": "soft", "instruction": "Dab the small, soft seeds.",
         "note": {"text": "Thinner beaks handle small, soft seeds well."}},
        {"type": "choice", "title": "A wet year", "instruction": "Use the model.", "showsDiagram": True,
         "question": "An El Niño brought heavy rain: few large hard seeds, lots of small soft ones. Which birds did better?",
         "options": [
             {"text": "The thinner-beaked birds", "correct": True,
              "feedback": "Yes. They could eat the plentiful small seeds, so more of them survived and reproduced."},
             {"text": "The wide-beaked birds", "feedback": "Their food, the large hard seeds, became scarce."},
             {"text": "Both did equally well", "feedback": "The food changed, so one beak type had an advantage."},
             {"text": "Neither: all the finches died", "feedback": "Many survived, especially birds with beaks suited to the small seeds."}]},
        {"type": "choice", "title": "The next generation", "instruction": "Beak size is inherited.", "showsDiagram": True,
         "question": "In the years after the El Niño, what did the Grants find?",
         "options": [
             {"text": "The average beak size in the population got smaller", "correct": True,
              "feedback": "Right. More thin-beaked parents meant more thin-beaked young. That's natural selection."},
             {"text": "Each bird's beak shrank during its life", "feedback": "Individual birds don't change their beaks. The population changed over generations."},
             {"text": "Beaks got bigger", "feedback": "The small-beaked birds survived better, so the average got smaller."},
             {"text": "Nothing changed", "feedback": "The Grants measured a real change: the average beak got smaller."}]},
        {"type": "order", "title": "Natural selection", "instruction": "Tap the steps of natural selection in order.",
         "items": ["Beak sizes vary", "The food supply changes", "Birds with suited beaks survive and reproduce more",
                   "Their young inherit those beaks", "The population's average beak changes"],
         "why": "Natural selection needs inherited variation. The environment decides which variations help survival.",
         "hint": "It starts with differences that already exist."},
    ],
}

for lesson in (dna, punnett, asexual, forelimbs, finches):
    save(lesson)
