"""Grade 7 · the nervous system, the urinary system and kidney, a reflex arc (MS-LS1-3, MS-LS1-8), and pollination and
inside a bean seed (MS-LS1-4).

Facts checked against OpenStax Anatomy and Physiology 2e (10.2, 12.1, 13.4, 14.3, 25.2, 25.3, 25.5) and OpenStax
Biology 2e (26.3, 26.4, 32.2), searched with curriculum/tools/openstax.py.
"""
from lib import save, straight_arrow, mirror_path, head_at, r


def ap(section, slug, title):
    return {"title": f"OpenStax Anatomy and Physiology 2e, {section} {title}",
            "url": f"https://openstax.org/books/anatomy-and-physiology-2e/pages/{slug}"}


def bio(section, slug, title):
    return {"title": f"OpenStax Biology 2e, {section} {title}", "url": f"https://openstax.org/books/biology-2e/pages/{slug}"}


LS1_3 = {"title": "NGSS MS-LS1-3: Use argument supported by evidence for how the body is a system of interacting subsystems "
                  "composed of groups of cells"}
LS1_4 = {"title": "NGSS MS-LS1-4: Use argument based on empirical evidence and scientific reasoning to support an explanation "
                  "for how characteristic animal behaviors and specialized plant structures affect the probability of "
                  "successful reproduction of animals and plants respectively"}
LS1_8 = {"title": "NGSS MS-LS1-8: Gather and synthesize information that sensory receptors respond to stimuli by sending "
                  "messages to the brain for immediate behavior or storage as memories"}
NERVOUS = ap("12.1", "12-1-basic-structure-and-function-of-the-nervous-system", "Basic Structure and Function of the Nervous System")
MOTOR = ap("14.3", "14-3-motor-responses", "Motor Responses")
POLLINATION = bio("32.2", "32-2-pollination-and-fertilization", "Pollination and Fertilization")
ANGIOSPERMS = bio("26.3", "26-3-angiosperms", "Angiosperms")


def bean(cx, cy, a, b, d):
    """A bean outline standing upright, its dent on the left: half-width a, half-height b, dent depth d."""
    k = 1.33 * a
    return (f"M {cx} {cy - b} C {r(cx + k)} {cy - b} {r(cx + k)} {cy + b} {cx} {cy + b} "
            f"C {r(cx - k)} {cy + b} {r(cx - a + d)} {r(cy + 0.4 * b)} {r(cx - a + d)} {cy} "
            f"C {r(cx - a + d)} {r(cy - 0.4 * b)} {r(cx - k)} {cy - b} {cx} {cy - b} Z")


def turn(d, cx, cy):
    """Turns an absolute M/L/C/Z path a quarter turn clockwise about (cx, cy)."""
    out, nums = [], []
    for t in d.split() + ["M"]:
        if t.isalpha():
            for x, y in zip(nums[::2], nums[1::2]):
                out += [str(r(cx - (y - cy))), str(r(cy + (x - cx)))]
            nums = []
            out.append(t)
        else:
            nums.append(float(t))
    return " ".join(out[:-1])


def curve_arrow(x0, y0, c1, c2, x1, y1, head=24):
    """A cubic curve from (x0, y0) to (x1, y1) with an arrowhead pointing along its last control leg."""
    dx, dy = x1 - c2[0], y1 - c2[1]
    n = (dx * dx + dy * dy) ** 0.5
    return [{"path": f"M {x0} {y0} C {c1[0]} {c1[1]} {c2[0]} {c2[1]} {x1} {y1}"}, head_at((x1, y1), (dx / n, dy / n), head)]


# ---------------------------------------------------------------- The nervous system
BRAIN = ("M 190 170 C 180 100 250 62 310 76 C 380 60 440 110 430 170 C 440 230 380 262 320 250 "
         "C 260 266 196 236 190 170 Z")
