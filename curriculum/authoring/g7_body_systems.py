"""Grade 7 body systems (MS-LS1-3) · levels of organization, the circulatory, respiratory and digestive systems, and
the biceps and triceps.

Facts checked against OpenStax Anatomy and Physiology 2e (1.2, 10.4, 11.1, 19.1, 20.5, 22.1, 22.3, 23.1, 23.2, 23.5),
searched with curriculum/tools/openstax.py.
"""
from lib import save, straight_arrow, mirror_path, r


def ap(section, slug, title):
    return {"title": f"OpenStax Anatomy and Physiology 2e, {section} {title}",
            "url": f"https://openstax.org/books/anatomy-and-physiology-2e/pages/{slug}"}


LS1_3 = {"title": "NGSS MS-LS1-3: Use argument supported by evidence for how the body is a system of interacting subsystems "
                  "composed of groups of cells"}
LEVELS = ap("1.2", "1-2-structural-organization-of-the-human-body", "Structural Organization of the Human Body")
HEART = ap("19.1", "19-1-heart-anatomy", "Heart Anatomy")
PATHWAYS = ap("20.5", "20-5-circulatory-pathways", "Circulatory Pathways")
DIGESTION = ap("23.2", "23-2-digestive-system-processes-and-regulation", "Digestive System Processes and Regulation")
OXY_POOR, OXY_RICH = "#7A1F2B", "#D2342C"  # the same blood colors as the grade 4 heart


def scale_path(d, k, cx, cy, to_x, to_y):
    """Scales an absolute M/L/C/Z path by k about (cx, cy) and moves that point to (to_x, to_y)."""
    out, is_x = [], True
    for t in d.split():
        if t.isalpha(): out.append(t); is_x = True
        else:
            v = float(t)
            out.append(str(r(to_x + (v - cx) * k) if is_x else r(to_y + (v - cy) * k)))
            is_x = not is_x
    return " ".join(out)


HEART_OUTLINE = ("M 330 340 C 330 272 420 252 500 272 C 600 250 706 290 706 384 C 706 520 626 642 566 756 "
                 "C 546 790 518 792 498 770 C 398 668 314 520 330 340 Z")


def heart_at(k, x, y):
    return {"path": scale_path(HEART_OUTLINE, k, 510, 520, x, y)}


def rrect(x, y, w, h, rad):
    return {"rect": [x, y, w, h, rad]}


# ---------------------------------------------------------------- Levels of organization
tissue = [rrect(379 + c * 86 + (20 if row % 2 else 0) - 10, 133 + row * 50, 70, 34, 14) for row in range(3) for c in range(3)]
PERSON = ("M 705 590 L 795 590 L 850 700 L 828 712 L 795 650 L 795 770 L 820 910 L 790 910 L 750 800 L 710 910 L 680 910 "
          "L 705 770 L 705 650 L 672 712 L 650 700 Z")