nervous = {
    "id": "g7-nervous-system", "title": "The nervous system", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-3", "minutes": 10,
    "sources": [LS1_3, LS1_8, NERVOUS, ap("13.4", "13-4-the-peripheral-nervous-system", "The Peripheral Nervous System"),
                ap("10.2", "10-2-skeletal-muscle", "Skeletal Muscle (axons bundle together to form nerves)")],
    "keywords": ["nervous system", "brain", "spinal cord", "nerves", "neuron", "nerve cell", "central nervous system",
                 "peripheral nervous system", "CNS", "PNS", "axon", "dendrites", "signals"],
    "printed": [{"text": "A neuron, enlarged", "at": [770, 70], "size": 26}],
    "structures": [
        {"id": "brain", "name": "brain", "pen": "bold", "outlines": [{"path": BRAIN}],
         "details": [{"path": "M 250 120 C 280 150 260 190 300 210"}, {"path": "M 350 110 C 330 150 380 170 360 215"}]},
        {"id": "cord", "name": "spinal cord", "pen": "bold", "outlines": [{"line": [296, 258, 296, 600]}, {"line": [330, 256, 330, 600]}]},
        {"id": "arms", "name": "nerves to the arms", "outlines": [
            {"line": [296, 320, 200, 400, 120, 560]}, {"line": [200, 400, 190, 560]},
            {"line": [330, 320, 426, 400, 506, 560]}, {"line": [426, 400, 436, 560]}]},
        {"id": "legs", "name": "nerves to the legs", "outlines": [
            {"line": [300, 600, 240, 760, 220, 940]}, {"line": [240, 760, 170, 900]},
            {"line": [326, 600, 386, 760, 406, 940]}, {"line": [386, 760, 456, 900]}]},
        {"id": "body", "name": "cell body", "outlines": [{"circle": [770, 250, 48]}], "details": [{"circle": [770, 250, 14]}]},
        {"id": "dendrites", "name": "dendrites", "pen": "fine", "outlines": [
            {"line": [740, 214, 690, 150]}, {"line": [770, 202, 770, 120]}, {"line": [800, 214, 850, 150]},
            {"line": [724, 262, 650, 280]}, {"line": [816, 262, 890, 280]}]},
        {"id": "axon", "name": "axon", "outlines": [{"line": [770, 298, 770, 800]},
                                                   {"line": [770, 800, 710, 880]}, {"line": [770, 800, 770, 890]},
                                                   {"line": [770, 800, 830, 880]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Brain", "structure": "brain", "instruction": "Trace the brain.",
         "note": {"text": "The brain takes in signals from the senses, decides what to do and sends out commands. It's inside the skull."}},
        {"type": "trace", "title": "Folds", "structure": "brain", "part": "details", "instruction": "Draw two folds on the brain.",
         "note": {"text": "The brain's wrinkly folds pack lots of nerve tissue into a small space."}},
        {"type": "trace", "title": "Spinal cord", "structure": "cord", "instruction": "Trace the spinal cord down from the brain.",
         "note": {"text": "The spinal cord runs down inside the backbone. With the brain it forms the central nervous system.",
                  "remember": "Central nervous system: brain + spinal cord."}},
        {"type": "trace", "title": "Arm nerves", "structure": "arms", "instruction": "Trace the nerves branching out to the arms.",
         "note": {"text": "Nerves are cables made of bundles of long nerve-cell fibers. They carry signals to and from the spinal cord."}},
        {"type": "trace", "title": "Leg nerves", "structure": "legs", "instruction": "Trace the nerves to the legs.",
         "note": {"text": "All the nerves outside the brain and spinal cord make up the peripheral nervous system.",
                  "remember": "Peripheral nervous system: all the nerves."}},
        {"type": "trace", "title": "Neuron", "structure": "body", "instruction": "Trace the neuron's cell body, at the right.",
         "note": {"text": "Neurons are the nerve cells that carry signals. The cell body holds the nucleus."}},
        {"type": "trace", "title": "Nucleus", "structure": "body", "part": "details", "instruction": "Draw its nucleus.",
         "note": {"text": "Like other body cells, a neuron has a nucleus."}},
        {"type": "trace", "title": "Dendrites", "structure": "dendrites", "instruction": "Draw the short branches around the cell body.",
         "note": {"text": "Dendrites receive signals from other cells and carry them toward the cell body.", "remember": "Dendrites: signals in."}},
        {"type": "trace", "title": "Axon", "structure": "axon", "instruction": "Draw the long axon and its branching ends.",
         "note": {"text": "The axon carries the signal away from the cell body. Some axons run from the spinal cord all the way to a foot.",
                  "remember": "Axon: signals out."}},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [310, 160], "answer": "Brain", "role": "Processes signals and sends commands."},
             {"n": 2, "at": [313, 450], "answer": "Spinal cord", "role": "Carries signals between brain and body.",
              "mistakes": {"Nerve": "Nerves branch out to the body. This thick cord inside the backbone is the spinal cord."}},
             {"n": 3, "at": [160, 480], "answer": "Nerve", "role": "Cable of nerve fibers."},
             {"n": 4, "at": [770, 250], "answer": "Cell body", "role": "Holds the nucleus."},
             {"n": 5, "at": [770, 560], "answer": "Axon", "role": "Carries the signal away.",
              "mistakes": {"Dendrite": "Dendrites are the short branches that bring signals in. This long fiber is the axon."}}],
         "vocabulary": ["Brain", "Spinal cord", "Nerve", "Cell body", "Axon", "Dendrite", "Muscle"]},
        {"type": "choice", "title": "Two parts", "instruction": "Use the model.", "showsDiagram": True,
         "question": "Which parts make up the central nervous system?",
         "options": [
             {"text": "The brain and the spinal cord", "correct": True,
              "feedback": "Yes. The nerves that branch out to the rest of the body are the peripheral nervous system."},
             {"text": "The brain only", "feedback": "The spinal cord is part of it too. Together they're the central nervous system."},
             {"text": "All the nerves", "feedback": "The nerves branching out to the body are the peripheral nervous system."},
             {"text": "The heart and the brain", "feedback": "The heart is part of the circulatory system. The CNS is the brain and spinal cord."}]},
        {"type": "choice", "title": "Argue", "instruction": "Follow the signal.", "showsDiagram": True,
         "question": "A person's spinal cord is injured in the middle of the back. Why might they be unable to move their legs?",
         "options": [
             {"text": "Commands from the brain can't travel down the cord to the leg nerves", "correct": True,
              "feedback": "Right. The leg muscles are fine, but the signals that tell them to contract can't get past the injury."},
             {"text": "The leg muscles disappear", "feedback": "The muscles are still there. They don't get the brain's signals."},
             {"text": "The brain stops working", "feedback": "The brain still works. Its signals can't pass the injured part of the cord."},
             {"text": "The leg bones break", "feedback": "The bones are fine. The signal path from the brain is cut."}]},
    ],
}