levels = {
    "id": "g7-levels-of-organization", "title": "Levels of organization: cell to organism", "grade": "7",
    "subject": "Life science", "standard": "MS-LS1-3", "minutes": 9,
    "sources": [LS1_3, LEVELS, HEART],
    "keywords": ["levels of organization", "cell", "tissue", "organ", "organ system", "organism", "heart", "muscle",
                 "circulatory system", "body systems"],
    "structures": [
        {"id": "cell", "name": "heart muscle cell", "outlines": [rrect(70, 170, 160, 60, 22)], "details": [{"ellipse": [150, 200, 22, 13]}]},
        {"id": "tissue", "name": "heart muscle tissue", "outlines": tissue},
        {"id": "organ", "name": "heart", "pen": "bold", "outlines": [heart_at(0.36, 860, 205)]},
        {"id": "system", "name": "circulatory system", "outlines": [heart_at(0.2, 300, 600),
                                                                   {"path": "M 262 625 C 110 660 120 900 300 905 C 480 900 490 660 338 625"}]},
        {"id": "organism", "name": "person", "outlines": [{"circle": [750, 538, 44]}, {"path": PERSON}]},
        {"id": "arrows", "name": "arrows", "pen": "bold",
         "outlines": straight_arrow(250, 200, 345, 200, head=22) + straight_arrow(655, 200, 745, 200, head=22)
                     + straight_arrow(800, 340, 430, 560, head=22) + straight_arrow(480, 760, 630, 760, head=22)},
    ],
    "steps": [
        {"type": "trace", "title": "Cell", "structure": "cell", "instruction": "Trace the heart muscle cell.",
         "note": {"text": "Cells are the smallest units of life. In humans, cells carry out all the functions of life.",
                  "remember": "Level 1: cell."}},
        {"type": "trace", "title": "Nucleus", "structure": "cell", "part": "details", "instruction": "Draw its nucleus.",
         "note": {"text": "Each heart muscle cell can shorten, or contract."}},
        {"type": "trace", "title": "Tissue", "structure": "tissue", "instruction": "Trace the nine cells joined together.",
         "note": {"text": "A tissue is a group of similar cells working together. Heart muscle cells form heart muscle tissue.",
                  "remember": "Level 2: tissue."}},
        {"type": "trace", "title": "Organ", "structure": "organ", "instruction": "Trace the heart.",
         "note": {"text": "An organ is built from two or more kinds of tissue. The heart has muscle, nerve and other tissues.",
                  "remember": "Level 3: organ."}},
        {"type": "trace", "title": "Organ system", "structure": "system", "instruction": "Trace the small heart and the loop of blood vessels.",
         "note": {"text": "An organ system is a group of organs working together. The heart and blood vessels form the circulatory system.",
                  "remember": "Level 4: organ system."}},
        {"type": "trace", "title": "Organism", "structure": "organism", "instruction": "Trace the person.",
         "note": {"text": "Eleven organ systems work together to keep one whole organism alive: you.", "remember": "Level 5: organism."}},
        {"type": "trace", "title": "Building up", "structure": "arrows", "instruction": "Draw the four arrows from smallest to largest.",
         "note": {"text": "Each level is built from the one before it."}},
        {"type": "order", "title": "Smallest to largest", "items": ["Cell", "Tissue", "Organ", "Organ system", "Organism"],
         "instruction": "Tap the levels in order, smallest first.",
         "why": "Cells form tissues, tissues form organs, organs form organ systems, and organ systems make up the organism.",
         "hint": "Start with the smallest living unit."},
        {"type": "label", "title": "Name the levels", "instruction": "Pick the level for each numbered drawing.",
         "targets": [
             {"n": 1, "at": [150, 200], "answer": "Cell", "role": "Smallest unit of life."},
             {"n": 2, "at": [500, 200], "answer": "Tissue", "role": "Similar cells working together.",
              "mistakes": {"Organ": "This is a group of one kind of cell. An organ has two or more kinds of tissue."}},
             {"n": 3, "at": [860, 205], "answer": "Organ", "role": "Made of several tissues."},
             {"n": 4, "at": [300, 760], "answer": "Organ system", "role": "Organs working together."},
             {"n": 5, "at": [750, 700], "answer": "Organism", "role": "A whole living thing."}],
         "vocabulary": ["Cell", "Tissue", "Organ", "Organ system", "Organism", "Organelle"]},
        {"type": "choice", "title": "Argue", "instruction": "Use the model.", "showsDiagram": True,
         "question": "Heart muscle cells stop getting oxygen. Why can this harm the whole body?",
         "options": [
             {"text": "The cells form the tissue that makes the heart pump, and the body depends on that blood flow", "correct": True,
              "feedback": "Yes. Each level depends on the one below: weak cells mean a weak heart, and every system needs blood."},
             {"text": "It can't: cells are too small to matter", "feedback": "Everything the body does is done by cells. The levels depend on each other."},
             {"text": "Only the heart is affected", "feedback": "The heart pumps blood to every organ, so the whole body is affected."},
             {"text": "Other cells will grow a new heart", "feedback": "The body can't grow a new heart. Damaged heart cells affect the whole system."}]},
    ],
}