# ---------------------------------------------------------------- The urinary system and kidney
KID_R = bean(330, 260, 55, 100, 28)
BIG = bean(770, 500, 180, 300, 60)
BLADDER = "M 160 640 C 160 610 280 610 280 640 C 300 720 270 770 220 770 C 170 770 140 720 160 640 Z"
pyramids = [{"polygon": [800, 265, 880, 320, 790, 430]}, {"polygon": [905, 405, 905, 475, 805, 482]},
            {"polygon": [905, 525, 905, 595, 805, 518]}, {"polygon": [880, 680, 800, 735, 790, 570]}]
PELVIS = "M 765 420 C 750 460 730 485 700 490 L 700 530 C 730 535 750 560 765 590 C 785 550 785 460 765 420 Z"
urinary = {
    "id": "g7-urinary-system", "title": "The urinary system and kidney", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-3", "minutes": 10,
    "sources": [LS1_3, ap("25.2", "25-2-gross-anatomy-of-urine-transport", "Gross Anatomy of Urine Transport"),
                ap("25.3", "25-3-gross-anatomy-of-the-kidney", "Gross Anatomy of the Kidney"),
                ap("25.5", "25-5-physiology-of-urine-formation", "Physiology of Urine Formation")],
    "keywords": ["urinary system", "kidney", "ureter", "bladder", "urethra", "urine", "nephron", "renal artery", "renal vein",
                 "filter", "waste", "cortex", "medulla", "renal pelvis", "excretion"],
    "printed": [{"text": "Kidney, enlarged", "at": [770, 150], "size": 26}],
    "structures": [
        {"id": "kidneys", "name": "kidneys", "pen": "bold", "outlines": [{"path": mirror_path(KID_R, 220)}, {"path": KID_R}]},
        {"id": "ureters", "name": "ureters", "outlines": [{"line": [143, 270, 190, 622]}, {"line": [297, 270, 250, 622]}]},
        {"id": "bladder", "name": "bladder", "pen": "bold", "outlines": [{"path": BLADDER}]},
        {"id": "urethra", "name": "urethra", "outlines": [{"line": [220, 770, 220, 860]}]},
        {"id": "kidney", "name": "kidney", "pen": "bold", "outlines": [{"path": BIG}]},
        {"id": "medulla", "name": "medulla", "outlines": pyramids},
        {"id": "pelvis", "name": "renal pelvis and ureter", "outlines": [{"path": PELVIS}, {"path": "M 700 512 C 640 512 575 520 555 580 L 555 900"}]},
        {"id": "vessels", "name": "renal artery and vein", "pen": "fine",
         "outlines": straight_arrow(420, 470, 632, 470, head=22) + straight_arrow(632, 410, 420, 410, head=22)},
    ],
    "steps": [
        {"type": "trace", "title": "Kidneys", "structure": "kidneys", "instruction": "Trace the two bean-shaped kidneys.",
         "note": {"text": "Your two kidneys sit against the back wall of your belly, just under the ribs. They clean your blood.",
                  "remember": "Kidneys: filter the blood."}},
        {"type": "trace", "title": "Ureters", "structure": "ureters", "instruction": "Trace the tubes from the kidneys down to the bladder.",
         "note": {"text": "Each kidney sends urine down a tube called a ureter. Muscle in its wall squeezes the urine along in waves."}},
        {"type": "trace", "title": "Bladder", "structure": "bladder", "instruction": "Trace the bladder.",
         "note": {"text": "The bladder is a stretchy, muscular bag that collects urine from both ureters and stores it."}},
        {"type": "trace", "title": "Urethra", "structure": "urethra", "instruction": "Draw the tube that carries urine out of the body.",
         "note": {"text": "When the bladder empties, urine leaves the body through the urethra.",
                  "remember": "Kidney, ureter, bladder, urethra."}},
        {"type": "trace", "title": "Inside a kidney", "structure": "kidney", "instruction": "Trace the enlarged kidney, at the right.",
         "note": {"text": "The outer layer is the cortex. Each kidney holds over a million tiny filters, called nephrons."}},
        {"type": "trace", "title": "Medulla", "structure": "medulla", "instruction": "Trace the four triangles in the middle layer.",
         "note": {"text": "The middle layer, the medulla, is made of cone-shaped pyramids. Tiny ducts in them carry urine inward."}},
        {"type": "trace", "title": "Collecting urine", "structure": "pelvis", "instruction": "Trace the funnel and the ureter leaving the kidney.",
         "note": {"text": "Urine drains into a funnel, the renal pelvis, which narrows to become the ureter."}},
        {"type": "trace", "title": "Blood in and out", "structure": "vessels", "instruction": "Draw the two arrows: blood in, then blood out.",
         "note": {"text": "The renal artery brings blood in to be cleaned. The renal vein carries the cleaned blood back toward the heart.",
                  "remember": "Artery in, vein out."}},
        {"type": "order", "title": "Urine's path", "instruction": "Tap the parts in the order urine passes through them.",
         "items": ["Kidney", "Ureter", "Bladder", "Urethra"],
         "why": "Kidneys make urine, ureters carry it down, the bladder stores it, and the urethra carries it out.",
         "hint": "Start where urine is made."},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [330, 260], "answer": "Kidney", "role": "Filters the blood."},
             {"n": 2, "at": [270, 450], "answer": "Ureter", "role": "Carries urine to the bladder.",
              "mistakes": {"Urethra": "The urethra carries urine out of the body. This tube from the kidney is a ureter."}},
             {"n": 3, "at": [220, 700], "answer": "Bladder", "role": "Stores urine."},
             {"n": 4, "at": [220, 830], "answer": "Urethra", "role": "Carries urine out."},
             {"n": 5, "at": [860, 440], "answer": "Medulla", "role": "Pyramids of tiny ducts.",
              "mistakes": {"Cortex": "The cortex is the outer layer. These triangles are in the middle layer, the medulla."}}],
         "vocabulary": ["Kidney", "Ureter", "Bladder", "Urethra", "Medulla", "Cortex", "Liver"]},
        {"type": "choice", "title": "Most comes back", "instruction": "Think about the numbers.", "showsDiagram": True,
         "question": "Each day the kidneys filter about 180 L of fluid from the blood, but make only 1 to 2 L of urine. Where does the rest go?",
         "options": [
             {"text": "About 99% is taken back into the blood", "correct": True,
              "feedback": "Yes. The nephrons keep the water and nutrients the body needs and send only wastes and extra water out."},
             {"text": "It's stored in the bladder", "feedback": "The bladder holds only urine, which is 1 to 2 L a day. The rest returns to the blood."},
             {"text": "It's breathed out", "feedback": "The lungs breathe out a little water, but the nephrons return almost all the fluid to the blood."},
             {"text": "It's lost as sweat", "feedback": "Sweat comes from the skin. The kidneys return almost all the filtered fluid to the blood."}]},
        {"type": "choice", "title": "Systems working together", "instruction": "Use the model.", "showsDiagram": True,
         "question": "Which system brings wastes from the body's cells to the kidneys?",
         "options": [
             {"text": "The circulatory system: blood carries the wastes in by the renal artery", "correct": True,
              "feedback": "Right. Cells dump waste into the blood, and the kidneys clean the blood as it passes through."},
             {"text": "The digestive system", "feedback": "Digestive waste leaves through the rectum. Cell wastes travel in the blood."},
             {"text": "The nervous system", "feedback": "Nerves carry signals, not wastes. The blood brings wastes to the kidneys."},
             {"text": "The respiratory system", "feedback": "The lungs remove carbon dioxide. Other wastes travel in the blood to the kidneys."}]},
    ],
}