# ---------------------------------------------------------------- The circulatory system
circulation = {
    "id": "g7-circulatory-system", "title": "The circulatory system", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-3", "minutes": 11, "colorMode": "illustration",
    "sources": [LS1_3, HEART, PATHWAYS, ap("5.1", "5-1-layers-of-the-skin", "Layers of the Skin (oxygen-poor blood is dark red)")],
    "keywords": ["circulatory system", "heart", "arteries", "veins", "capillaries", "pulmonary circuit", "systemic circuit",
                 "oxygen", "carbon dioxide", "blood", "lungs", "double circulation"],
    "printed": [{"text": "Lungs", "at": [500, 70], "size": 30}, {"text": "Body", "at": [500, 960], "size": 30},
                {"text": "Heart", "at": [500, 380], "size": 28}],
    "legend": [{"name": "Oxygen-poor blood", "color": OXY_POOR, "meaning": "Dark red. Diagrams often use blue, but blood is never blue."},
               {"name": "Oxygen-rich blood", "color": OXY_RICH, "meaning": "Bright red"},
               {"name": "Lungs", "color": "#E8A0A0", "meaning": "Pink, spongy tissue"}],
    "structures": [
        {"id": "right", "name": "right atrium and ventricle", "colorName": "oxygen-poor blood", "fill": OXY_POOR,
         "outlines": [rrect(340, 410, 140, 110, 20), rrect(340, 545, 140, 140, 20)]},
        {"id": "left", "name": "left atrium and ventricle", "colorName": "oxygen-rich blood", "fill": OXY_RICH,
         "outlines": [rrect(520, 410, 140, 110, 20), rrect(520, 545, 140, 140, 20)]},
        {"id": "lungs", "name": "lung capillaries", "colorName": "lungs", "fill": "#E8A0A0", "outlines": [rrect(330, 95, 340, 120, 40)]},
        {"id": "pa", "name": "pulmonary artery", "outlines": [{"line": [340, 620, 240, 620, 240, 155, 326, 155]}]
                                                             + straight_arrow(290, 155, 326, 155, head=20)[1:]},
        {"id": "pv", "name": "pulmonary vein", "outlines": [{"line": [670, 155, 760, 155, 760, 465, 662, 465]}]
                                                           + straight_arrow(700, 465, 662, 465, head=20)[1:]},
        {"id": "body", "name": "body capillaries", "outlines": [rrect(330, 800, 340, 120, 40)]},
        {"id": "aorta", "name": "aorta", "outlines": [{"line": [660, 615, 840, 615, 840, 860, 672, 860]}]
                                                     + straight_arrow(710, 860, 672, 860, head=20)[1:]},
        {"id": "vc", "name": "vena cava", "outlines": [{"line": [330, 860, 160, 860, 160, 465, 338, 465]}]
                                                     + straight_arrow(300, 465, 338, 465, head=20)[1:]},
    ],
    "steps": [
        {"type": "trace", "title": "Right side", "structure": "right", "instruction": "Trace the heart's right atrium and right ventricle.",
         "note": {"text": "The heart is two pumps side by side. The right side pumps blood to the lungs.",
                  "remember": "Right side: to the lungs."}},
        {"type": "trace", "title": "Left side", "structure": "left", "instruction": "Trace the left atrium and left ventricle.",
         "note": {"text": "The left side pumps blood out to the rest of the body.", "remember": "Left side: to the body."}},
        {"type": "trace", "title": "Lungs", "structure": "lungs", "instruction": "Trace the lungs' tiny blood vessels at the top.",
         "note": {"text": "In the lungs, blood flows through capillaries, vessels so thin that gases pass through their walls."}},
        {"type": "trace", "title": "To the lungs", "structure": "pa", "instruction": "Draw the vessel from the right ventricle up to the lungs.",
         "note": {"text": "The pulmonary artery carries oxygen-poor blood to the lungs, where it drops carbon dioxide and picks up oxygen."}},
        {"type": "trace", "title": "Back from the lungs", "structure": "pv", "instruction": "Draw the vessel from the lungs to the left atrium.",
         "note": {"text": "Pulmonary veins bring the oxygen-rich blood back to the heart. This loop is the pulmonary circuit.",
                  "remember": "Pulmonary circuit: heart, lungs, heart."}},
        {"type": "trace", "title": "Body", "structure": "body", "instruction": "Trace the body's capillaries at the bottom.",
         "note": {"text": "In the body's capillaries, oxygen and food pass out to the cells, and waste like carbon dioxide passes in."}},
        {"type": "trace", "title": "Aorta", "structure": "aorta", "instruction": "Draw the aorta from the left ventricle down to the body.",
         "note": {"text": "Arteries carry blood away from the heart. The aorta, the biggest, carries oxygen-rich blood to the body.",
                  "remember": "Arteries: away from the heart."}},
        {"type": "trace", "title": "Vena cava", "structure": "vc", "instruction": "Draw the vena cava from the body back to the right atrium.",
         "note": {"text": "Veins carry blood back to the heart. This loop through the body is the systemic circuit.",
                  "remember": "Veins: back to the heart."}},
        {"type": "color", "title": "Color", "structures": ["right", "left", "lungs"],
         "instruction": "Color the heart's two sides and the lungs. Oxygen-poor blood is dark red; oxygen-rich is bright red."},
        {"type": "order", "title": "One full trip", "instruction": "Tap the stops in order, starting at the right ventricle.",
         "items": ["Right ventricle", "Lungs", "Left atrium", "Left ventricle", "Body", "Right atrium"],
         "why": "Blood makes two loops: right side to the lungs and back to the left side, then left side to the body and back.",
         "hint": "Where does blood pick up oxygen?"},
        {"type": "choice", "title": "Systems working together", "instruction": "Use the model.", "showsDiagram": True,
         "question": "How do the circulatory and respiratory systems work together?",
         "options": [
             {"text": "The lungs take in oxygen, and the blood carries it to every cell", "correct": True,
              "feedback": "Yes. Neither system could keep cells alive alone: one gets oxygen in, the other delivers it."},
             {"text": "They don't: each works alone", "feedback": "They depend on each other. Blood must pass through the lungs to pick up oxygen."},
             {"text": "The heart breathes for the lungs", "feedback": "The heart pumps blood; the lungs exchange gases. Together they supply oxygen."},
             {"text": "The lungs pump the blood", "feedback": "The heart pumps blood. The lungs are where oxygen enters it."}]},
        {"type": "choice", "title": "Strong side", "instruction": "Compare the two pumps.", "showsDiagram": True,
         "question": "Why does the left ventricle need a thicker, stronger wall than the right?",
         "options": [
             {"text": "It pumps blood all around the body, not just next door to the lungs", "correct": True,
              "feedback": "Right. The systemic circuit is far longer than the trip to the lungs, so it needs much more force."},
             {"text": "It holds more oxygen", "feedback": "Wall thickness is about pumping force. The left ventricle pushes blood around the whole body."},
             {"text": "It pumps blood to the lungs", "feedback": "That's the right ventricle's job. The left pumps to the whole body."},
             {"text": "It doesn't: both are the same", "feedback": "The left ventricle's wall is much thicker, because it pumps to the whole body."}]},
    ],
}

# ---------------------------------------------------------------- The respiratory system
LUNG_R = "M 455 330 C 385 300 255 380 235 560 C 220 700 245 780 300 790 C 360 795 420 782 458 762 C 472 620 472 450 455 330 Z"
alveoli = [(820, 140), (866, 130), (842, 182), (888, 176), (800, 190)]
respiration = {
    "id": "g7-respiratory-system", "title": "The respiratory system", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-3", "minutes": 10,
    "sources": [LS1_3, ap("22.1", "22-1-organs-and-structures-of-the-respiratory-system", "Organs and Structures of the Respiratory System"),
                ap("22.3", "22-3-the-process-of-breathing", "The Process of Breathing")],
    "keywords": ["respiratory system", "lungs", "trachea", "windpipe", "bronchi", "alveoli", "diaphragm", "breathing",
                 "oxygen", "carbon dioxide", "gas exchange", "capillaries"],
    "printed": [{"text": "Air sacs, enlarged", "at": [850, 300], "size": 24}],
    "structures": [
        {"id": "trachea", "name": "trachea", "outlines": [{"line": [482, 110, 482, 380]}, {"line": [518, 110, 518, 380]}],
         "details": [{"line": [482, y, 518, y]} for y in (150, 200, 250, 300, 350)]},
        {"id": "bronchi", "name": "bronchi", "pen": "bold",
         "outlines": [{"line": [500, 380, 395, 470, 340, 560]}, {"line": [395, 470, 410, 600]},
                      {"line": [500, 380, 605, 470, 660, 560]}, {"line": [605, 470, 590, 600]}]},
        {"id": "lungs", "name": "lungs", "pen": "bold", "outlines": [{"path": LUNG_R}, {"path": mirror_path(LUNG_R, 500)}]},
        {"id": "diaphragm", "name": "diaphragm", "pen": "bold", "outlines": [{"path": "M 180 860 C 320 770 680 770 820 860"}]},
        {"id": "alveoli", "name": "alveoli", "outlines": [{"circle": [x, y, 22]} for x, y in alveoli]},
        {"id": "capillary", "name": "capillary", "pen": "fine", "outlines": [{"path": "M 760 240 C 800 210 860 230 900 214 C 930 205 950 190 960 170"}]},
    ],
    "steps": [
        {"type": "trace", "title": "Trachea", "structure": "trachea", "instruction": "Trace the trachea, the windpipe.",
         "note": {"text": "Air from your nose and mouth goes down the trachea, or windpipe."}},
        {"type": "trace", "title": "Rings", "structure": "trachea", "part": "details", "instruction": "Draw the rings across it.",
         "note": {"text": "Rings of cartilage hold the trachea open, so it never collapses."}},
        {"type": "trace", "title": "Bronchi", "structure": "bronchi", "instruction": "Trace the branching tubes into each lung.",
         "note": {"text": "The trachea splits into two bronchi, which branch again and again into tiny tubes, like an upside-down tree.",
                  "remember": "Air path: trachea, bronchi, air sacs."}},
        {"type": "trace", "title": "Lungs", "structure": "lungs", "instruction": "Trace both lungs.",
         "note": {"text": "The lungs are spongy organs filled with the branching tubes and millions of tiny air sacs."}},
        {"type": "trace", "title": "Diaphragm", "structure": "diaphragm", "instruction": "Trace the dome-shaped muscle under the lungs.",
         "note": {"text": "When the diaphragm contracts, it moves down, making more space. The lungs stretch and air rushes in.",
                  "remember": "Diaphragm down = breathe in."}},
        {"type": "trace", "title": "Air sacs", "structure": "alveoli", "instruction": "Trace the cluster of tiny air sacs, shown enlarged.",
         "note": {"text": "Each air sac, or alveolus, is only about 0.2 mm across. This is where gases are exchanged."}},
        {"type": "trace", "title": "Capillary", "structure": "capillary", "instruction": "Draw the blood capillary next to the air sacs.",
         "note": {"text": "Oxygen diffuses from the air sacs into the blood, and carbon dioxide diffuses out to be breathed away.",
                  "remember": "Air sacs: oxygen in, CO2 out."}},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [500, 230], "answer": "Trachea", "synonyms": ["Windpipe"], "role": "Carries air down to the lungs.",
              "mistakes": {"Esophagus": "The esophagus carries food. This ringed tube carries air: the trachea."}},
             {"n": 2, "at": [395, 470], "answer": "Bronchus", "synonyms": ["Bronchi"], "role": "Branch into a lung."},
             {"n": 3, "at": [300, 600], "answer": "Lung", "role": "Where gas exchange happens."},
             {"n": 4, "at": [500, 795], "answer": "Diaphragm", "role": "Muscle that powers breathing."},
             {"n": 5, "at": [842, 160], "answer": "Alveoli", "synonyms": ["Air sacs"], "role": "Tiny air sacs."}],
         "vocabulary": ["Trachea", "Windpipe", "Esophagus", "Bronchus", "Lung", "Diaphragm", "Alveoli", "Heart"]},
        {"type": "choice", "title": "Breathing in", "instruction": "Use the model.", "showsDiagram": True,
         "question": "What happens when you breathe in?",
         "options": [
             {"text": "The diaphragm contracts and moves down, so the chest gets bigger and air flows in", "correct": True,
              "feedback": "Yes. Muscles between the ribs help too, lifting the rib cage outward."},
             {"text": "The lungs suck air in on their own", "feedback": "Lungs have no muscle to do that. The diaphragm and rib muscles make the space."},
             {"text": "The diaphragm moves up", "feedback": "When it contracts it moves down, making more room for the lungs."},
             {"text": "The heart pushes air in", "feedback": "The heart pumps blood. Breathing is powered by the diaphragm."}]},
        {"type": "choice", "title": "Teamwork", "instruction": "Think about other systems.", "showsDiagram": True,
         "question": "Why do the air sacs need to be wrapped in blood capillaries?",
         "options": [
             {"text": "So oxygen can pass straight into the blood and travel to every cell", "correct": True,
              "feedback": "Right. The respiratory system brings oxygen in; the circulatory system carries it to the body."},
             {"text": "To keep the air sacs warm", "feedback": "The capillaries are there for gas exchange: oxygen into the blood, CO2 out."},
             {"text": "To pump air", "feedback": "Capillaries carry blood. They pick up oxygen from the air sacs."},
             {"text": "They don't need them", "feedback": "Without capillaries, oxygen in the lungs couldn't reach the body's cells."}]},
    ],
}