# ---------------------------------------------------------------- A reflex arc
FLAME = "M 160 540 C 110 510 120 450 160 390 C 170 440 190 450 200 420 C 230 470 220 520 160 540 Z"
HAND = "M 120 350 C 170 310 260 300 330 310 L 330 270 C 260 260 200 250 140 270 C 100 290 90 330 120 350 Z"
GRAY = ("M 750 285 C 700 250 660 270 680 320 C 690 350 720 360 735 375 C 715 400 690 420 700 450 C 720 470 745 440 750 420 "
        "C 755 440 780 470 800 450 C 810 420 785 400 765 375 C 780 360 810 350 820 320 C 840 270 800 250 750 285 Z")
reflex = {
    "id": "g7-reflex-arc", "title": "A reflex arc", "grade": "7", "subject": "Life science", "standard": "MS-LS1-8",
    "minutes": 9,
    "sources": [LS1_8, MOTOR, ap("14.1", "14-1-sensory-perception", "Sensory Perception"), NERVOUS],
    "keywords": ["reflex", "reflex arc", "withdrawal reflex", "sensory neuron", "motor neuron", "interneuron", "spinal cord",
                 "receptor", "stimulus", "response", "hot stove", "nervous system"],
    "printed": [{"text": "To the brain", "at": [880, 80], "size": 26}, {"text": "Spinal cord", "at": [750, 550], "size": 26},
                {"text": "Hot!", "at": [250, 480], "size": 28},
                {"text": "Arm muscle", "at": [425, 640], "size": 24}],
    "structures": [
        {"id": "hand", "name": "hand", "outlines": [{"path": HAND}]},
        {"id": "flame", "name": "flame", "outlines": [{"path": FLAME}]},
        {"id": "cord", "name": "spinal cord", "pen": "bold", "outlines": [{"circle": [750, 365, 140]}], "details": [{"path": GRAY}]},
        {"id": "sensory", "name": "sensory neuron", "outlines": curve_arrow(330, 290, (450, 280), (580, 250), 696, 300)},
        {"id": "inter", "name": "interneuron", "pen": "bold", "outlines": [{"line": [702, 316, 728, 432]}]},
        {"id": "motor", "name": "motor neuron", "outlines": curve_arrow(730, 446, (690, 560), (600, 575), 512, 565)},
        {"id": "muscle", "name": "muscle", "pen": "bold", "outlines": [{"ellipse": [425, 565, 80, 38]}]},
        {"id": "up", "name": "signal to the brain", "pen": "fine", "outlines": straight_arrow(800, 240, 860, 120, head=22)},
    ],
    "steps": [
        {"type": "trace", "title": "Hand", "structure": "hand", "instruction": "Trace the hand.",
         "note": {"text": "Your skin has sensory receptors. Some respond to heat or pain."}},
        {"type": "trace", "title": "Stimulus", "structure": "flame", "instruction": "Trace the flame under the hand.",
         "note": {"text": "A stimulus is a change a receptor can detect, like the heat of a hot stove.", "remember": "Stimulus: what you sense."}},
        {"type": "trace", "title": "Spinal cord", "structure": "cord", "instruction": "Trace the spinal cord, cut across.",
         "note": {"text": "This is a slice across the spinal cord. Signals from the body enter it through nerves."}},
        {"type": "trace", "title": "Gray matter", "structure": "cord", "part": "details", "instruction": "Draw the butterfly shape inside.",
         "note": {"text": "The butterfly-shaped gray matter is where neurons connect to each other."}},
        {"type": "trace", "title": "Sensory neuron", "structure": "sensory", "instruction": "Draw the signal from the hand to the spinal cord.",
         "note": {"text": "Receptors start a signal. A sensory neuron carries it from the skin to the spinal cord.",
                  "remember": "Sensory neuron: body to spinal cord."}},
        {"type": "trace", "title": "Interneuron", "structure": "inter", "instruction": "Draw the short neuron inside the spinal cord.",
         "note": {"text": "In the spinal cord, the signal passes to another neuron, which connects straight to a motor neuron."}},
        {"type": "trace", "title": "Motor neuron", "structure": "motor", "instruction": "Draw the signal back out to the arm muscle.",
         "note": {"text": "A motor neuron carries the command out to a muscle.", "remember": "Motor neuron: spinal cord to muscle."}},
        {"type": "trace", "title": "Response", "structure": "muscle", "instruction": "Trace the arm muscle.",
         "note": {"text": "The biceps contracts and pulls your hand away. This fast, automatic response is a reflex."}},
        {"type": "trace", "title": "Message to the brain", "structure": "up", "instruction": "Draw the arrow going up to the brain.",
         "note": {"text": "Signals also travel up to the brain. You feel the pain, and you can remember not to touch the stove again."}},
        {"type": "order", "title": "The reflex arc", "instruction": "Tap the steps in order.",
         "items": ["Receptor senses heat", "Sensory neuron", "Spinal cord", "Motor neuron", "Muscle pulls the hand away"],
         "why": "The signal goes in on a sensory neuron, connects in the spinal cord and comes back out on a motor neuron.",
         "hint": "It starts in the skin and ends at a muscle."},
        {"type": "choice", "title": "Why so fast?", "instruction": "Follow the arrows.", "showsDiagram": True,
         "question": "Why can you pull your hand away before you even feel the pain?",
         "options": [
             {"text": "The signal turns around in the spinal cord, without waiting for the brain", "correct": True,
              "feedback": "Yes. The short path is fast, so less damage is done. The brain gets the message a moment later."},
             {"text": "Muscles can sense heat", "feedback": "Muscles don't sense heat. Receptors in the skin do, and nerves carry the signal."},
             {"text": "The brain decides very fast", "feedback": "The brain isn't in the loop. The signal connects in the spinal cord."},
             {"text": "The hand moves by itself", "feedback": "Something has to signal the muscle: a motor neuron from the spinal cord."}]},
        {"type": "choice", "title": "Memory", "instruction": "Think about the arrow up to the brain.", "showsDiagram": True,
         "question": "What does the signal that reaches the brain let you do?",
         "options": [
             {"text": "Feel the pain and remember to avoid the stove next time", "correct": True,
              "feedback": "Right. Messages to the brain can lead to action now or be stored as memories."},
             {"text": "Pull your hand away", "feedback": "The spinal cord already did that. The brain lets you feel it and remember."},
             {"text": "Nothing: the brain ignores it", "feedback": "The brain does get the message. That's how you feel the pain."},
             {"text": "Cool down the stove", "feedback": "Your body can't change the stove. The brain lets you learn to avoid it."}]},
    ],
}

# ---------------------------------------------------------------- Pollination and the pollen tube
CARPEL = ("M 476 180 C 440 160 450 112 500 110 C 550 112 560 160 524 180 L 524 470 C 640 500 660 700 560 760 "
          "C 520 780 480 780 440 760 C 340 700 360 500 476 470 Z")
PETAL = "M 560 792 C 700 770 860 640 900 430 C 790 450 690 560 615 760 Z"
ovules = [(430, 670), (500, 700), (570, 670)]
pollination = {
    "id": "g7-pollination", "title": "Pollination and the pollen tube", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-4", "minutes": 9,
    "sources": [LS1_4, POLLINATION, ANGIOSPERMS, bio("26.4", "26-4-the-role-of-seed-plants", "The Role of Seed Plants"),
                bio("26.1", "26-1-evolution-of-seed-plants", "Evolution of Seed Plants")],
    "keywords": ["pollination", "pollen", "pollen tube", "anther", "stamen", "stigma", "style", "ovary", "ovule", "carpel",
                 "pistil", "fertilization", "seed", "fruit", "bee", "pollinator", "nectar"],
    "printed": [{"text": "Carried by a bee or the wind", "at": [250, 60], "size": 24}],
    "structures": [
        {"id": "stamen", "name": "stamen", "outlines": [{"ellipse": [250, 300, 34, 56]}, {"line": [250, 360, 260, 840]}]},
        {"id": "carpel", "name": "carpel", "pen": "bold", "outlines": [{"path": CARPEL}]},
        {"id": "ovules", "name": "ovules", "outlines": [{"ellipse": [x, y, 22, 30]} for x, y in ovules]},
        {"id": "carry", "name": "pollen carried to the stigma", "pen": "fine",
         "outlines": curve_arrow(260, 230, (280, 110), (380, 70), 450, 100)},
        {"id": "tube", "name": "pollen tube", "pen": "fine",
         "outlines": [{"path": "M 500 140 L 500 470 C 500 560 500 610 500 662"}], "details": [{"circle": [500, 132, 10]}]},
        {"id": "petal", "name": "petal", "outlines": [{"path": PETAL}]},
    ],
    "steps": [
        {"type": "trace", "title": "Stamen", "structure": "stamen", "instruction": "Trace the stamen: the anther on its stalk.",
         "note": {"text": "The anther at the top of the stamen makes pollen. Pollen grains carry the plant's sperm.",
                  "remember": "Anther: makes pollen."}},
        {"type": "trace", "title": "Carpel", "structure": "carpel", "instruction": "Trace the carpel: stigma, style and ovary.",
         "note": {"text": "The sticky stigma on top traps pollen. A stalk, the style, leads down to the ovary at the bottom."}},
        {"type": "trace", "title": "Ovules", "structure": "ovules", "instruction": "Trace the three ovules inside the ovary.",
         "note": {"text": "Each ovule holds an egg cell. Each ovule can become a seed.", "remember": "Ovule becomes a seed."}},
        {"type": "trace", "title": "Pollination", "structure": "carry", "instruction": "Draw pollen moving from the anther to the stigma.",
         "note": {"text": "Pollination is pollen landing on a stigma. Insects, birds, wind or water carry it, often from another flower."}},
        {"type": "trace", "title": "Pollen tube", "structure": "tube", "instruction": "Draw the pollen tube growing down the style.",
         "note": {"text": "The pollen grain grows a tube down through the style to an ovule. The sperm travel down inside it.",
                  "remember": "Pollen tube: carries sperm to the egg."}},
        {"type": "trace", "title": "Pollen grain", "structure": "tube", "part": "details", "instruction": "Dab the pollen grain on the stigma.",
         "note": {"text": "When a sperm joins the egg in the ovule, that's fertilization. The ovule then grows into a seed."}},
        {"type": "trace", "title": "Petal", "structure": "petal", "instruction": "Trace one petal.",
         "note": {"text": "Bright petals, scent and sweet nectar draw in animals. As they feed, pollen dusts their bodies."}},
        {"type": "order", "title": "From pollen to seed", "instruction": "Tap the steps in order.",
         "items": ["Anther makes pollen", "Pollen lands on the stigma", "Pollen tube grows down the style", "Sperm joins the egg",
                   "Ovule becomes a seed"],
         "why": "Pollen is carried to the stigma, grows a tube to the ovule, and fertilization turns the ovule into a seed.",
         "hint": "Pollination comes before fertilization."},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [250, 300], "answer": "Anther", "role": "Makes pollen."},
             {"n": 2, "at": [500, 145], "answer": "Stigma", "role": "Sticky tip that traps pollen.",
              "mistakes": {"Anther": "The anther makes pollen. The sticky tip that catches it is the stigma."}},
             {"n": 3, "at": [500, 330], "answer": "Style", "role": "The pollen tube grows down it."},
             {"n": 4, "at": [610, 600], "answer": "Ovary", "role": "Becomes the fruit."},
             {"n": 5, "at": [430, 670], "answer": "Ovule", "role": "Becomes a seed.",
              "mistakes": {"Ovary": "The ovary is the whole chamber. Each small oval inside it is an ovule."}}],
         "vocabulary": ["Anther", "Stigma", "Style", "Ovary", "Ovule", "Petal", "Sepal"]},
        {"type": "choice", "title": "Argue", "instruction": "Think about reproduction.", "showsDiagram": True,
         "question": "How do bright petals and sweet nectar help a plant reproduce?",
         "options": [
             {"text": "They attract animals that carry pollen between flowers, so more ovules get fertilized", "correct": True,
              "feedback": "Yes. More pollinator visits mean more pollen reaches stigmas, so the plant is likelier to make seeds."},
             {"text": "They make food for the seeds", "feedback": "Petals don't feed seeds. They attract the animals that carry pollen."},
             {"text": "They scare away animals", "feedback": "They do the opposite: they attract the pollinators the plant needs."},
             {"text": "They make pollen", "feedback": "The anthers make pollen. Petals attract animals that carry it."}]},
        {"type": "choice", "title": "Fruit", "instruction": "After fertilization.", "showsDiagram": True,
         "question": "After the ovules become seeds, what does the ovary around them become?",
         "options": [
             {"text": "The fruit", "correct": True,
              "feedback": "Right. The ovary wall thickens into a fruit that protects the seeds and helps spread them."},
             {"text": "A new flower", "feedback": "The ovary becomes the fruit. New flowers grow from new buds."},
             {"text": "Pollen", "feedback": "Pollen comes from anthers. The ovary becomes the fruit."},
             {"text": "A root", "feedback": "Roots grow from a seed's embryo after it sprouts. The ovary becomes the fruit."}]},
    ],
}