# ---------------------------------------------------------------- The digestive system
STOMACH = ("M 545 300 C 625 290 715 325 705 410 C 695 500 595 530 535 500 C 508 488 508 458 534 452 "
           "C 600 468 652 440 652 402 C 652 356 604 345 560 348 Z")
LIVER = "M 230 330 C 300 290 470 300 495 340 C 478 420 380 452 250 442 C 210 420 205 360 230 330 Z"
PANCREAS = "M 470 562 C 520 542 640 542 700 562 C 650 592 520 592 470 562 Z"
COLON = ("M 280 820 L 280 640 C 280 620 290 610 310 610 L 690 610 C 710 610 720 620 720 640 L 720 845 "
         "C 720 872 698 882 668 882 L 560 882 C 535 882 525 900 525 960")
SMALL = ("M 520 492 L 470 655 L 640 655 A 25 25 0 0 1 640 705 L 360 705 A 25 25 0 0 0 360 755 "
         "L 640 755 A 25 25 0 0 1 640 805 L 292 805")
digestion = {
    "id": "g7-digestive-system", "title": "The digestive system", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-3", "minutes": 11,
    "sources": [LS1_3, ap("23.1", "23-1-overview-of-the-digestive-system", "Overview of the Digestive System"), DIGESTION,
                ap("23.5", "23-5-the-small-and-large-intestines", "The Small and Large Intestines")],
    "keywords": ["digestive system", "esophagus", "stomach", "liver", "pancreas", "small intestine", "large intestine",
                 "rectum", "nutrients", "absorption", "digestion", "bile", "enzymes"],
    "printed": [{"text": "From the mouth", "at": [660, 70], "size": 26}],
    "structures": [
        {"id": "esophagus", "name": "esophagus", "outlines": [{"line": [500, 60, 528, 302]}, {"line": [536, 60, 560, 300]}]},
        {"id": "stomach", "name": "stomach", "pen": "bold", "outlines": [{"path": STOMACH}]},
        {"id": "liver", "name": "liver", "pen": "bold", "outlines": [{"path": LIVER}]},
        {"id": "pancreas", "name": "pancreas", "outlines": [{"path": PANCREAS}]},
        {"id": "small", "name": "small intestine", "outlines": [{"path": SMALL}]},
        {"id": "large", "name": "large intestine", "pen": "bold", "outlines": [{"path": COLON}]},
    ],
    "steps": [
        {"type": "trace", "title": "Esophagus", "structure": "esophagus", "instruction": "Trace the esophagus down from the mouth.",
         "note": {"text": "After you chew and swallow, muscles in the esophagus squeeze food down to the stomach in waves."}},
        {"type": "trace", "title": "Stomach", "structure": "stomach", "instruction": "Trace the J-shaped stomach.",
         "note": {"text": "The stomach churns food and mixes it with acid and enzymes that start breaking it down.",
                  "remember": "Stomach: churn and break down."}},
        {"type": "trace", "title": "Liver", "structure": "liver", "instruction": "Trace the liver.",
         "note": {"text": "The liver makes bile, which helps break fats into tiny droplets so they can be digested."}},
        {"type": "trace", "title": "Pancreas", "structure": "pancreas", "instruction": "Trace the pancreas below the stomach.",
         "note": {"text": "The pancreas makes digestive enzymes and sends them into the small intestine."}},
        {"type": "trace", "title": "Small intestine", "structure": "small", "instruction": "Trace the long, winding small intestine.",
         "note": {"text": "About 3 m long, the small intestine is where most digestion and almost all absorption of nutrients happen.",
                  "remember": "Small intestine: nutrients into the blood."}},
        {"type": "trace", "title": "Large intestine", "structure": "large", "instruction": "Trace the large intestine around the outside, down to the rectum.",
         "note": {"text": "The large intestine absorbs most of the leftover water, then the waste leaves through the rectum.",
                  "remember": "Large intestine: absorbs water."}},
        {"type": "order", "title": "Food's path", "instruction": "Tap the places food passes through, in order.",
         "items": ["Mouth", "Esophagus", "Stomach", "Small intestine", "Large intestine", "Rectum"],
         "why": "Food goes down the esophagus to the stomach, then the small intestine absorbs nutrients and the large intestine absorbs water.",
         "hint": "The liver and pancreas help, but food doesn't pass through them."},
        {"type": "label", "title": "Name the organs", "instruction": "Pick the name for each numbered organ.",
         "targets": [
             {"n": 1, "at": [640, 420], "answer": "Stomach", "role": "Churns food with acid."},
             {"n": 2, "at": [350, 380], "answer": "Liver", "role": "Makes bile."},
             {"n": 3, "at": [585, 566], "answer": "Pancreas", "role": "Makes digestive enzymes.",
              "mistakes": {"Stomach": "The stomach is the J-shaped bag above. This organ below it is the pancreas."}},
             {"n": 4, "at": [500, 750], "answer": "Small intestine", "role": "Absorbs nutrients.",
              "mistakes": {"Large intestine": "The large intestine frames the outside. This long winding tube is the small intestine."}},
             {"n": 5, "at": [280, 720], "answer": "Large intestine", "role": "Absorbs water."}],
         "vocabulary": ["Esophagus", "Stomach", "Liver", "Pancreas", "Small intestine", "Large intestine", "Lung"]},
        {"type": "choice", "title": "Systems working together", "instruction": "Follow the nutrients.", "showsDiagram": True,
         "question": "Nutrients are absorbed in the small intestine. How do they reach your muscles?",
         "options": [
             {"text": "They pass into the blood, and the circulatory system carries them", "correct": True,
              "feedback": "Yes. The digestive system breaks food down; the circulatory system delivers it to every cell."},
             {"text": "They travel down the large intestine", "feedback": "That carries waste out. Nutrients enter the blood in the small intestine."},
             {"text": "Muscles reach into the intestine", "feedback": "Muscles get nutrients from the blood, which picks them up in the small intestine."},
             {"text": "Through the lungs", "feedback": "The lungs handle gases. Nutrients travel in the blood."}]},
        {"type": "choice", "title": "Why so long?", "instruction": "Think about absorption.", "showsDiagram": True,
         "question": "Why is it useful that the small intestine is so long?",
         "options": [
             {"text": "It gives lots of surface for absorbing nutrients", "correct": True,
              "feedback": "Right. Its great length, plus folds inside, gives a huge surface for nutrients to pass into the blood."},
             {"text": "It stores food for weeks", "feedback": "Food passes through in hours. The length gives more surface for absorption."},
             {"text": "It absorbs water only", "feedback": "That's mostly the large intestine. The small intestine absorbs nutrients."},
             {"text": "It makes bile", "feedback": "The liver makes bile. The length gives more surface for absorbing nutrients."}]},
    ],
}