# ---------------------------------------------------------------- Inside a bean seed
COAT = turn(bean(320, 470, 160, 250, 60), 320, 470)
COTYLEDON = turn(bean(320, 470, 132, 220, 50), 320, 470)
RADICLE = "M 400 520 C 370 528 330 545 296 576 C 288 586 300 596 312 588 C 345 566 380 556 410 548 Z"
PLUMULE = "M 410 535 C 420 500 455 485 480 492 C 470 515 445 535 410 535 Z"
LEAF = "M 790 250 C 740 240 690 200 680 150 C 735 150 780 190 790 250 Z"
GREEN, TAN = "#6BA368", "#E9D9A6"
seed = {
    "id": "g7-bean-seed", "title": "Inside a bean seed", "grade": "7", "subject": "Life science", "standard": "MS-LS1-4",
    "minutes": 9, "colorMode": "illustration",
    "sources": [LS1_4, POLLINATION, ANGIOSPERMS],
    "keywords": ["seed", "bean", "seed coat", "cotyledon", "embryo", "radicle", "plumule", "hypocotyl", "germination",
                 "seedling", "dicot", "stored food"],
    "printed": [{"text": "Opened bean seed", "at": [320, 170], "size": 26}, {"text": "Seedling", "at": [800, 80], "size": 26},
                {"text": "Soil", "at": [960, 600], "size": 22}],
    "legend": [{"name": "Stored food", "color": TAN, "meaning": "The cotyledon is packed with food"},
               {"name": "Leaves", "color": GREEN, "meaning": "Green, so they can make food from sunlight"}],
    "structures": [
        {"id": "coat", "name": "seed coat", "pen": "bold", "outlines": [{"path": COAT}]},
        {"id": "cotyledon", "name": "cotyledon", "colorName": "stored food", "fill": TAN, "outlines": [{"path": COTYLEDON}]},
        {"id": "radicle", "name": "radicle", "outlines": [{"path": RADICLE}]},
        {"id": "plumule", "name": "plumule", "outlines": [{"path": PLUMULE}]},
        {"id": "soil", "name": "soil line", "pen": "fine", "outlines": [{"line": [620, 560, 980, 560]}]},
        {"id": "root", "name": "root", "outlines": [{"line": [800, 560, 800, 880]}, {"line": [800, 660, 730, 740]},
                                                   {"line": [800, 720, 870, 800]}]},
        {"id": "stem", "name": "stem", "pen": "bold", "outlines": [{"line": [800, 540, 800, 260]}]},
        {"id": "seed-leaves", "name": "cotyledons", "colorName": "stored food", "fill": TAN,
         "outlines": [{"ellipse": [752, 400, 44, 24]}, {"ellipse": [848, 400, 44, 24]}]},
        {"id": "leaves", "name": "first leaves", "colorName": "leaves", "fill": GREEN, "outlines": [{"path": LEAF}, {"path": mirror_path(LEAF, 800)}]},
    ],
    "steps": [
        {"type": "trace", "title": "Seed coat", "structure": "coat", "instruction": "Trace the seed coat around the opened bean.",
         "note": {"text": "A seed is a baby plant packed with food inside a tough coat. The coat protects it until it sprouts.",
                  "remember": "Seed coat: protects."}},
        {"type": "trace", "title": "Cotyledon", "structure": "cotyledon", "instruction": "Trace the big half that fills the seed.",
         "note": {"text": "A bean splits into two halves, the cotyledons, or seed leaves. They're packed with stored food.",
                  "remember": "Cotyledons: stored food."}},
        {"type": "trace", "title": "Radicle", "structure": "radicle", "instruction": "Trace the tiny root tip of the embryo.",
         "note": {"text": "The embryo is the baby plant. Its radicle, the embryonic root, grows into the plant's first root."}},
        {"type": "trace", "title": "Plumule", "structure": "plumule", "instruction": "Trace the tiny folded leaves.",
         "note": {"text": "The plumule holds the first young leaves and the shoot tip.", "remember": "Radicle: root. Plumule: leaves."}},
        {"type": "trace", "title": "Soil", "structure": "soil", "instruction": "Draw the soil line for the seedling.",
         "note": {"text": "When a seed gets water and warmth, it sprouts. This is germination."}},
        {"type": "trace", "title": "Root", "structure": "root", "instruction": "Trace the root growing down.",
         "note": {"text": "The radicle comes out first and grows down into a root that takes in water."}},
        {"type": "trace", "title": "Stem", "structure": "stem", "instruction": "Trace the stem growing up.",
         "note": {"text": "In a bean, the stem below the seed leaves grows and lifts them up out of the soil."}},
        {"type": "trace", "title": "Seed leaves", "structure": "seed-leaves", "instruction": "Trace the two cotyledons on the stem.",
         "note": {"text": "The seedling lives on the food in the cotyledons until its first leaves can make food."}},
        {"type": "trace", "title": "First leaves", "structure": "leaves", "instruction": "Trace the first leaves at the top.",
         "note": {"text": "The plumule grows into the first true leaves, which make food by photosynthesis."}},
        {"type": "color", "title": "Color", "structures": ["cotyledon", "seed-leaves", "leaves"],
         "instruction": "Color the stored food tan and the leaves green."},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [320, 400], "answer": "Cotyledon", "synonyms": ["Seed leaf"], "role": "Stores food.",
              "mistakes": {"Seed coat": "The seed coat is the thin outer layer. This big food store is a cotyledon."}},
             {"n": 2, "at": [330, 570], "answer": "Radicle", "role": "Becomes the root."},
             {"n": 3, "at": [455, 510], "answer": "Plumule", "role": "Becomes the first leaves.",
              "mistakes": {"Radicle": "The radicle becomes the root. These tiny leaves are the plumule."}},
             {"n": 4, "at": [800, 800], "answer": "Root", "role": "Grew from the radicle."}],
         "vocabulary": ["Seed coat", "Cotyledon", "Radicle", "Plumule", "Root", "Pollen"]},
        {"type": "choice", "title": "Food before leaves", "instruction": "Use the model.", "showsDiagram": True,
         "question": "A seed sprouts underground in the dark. Where does it get food to grow?",
         "options": [
             {"text": "From the food stored in its cotyledons", "correct": True,
              "feedback": "Yes. The stored food lasts until the first leaves reach light and start photosynthesis."},
             {"text": "From sunlight through the seed coat", "feedback": "It's dark underground. The seedling uses food stored in the cotyledons."},
             {"text": "From the soil only", "feedback": "Roots take in water and minerals, but the food comes from the cotyledons."},
             {"text": "From the flower", "feedback": "The seed has left the parent plant. Its food is packed in the cotyledons."}]},
        {"type": "choice", "title": "Argue", "instruction": "Think about reproduction.", "showsDiagram": False,
         "question": "How does the seed coat help a plant reproduce?",
         "options": [
             {"text": "It protects the embryo, so it survives until conditions are right to sprout", "correct": True,
              "feedback": "Right. A protected seed can wait out cold or drought, so its chance of growing into a plant goes up."},
             {"text": "It makes the seed's food", "feedback": "The food is stored in the cotyledons. The coat protects the embryo."},
             {"text": "It grows into the root", "feedback": "The radicle becomes the root. The coat protects the embryo."},
             {"text": "It attracts bees", "feedback": "Petals attract bees. The seed coat protects the embryo inside."}]},
    ],
}

for lesson in (nervous, urinary, reflex, pollination, seed):
    save(lesson)