# ---------------------------------------------------------------- Muscles moving the arm: biceps and triceps
BICEPS = "M 500 196 C 600 230 625 400 552 482 L 524 486 C 538 400 528 280 500 196 Z"
TRICEPS = "M 432 190 C 340 240 330 420 402 532 L 428 528 C 400 420 410 280 432 190 Z"
BONE, MUSCLE = "#EDE6D3", "#B5483F"
arm = {
    "id": "g7-arm-muscles", "title": "Muscles moving the arm: biceps and triceps", "grade": "7", "subject": "Life science",
    "standard": "MS-LS1-3", "minutes": 9, "colorMode": "illustration",
    "sources": [LS1_3, ap("11.1", "11-1-interactions-of-skeletal-muscles-their-fascicle-arrangement-and-their-lever-systems",
                          "Interactions of Skeletal Muscles"),
                ap("10.4", "10-4-nervous-system-control-of-muscle-tension", "Nervous System Control of Muscle Tension")],
    "keywords": ["muscles", "biceps", "triceps", "bones", "tendons", "joint", "elbow", "contract", "pull", "muscle pairs",
                 "skeletal system", "muscular system"],
    "printed": [{"text": "Shoulder", "at": [465, 100], "size": 26}, {"text": "Elbow", "at": [440, 660], "size": 26},
                {"text": "Hand", "at": [900, 520], "size": 26}],
    "legend": [{"name": "Bone", "color": BONE, "meaning": "Hard, pale bone"},
               {"name": "Muscle", "color": MUSCLE, "meaning": "Red, because it's full of blood vessels"}],
    "structures": [
        {"id": "humerus", "name": "upper arm bone", "colorName": "bone", "fill": BONE, "pen": "bold", "outlines": [rrect(440, 140, 50, 430, 25)]},
        {"id": "forearm", "name": "forearm bones", "colorName": "bone", "fill": BONE, "pen": "bold",
         "outlines": [rrect(470, 515, 390, 36, 18), rrect(436, 571, 424, 36, 18)]},
        {"id": "biceps", "name": "biceps", "colorName": "muscle", "fill": MUSCLE, "outlines": [{"path": BICEPS}],
         "details": [{"line": [538, 484, 580, 515]}]},
        {"id": "triceps", "name": "triceps", "colorName": "muscle", "fill": MUSCLE, "outlines": [{"path": TRICEPS}],
         "details": [{"line": [415, 530, 440, 580]}]},
        {"id": "lift", "name": "forearm lifting", "pen": "bold", "outlines": straight_arrow(800, 500, 760, 360)},
    ],
    "steps": [
        {"type": "trace", "title": "Upper arm bone", "structure": "humerus", "instruction": "Trace the upper arm bone.",
         "note": {"text": "Bones are levers. Muscles move them by pulling."}},
        {"type": "trace", "title": "Forearm bones", "structure": "forearm", "instruction": "Trace the two forearm bones.",
         "note": {"text": "The forearm has two bones. They meet the upper arm bone at the elbow, a joint that bends."}},
        {"type": "trace", "title": "Biceps", "structure": "biceps", "instruction": "Trace the biceps on the front of the upper arm.",
         "note": {"text": "When the biceps contracts, it gets shorter and pulls the forearm up, bending the elbow.",
                  "remember": "Biceps: bends the arm."}},
        {"type": "trace", "title": "Biceps tendon", "structure": "biceps", "part": "details", "instruction": "Draw the tendon joining the biceps to the forearm.",
         "note": {"text": "Tendons are strong bands that join muscles to bones. They pass the muscle's pull to the bone."}},
        {"type": "trace", "title": "Triceps", "structure": "triceps", "instruction": "Trace the triceps on the back of the upper arm.",
         "note": {"text": "When the triceps contracts, it pulls the forearm down, straightening the elbow.",
                  "remember": "Triceps: straightens the arm."}},
        {"type": "trace", "title": "Triceps tendon", "structure": "triceps", "part": "details", "instruction": "Draw the tendon joining the triceps to the forearm.",
         "note": {"text": "It attaches just behind the elbow, so its pull straightens the arm."}},
        {"type": "trace", "title": "Lifting", "structure": "lift", "instruction": "Draw the arrow showing the forearm lifting.",
         "note": {"text": "Nerves signal the biceps to contract. Nervous, muscular and skeletal systems all work together to move."}},
        {"type": "color", "title": "Color", "structures": ["humerus", "forearm", "biceps", "triceps"], "instruction": "Color the bones and the muscles."},
        {"type": "label", "title": "Name the parts", "instruction": "Pick the name for each numbered part.",
         "targets": [
             {"n": 1, "at": [570, 350], "answer": "Biceps", "role": "Bends the elbow.",
              "mistakes": {"Triceps": "The triceps is on the back of the arm. This front muscle is the biceps."}},
             {"n": 2, "at": [375, 350], "answer": "Triceps", "role": "Straightens the elbow."},
             {"n": 3, "at": [465, 300], "answer": "Upper arm bone", "synonyms": ["Humerus"], "role": "Lever moved by muscles."},
             {"n": 4, "at": [560, 500], "answer": "Tendon", "role": "Joins muscle to bone."}],
         "vocabulary": ["Biceps", "Triceps", "Upper arm bone", "Humerus", "Tendon", "Ligament"]},
        {"type": "choice", "title": "Pairs", "instruction": "Muscles can only pull.", "showsDiagram": True,
         "question": "Muscles can pull but can't push. So how do you straighten your arm again after bending it?",
         "options": [
             {"text": "The triceps contracts and pulls the forearm back down", "correct": True,
              "feedback": "Yes. Muscles work in opposing pairs: the biceps bends the elbow, the triceps straightens it."},
             {"text": "The biceps pushes it down", "feedback": "Muscles can only pull. The triceps does the straightening."},
             {"text": "The bones straighten themselves", "feedback": "Bones can't move on their own. The triceps pulls them."},
             {"text": "The tendon pushes it", "feedback": "Tendons only pass on a muscle's pull. The triceps pulls the arm straight."}]},
        {"type": "choice", "title": "Systems", "instruction": "Think about all the systems involved.", "showsDiagram": False,
         "question": "Which body systems work together when you lift a glass of water?",
         "options": [
             {"text": "Nervous, muscular and skeletal, with blood bringing the muscles energy", "correct": True,
              "feedback": "Right. Nerves signal, muscles pull, bones move, and the circulatory system fuels the muscles."},
             {"text": "Only the muscular system", "feedback": "Muscles need nerve signals to contract and bones to pull on."},
             {"text": "Only the skeletal system", "feedback": "Bones can't move on their own. Muscles and nerves are needed too."},
             {"text": "The digestive system alone", "feedback": "Digestion supplies energy over time, but nerves, muscles and bones do the lifting."}]},
    ],
}

for lesson in (levels, circulation, respiration, digestion, arm):
    save(lesson)
