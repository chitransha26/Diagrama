"""Grade 4 · 4-LS1-1 · Structures that help plants and animals survive, grow, behave and reproduce.

Parts of a flower, the human heart, a fish, a bird and the human skeleton. Every fact is checked
against the sources each lesson lists (OpenStax text searched with curriculum/tools/openstax.py).
Parts never share an edge: ink along a shared edge would count for only one of them.
"""
from lib import mirror_path, save, straight_arrow

NGSS = {"title": "NGSS 4-LS1-1: Construct an argument that plants and animals have internal and external "
                 "structures that function to support survival, growth, behavior, and reproduction"}
ANGIOSPERMS = {"title": "OpenStax Biology 2e, 26.3 Angiosperms", "url": "https://openstax.org/books/biology-2e/pages/26-3-angiosperms"}
POLLINATION = {"title": "OpenStax Biology 2e, 32.2 Pollination and Fertilization",
               "url": "https://openstax.org/books/biology-2e/pages/32-2-pollination-and-fertilization"}
STEMS = {"title": "OpenStax Biology 2e, 30.2 Stems", "url": "https://openstax.org/books/biology-2e/pages/30-2-stems"}

# ---------------------------------------------------------------- Parts of a flower
left_petal = "M 456 704 C 350 700 210 610 196 424 C 312 428 430 540 462 680 Z"
left_sepal = "M 470 714 C 440 726 392 726 356 702 C 396 692 440 696 470 702 Z"
left_leaf = "M 496 860 C 450 820 380 815 330 835 C 380 870 450 880 496 872 Z"
flower = {
    "id": "g4-flower-parts", "title": "Parts of a flower", "grade": "4", "subject": "Life science",
    "standard": "4-LS1-1", "minutes": 9, "colorMode": "illustration",
    "sources": [NGSS, ANGIOSPERMS, POLLINATION, STEMS,
                {"title": "USDA Forest Service: Flower parts (Desert Gardeners)",
                 "url": "https://fs.usda.gov/wildflowers/kids/teacher/documents/k5_DesertGardeners_flowerParts.pdf"}],
    "keywords": ["flower", "petal", "sepal", "stamen", "anther", "filament", "pistil", "stigma", "style", "ovary",
                 "ovule", "pollen", "pollination", "seed", "fruit", "plant structures", "reproduction"],
    "legend": [
        {"name": "Stem and leaf", "color": "#4F8A3B", "meaning": "Green: they make food from sunlight"},
        {"name": "Sepals", "color": "#6FA845", "meaning": "Usually green, like small leaves"},
        {"name": "Petals", "color": "#E58FB0", "meaning": "Shown pink; petal colors vary by kind of flower"},
        {"name": "Anthers", "color": "#E7C340", "meaning": "Shown yellow, the color of much pollen"},
    ],
    "structures": [
        {"id": "stem", "name": "stem and leaf", "colorName": "stem and leaf", "fill": "#4F8A3B",
         "outlines": [{"line": [500, 955, 500, 716]}, {"path": left_leaf}, {"path": mirror_path(left_leaf, 500)}]},
        {"id": "sepals", "name": "sepals", "colorName": "sepals", "fill": "#6FA845",
         "outlines": [{"path": left_sepal}, {"path": mirror_path(left_sepal, 500)}]},
        {"id": "petals", "name": "petals", "colorName": "petals", "fill": "#E58FB0",
         "outlines": [{"path": left_petal}, {"path": mirror_path(left_petal, 500)}]},
        {"id": "stamens", "name": "stamens", "colorName": "anthers", "fill": "#E7C340",
         "outlines": [{"line": [452, 700, 370, 540]}, {"line": [548, 700, 630, 540]},
                      {"line": [474, 704, 420, 500]}, {"line": [526, 704, 580, 500]},
                      {"ellipse": [366, 520, 13, 20]}, {"ellipse": [634, 520, 13, 20]},
                      {"ellipse": [418, 480, 13, 20]}, {"ellipse": [582, 480, 13, 20]}]},
        {"id": "pistil", "name": "pistil",
         "outlines": [{"ellipse": [500, 630, 26, 40]}, {"line": [500, 590, 500, 440]}, {"ellipse": [500, 426, 28, 14]}],
         "details": [{"circle": [500, 612, 7]}, {"circle": [500, 630, 7]}, {"circle": [500, 648, 7]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Stem and leaves", "structure": "stem", "instruction": "Trace the stem and its two leaves.",
         "note": {"text": "The stem holds the flower up. Inside, tubes carry water up from the roots. The leaves make food for the plant from sunlight.",
                  "remember": "Stem = support and transport."}},
        {"type": "trace", "title": "Sepals", "structure": "sepals", "instruction": "Trace the two small green sepals under the flower.",
         "note": {"text": "Sepals look like small leaves. Before the flower opened, they wrapped around the bud to protect it.",
                  "remember": "Sepals protect the bud."}},
        {"type": "trace", "title": "Petals", "structure": "petals", "instruction": "Trace the two petals.",
         "note": {"text": "Colorful petals attract animals like bees. As they visit, they carry pollen from flower to flower.",
                  "remember": "Petals attract pollinators."}},
        {"type": "trace", "title": "Stamens", "structure": "stamens", "instruction": "Trace the four stamens: each thin stalk and its anther on top.",
         "note": {"text": "Stamens make pollen. Each is a thin stalk, the filament, holding up an anther, where the pollen grows.",
                  "remember": "Anthers make pollen."}},
        {"type": "trace", "title": "Pistil", "structure": "pistil", "instruction": "Trace the pistil in the middle: the ovary, the style and the stigma on top.",
         "note": {"text": "The pistil's sticky top, the stigma, traps pollen. The style is the stalk that leads down to the ovary.",
                  "remember": "Stigma, style, ovary: the pistil."}},
        {"type": "trace", "title": "Ovules", "structure": "pistil", "part": "details", "instruction": "Dab the three ovules inside the ovary.",
         "note": {"text": "After pollination, each ovule can become a seed, and the ovary around them grows into the fruit.",
                  "remember": "Ovules become seeds; the ovary becomes the fruit."}},
        {"type": "color", "title": "Color", "structures": ["stem", "sepals", "petals", "stamens"],
         "instruction": "Color the flower. The pistil stays white so you can see the ovules."},
        {"type": "label", "title": "Label the parts", "instruction": "Pick the right name for each numbered part.",
         "targets": [
             {"n": 1, "at": [330, 500], "answer": "Petal", "role": "Attracts pollinators with its color."},
             {"n": 2, "at": [366, 520], "answer": "Anther", "role": "Makes pollen.",
              "mistakes": {"Stigma": "The stigma is on top of the pistil in the middle. This is on a stamen: it's an anther."}},
             {"n": 3, "at": [500, 426], "answer": "Stigma", "role": "Sticky top that traps pollen.",
              "mistakes": {"Anther": "Anthers are on the stamens around the edge. The sticky top in the middle is the stigma."}},
             {"n": 4, "at": [500, 662], "answer": "Ovary", "role": "Holds the ovules; becomes the fruit."},
             {"n": 5, "at": [410, 710], "answer": "Sepal", "role": "Protected the bud."}],
         "vocabulary": ["Petal", "Sepal", "Anther", "Stigma", "Ovary", "Root", "Seed"],
         "commonMistakes": {"Root": "Roots are under the ground, holding the plant and taking in water.",
                            "Seed": "Seeds come later: the ovules inside the ovary become seeds after pollination."}},
        {"type": "choice", "title": "Explain", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "How do a flower's parts help the plant make new plants?",
         "options": [
             {"text": "Petals attract pollinators, which carry pollen to the stigma so seeds can form", "correct": True,
              "feedback": "Yes. Pollen from an anther must reach a stigma. Then ovules become seeds that grow into new plants."},
             {"text": "The stem makes the seeds", "feedback": "The stem holds the flower up and carries water. Seeds form inside the ovary."},
             {"text": "Sepals turn into fruit", "feedback": "Sepals protect the bud. It's the ovary that grows into the fruit."},
             {"text": "Petals soak up water for the seeds", "feedback": "Roots take in water. Petals help by attracting pollinators."}]},
    ],
}

# ---------------------------------------------------------------- The human heart (simple)
HEART = {"title": "OpenStax Anatomy and Physiology 2e, 19.1 Heart Anatomy",
         "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/19-1-heart-anatomy"}
SKIN = {"title": "OpenStax Anatomy and Physiology 2e, 5.1 Layers of the Skin (oxygen-poor blood is dark red)",
        "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/5-1-layers-of-the-skin"}
heart_outline = ("M 330 340 C 330 272 420 252 500 272 C 600 250 706 290 706 384 C 706 520 626 642 566 756 "
                 "C 546 790 518 792 498 770 C 398 668 314 520 330 340 Z")
heart = {
    "id": "g4-human-heart", "title": "The human heart (simple)", "grade": "4", "subject": "Life science",
    "standard": "4-LS1-1", "minutes": 9, "colorMode": "illustration",
    "sources": [NGSS, HEART, SKIN],
    "keywords": ["heart", "atrium", "ventricle", "chambers", "valve", "blood", "circulation", "lungs", "oxygen",
                 "muscle", "pump", "internal structures"],
    "printed": [{"text": "From body", "at": [250, 196]}, {"text": "To lungs", "at": [500, 160]},
                {"text": "From lungs", "at": [760, 196]}, {"text": "To body", "at": [856, 600]}],
    "legend": [
        {"name": "Heart muscle", "color": "#B5483F", "meaning": "The muscle wall that squeezes"},
        {"name": "Right side", "color": "#7A1F2B", "meaning": "Dark red: blood low in oxygen. Diagrams often show it blue, but blood is never blue."},
        {"name": "Left side", "color": "#D2342C", "meaning": "Bright red: blood full of oxygen"},
    ],
    "structures": [
        {"id": "wall", "name": "heart muscle", "colorName": "heart muscle", "fill": "#B5483F", "pen": "bold",
         "outlines": [{"path": heart_outline}]},
        {"id": "right", "name": "right atrium and ventricle", "colorName": "right side", "fill": "#7A1F2B",
         "outlines": [{"ellipse": [420, 372, 58, 52]},
                      {"path": "M 382 462 C 404 444 466 444 488 462 L 494 690 C 448 636 392 566 382 462 Z"}]},
        {"id": "left", "name": "left atrium and ventricle", "colorName": "left side", "fill": "#D2342C",
         "outlines": [{"ellipse": [590, 364, 62, 48]},
                      {"path": "M 522 462 C 562 438 646 442 656 472 C 656 560 608 648 532 712 Z"}]},
        {"id": "arrows", "name": "arrows", "pen": "bold",
         "outlines": straight_arrow(270, 222, 384, 318) + straight_arrow(505, 430, 505, 196)
                     + straight_arrow(740, 222, 632, 306) + straight_arrow(660, 560, 800, 540)},
    ],
    "steps": [
        {"type": "trace", "title": "Heart muscle", "structure": "wall", "instruction": "Trace the outside of the heart.",
         "note": {"text": "Your heart is a muscle about the size of your fist. It squeezes about once a second to pump blood all around your body.",
                  "remember": "The heart is a pump."}},
        {"type": "trace", "title": "Right side", "structure": "right", "instruction": "Trace the two chambers on the left of the picture.",
         "note": {"text": "These are the heart's right side: it faces you, so its right is on your left. Blood from the body comes in here, then is pumped to the lungs.",
                  "remember": "Right side: body to lungs."}},
        {"type": "trace", "title": "Left side", "structure": "left", "instruction": "Trace the two chambers on the right of the picture.",
         "note": {"text": "Blood full of oxygen comes back from the lungs into the left side. Its strong lower chamber pumps it out to the whole body.",
                  "remember": "Left side: lungs to body."}},
        {"type": "trace", "title": "Blood flow", "structure": "arrows", "instruction": "Draw the four arrows showing where blood comes in and goes out.",
         "note": {"text": "Valves between the chambers act like one-way doors: they stop blood flowing backward, so it always moves the same way.",
                  "remember": "Valves keep blood moving one way."}},
        {"type": "color", "title": "Color", "structures": ["wall", "right", "left"],
         "instruction": "Color the heart. Blood low in oxygen is dark red; blood full of oxygen is bright red."},
        {"type": "label", "title": "Name the chambers", "instruction": "Pick the right name for each numbered chamber.",
         "targets": [
             {"n": 1, "at": [420, 372], "answer": "Right atrium", "role": "Receives blood from the body.",
              "mistakes": {"Left atrium": "The heart faces you, so its right side is on your left. This is the right atrium."}},
             {"n": 2, "at": [440, 560], "answer": "Right ventricle", "role": "Pumps blood to the lungs."},
             {"n": 3, "at": [590, 364], "answer": "Left atrium", "role": "Receives blood from the lungs.",
              "mistakes": {"Right atrium": "The heart faces you, so its left side is on your right. This is the left atrium."}},
             {"n": 4, "at": [590, 540], "answer": "Left ventricle", "role": "Pumps blood to the body."}],
         "vocabulary": ["Right atrium", "Right ventricle", "Left atrium", "Left ventricle", "Lung"],
         "commonMistakes": {"Lung": "The lungs are beside the heart, not inside it. These are the heart's four chambers."},
         "hint": "Top chambers are atria; bottom chambers are ventricles."},
        {"type": "order", "title": "Blood's path", "items": ["Body", "Right side of the heart", "Lungs", "Left side of the heart"],
         "instruction": "Tap the places in order, starting from the body.",
         "why": "Blood from the body goes into the right side, which pumps it to the lungs for oxygen. It returns to the left side, which pumps it to the body.",
         "hint": "Where does blood get its oxygen?"},
        {"type": "choice", "title": "Explain", "instruction": "Think about what the heart does.", "showsDiagram": True,
         "question": "Why does the heart send blood to the lungs before the rest of the body?",
         "options": [
             {"text": "So the blood can pick up oxygen the body needs", "correct": True,
              "feedback": "Yes. In the lungs, blood picks up oxygen and drops off carbon dioxide. Then the left side pumps it to the body."},
             {"text": "To clean the lungs", "feedback": "Blood visits the lungs to pick up oxygen, not to clean them."},
             {"text": "To cool the blood down", "feedback": "The trip to the lungs is about oxygen: the body's cells need it to live."},
             {"text": "Because the lungs pump the blood", "feedback": "The heart does the pumping. The lungs are where oxygen gets into the blood."}]},
    ],
}

# ---------------------------------------------------------------- Fish external anatomy
FISHES = {"title": "OpenStax Biology 2e, 29.2 Fishes", "url": "https://openstax.org/books/biology-2e/pages/29-2-fishes"}
GAS = {"title": "OpenStax Biology 2e, 39.1 Systems of Gas Exchange",
       "url": "https://openstax.org/books/biology-2e/pages/39-1-systems-of-gas-exchange"}
NYDEC = {"title": "NYSDEC I FISH NY: Fish anatomy vocabulary (Lemon Fish handout)",
         "url": "https://extapps.dec.ny.gov/docs/administration_pdf/ifnygofishlp.pdf"}
fish_body = ("M 840 480 C 780 372 580 352 420 392 C 320 418 250 452 214 480 "
             "C 250 508 320 542 420 568 C 580 608 780 588 840 480 Z")
fish = {
    "id": "g4-fish-anatomy", "title": "Fish external anatomy", "grade": "4", "subject": "Zoology",
    "standard": "4-LS1-1", "minutes": 9,
    "sources": [NGSS, FISHES, GAS, NYDEC],
    "keywords": ["fish", "fins", "dorsal fin", "caudal fin", "tail", "pectoral fin", "pelvic fin", "anal fin",
                 "gills", "operculum", "lateral line", "scales", "external structures"],
    "structures": [
        {"id": "body", "name": "body", "outlines": [{"path": fish_body}],
         "details": [{"path": "M 690 470 C 580 456 420 462 240 480"}]},
        {"id": "tail", "name": "tail fin", "outlines": [{"polygon": [222, 480, 104, 380, 140, 480, 104, 580]}]},
        {"id": "fins", "name": "fins",
         "outlines": [{"path": "M 440 386 C 470 312 580 290 650 372 Z"},
                      {"path": "M 660 506 C 620 530 580 556 556 572 C 606 566 646 544 672 516 Z"},
                      {"path": "M 528 590 C 510 624 482 642 460 648 C 488 622 504 604 508 586 Z"},
                      {"path": "M 336 556 C 318 596 290 614 266 620 C 288 590 302 568 306 548 Z"}]},
        {"id": "gills", "name": "gill cover", "outlines": [{"path": "M 706 404 C 662 446 662 520 706 562"}]},
        {"id": "head", "name": "eye, nostril and mouth",
         "outlines": [{"circle": [770, 452, 11]}, {"circle": [806, 444, 5]}, {"line": [840, 480, 806, 494]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Body", "structure": "body", "instruction": "Trace the fish's body.",
         "note": {"text": "A fish's smooth, pointed shape slips through water easily. Scales cover it like armor, and slime on top helps keep out germs.",
                  "remember": "Streamlined body, protective scales."}},
        {"type": "trace", "title": "Tail fin", "structure": "tail", "instruction": "Trace the tail fin.",
         "note": {"text": "The tail fin, or caudal fin, sweeps from side to side and pushes the fish forward.",
                  "remember": "Tail fin = forward."}},
        {"type": "trace", "title": "Fins", "structure": "fins", "instruction": "Trace the four other fins: one on the back, one on the side, two underneath.",
         "note": {"text": "The back (dorsal) fin keeps the fish upright. The side (pectoral) and belly (pelvic and anal) fins help it balance and steer.",
                  "remember": "Fins balance and steer."}},
        {"type": "trace", "title": "Gill cover", "structure": "gills", "instruction": "Trace the curved edge of the gill cover.",
         "note": {"text": "Under this bony flap, the operculum, are the gills. As water flows over them, they take in oxygen from the water.",
                  "remember": "Gills get oxygen from water."}},
        {"type": "trace", "title": "Lateral line", "structure": "body", "part": "details", "instruction": "Draw the lateral line along the side.",
         "note": {"text": "The lateral line is a row of tiny pores along each side. It lets the fish feel movement and vibration in the water around it.",
                  "remember": "Lateral line = feeling the water."}},
        {"type": "trace", "title": "Head", "structure": "head", "instruction": "Dab the eye and nostril, then draw the mouth.",
         "note": {"text": "Fish smell with their nostrils, called nares, which help them find food. They don't use them to breathe.",
                  "remember": "Nares smell; gills breathe."}},
        {"type": "label", "title": "Label the parts", "instruction": "Pick the right name for each numbered part.",
         "targets": [
             {"n": 1, "at": [140, 480], "answer": "Tail fin", "synonyms": ["Caudal fin"], "role": "Pushes the fish forward."},
             {"n": 2, "at": [550, 350], "answer": "Dorsal fin", "role": "Keeps the fish upright."},
             {"n": 3, "at": [706, 483], "answer": "Gill cover", "synonyms": ["Operculum"], "role": "Protects the gills.",
              "mistakes": {"Gills": "The gills are hidden underneath. This bony flap is the gill cover."}},
             {"n": 4, "at": [460, 466], "answer": "Lateral line", "role": "Senses movement in the water."},
             {"n": 5, "at": [612, 548], "answer": "Pectoral fin", "role": "Helps balance and steer."}],
         "vocabulary": ["Tail fin", "Dorsal fin", "Gill cover", "Gills", "Lateral line", "Pectoral fin", "Lung"],
         "commonMistakes": {"Lung": "Most fish have no lungs. They get oxygen with gills."}},
        {"type": "choice", "title": "Explain", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "A fish lives where the water is murky and dark. Which part best helps it notice a predator coming?",
         "options": [
             {"text": "The lateral line", "correct": True,
              "feedback": "Yes. Even when it can't see, it can feel the water move as a predator swims close, and dart away."},
             {"text": "The tail fin", "feedback": "The tail fin helps it escape fast, but noticing the predator is the lateral line's job."},
             {"text": "The gill cover", "feedback": "The gill cover protects the gills. It doesn't sense anything."},
             {"text": "The scales", "feedback": "Scales protect the body. The lateral line senses movement in the water."}]},
    ],
}

# ---------------------------------------------------------------- Bird external anatomy (male northern cardinal)
BIRDS = {"title": "OpenStax Biology 2e, 29.5 Birds", "url": "https://openstax.org/books/biology-2e/pages/29-5-birds"}
CARDINAL = {"title": "Cornell Lab of Ornithology, All About Birds: Northern Cardinal identification",
            "url": "https://www.allaboutbirds.org/guide/Northern_Cardinal/id"}
FINCHES = {"title": "OpenStax Biology 2e, 18.1 Understanding Evolution (beak shape and food)",
           "url": "https://openstax.org/books/biology-2e/pages/18-1-understanding-evolution"}
bird_body = ("M 702 362 C 694 322 652 304 622 324 L 588 282 L 588 338 C 520 356 444 378 384 410 "
             "C 312 446 268 466 236 482 C 290 512 386 550 476 560 C 586 568 664 520 692 452 C 702 424 706 396 702 362 Z")
bird = {
    "id": "g4-bird-anatomy", "title": "Bird external anatomy", "grade": "4", "subject": "Zoology",
    "standard": "4-LS1-1", "minutes": 9, "colorMode": "illustration",
    "sources": [NGSS, BIRDS, FINCHES, CARDINAL],
    "keywords": ["bird", "cardinal", "beak", "bill", "feathers", "wing", "tail", "crest", "feet", "hollow bones",
                 "flight", "external structures"],
    "legend": [
        {"name": "Feathers", "color": "#C8202E", "meaning": "A male northern cardinal is brilliant red all over"},
        {"name": "Not shown", "color": None, "meaning": "His reddish bill and the black mask around it"},
    ],
    "structures": [
        {"id": "body", "name": "head and body", "colorName": "body feathers", "fill": "#C8202E", "pen": "bold",
         "outlines": [{"path": bird_body}]},
        {"id": "beak", "name": "beak", "pen": "bold", "outlines": [{"line": [704, 366, 766, 392, 704, 414]}]},
        {"id": "wing", "name": "wing", "colorName": "wing", "fill": "#B01B28",
         "outlines": [{"path": "M 606 424 C 540 404 430 424 342 472 C 440 498 540 494 606 458 Z"}],
         "details": [{"line": [580, 436, 430, 452]}, {"line": [570, 468, 420, 482]}]},
        {"id": "tail", "name": "tail", "colorName": "tail", "fill": "#B01B28",
         "outlines": [{"polygon": [262, 470, 96, 436, 100, 508, 262, 500]}]},
        {"id": "eye", "name": "eye", "outlines": [{"circle": [664, 366, 10]}]},
        {"id": "legs", "name": "legs and feet",
         "outlines": [{"line": [482, 560, 472, 652]}, {"line": [532, 556, 542, 652]},
                      {"line": [440, 668, 472, 652, 500, 670]}, {"line": [512, 668, 542, 652, 572, 666]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Head and body", "structure": "body", "instruction": "Trace the cardinal's head and body, with its pointed crest.",
         "note": {"text": "Feathers cover a bird's body. Soft down feathers underneath trap heat, keeping the bird warm even in winter.",
                  "remember": "Feathers keep birds warm."}},
        {"type": "trace", "title": "Beak", "structure": "beak", "instruction": "Draw the short, thick beak.",
         "note": {"text": "Birds have no teeth. A cardinal's short, very thick beak is strong enough to crack open seeds.",
                  "remember": "Beak shape matches food."}},
        {"type": "trace", "title": "Wing", "structure": "wing", "instruction": "Trace the wing folded against the body.",
         "note": {"text": "Wings lift a bird into the air. Many birds also have hollow bones, which make them lighter for flying.",
                  "remember": "Wings plus light bones = flight."}},
        {"type": "trace", "title": "Wing feathers", "structure": "wing", "part": "details", "instruction": "Draw two long flight feathers on the wing.",
         "note": {"text": "Long, stiff flight feathers on the wing push against the air, giving the bird lift and thrust."}},
        {"type": "trace", "title": "Tail", "structure": "tail", "instruction": "Trace the long tail.",
         "note": {"text": "The tail helps a bird steer and slow down, a bit like a rudder and brakes together."}},
        {"type": "trace", "title": "Eye", "structure": "eye", "instruction": "Dab the eye.",
         "note": {"text": "Birds rely on sharp eyesight to find food and spot danger."}},
        {"type": "trace", "title": "Legs and feet", "structure": "legs", "instruction": "Draw both legs and their toes.",
         "note": {"text": "Toes that grip let a cardinal perch on thin branches, even while it sleeps.",
                  "remember": "Feet for perching."}},
        {"type": "color", "title": "Color", "structures": ["body", "wing", "tail"],
         "instruction": "Color the male cardinal's red feathers."},
        {"type": "label", "title": "Label the parts", "instruction": "Pick the right name for each numbered part.",
         "targets": [
             {"n": 1, "at": [740, 390], "answer": "Beak", "synonyms": ["Bill"], "role": "Cracks open seeds."},
             {"n": 2, "at": [600, 300], "answer": "Crest", "role": "The pointed feathers on its head."},
             {"n": 3, "at": [480, 448], "answer": "Wing", "role": "For flying."},
             {"n": 4, "at": [170, 472], "answer": "Tail", "role": "For steering and slowing down."},
             {"n": 5, "at": [500, 666], "answer": "Feet", "role": "For gripping branches."}],
         "vocabulary": ["Beak", "Crest", "Wing", "Tail", "Feet", "Fin", "Teeth"],
         "commonMistakes": {"Fin": "Fins belong to fish. Birds have wings and a tail.", "Teeth": "Birds have no teeth: they use their beaks."}},
        {"type": "choice", "title": "Explain", "instruction": "Think about the beak.", "showsDiagram": True,
         "question": "Why does a cardinal have a short, very thick beak?",
         "options": [
             {"text": "To crack open hard seeds", "correct": True,
              "feedback": "Yes. Cardinals split sunflower seeds with their beaks, then use their tongues to take the seed out of the shell."},
             {"text": "To catch fish", "feedback": "Fish-catching birds often have long, sharp beaks. A thick beak is built for cracking seeds."},
             {"text": "To sip nectar from flowers", "feedback": "Nectar-sippers like hummingbirds have long, thin beaks."},
             {"text": "To help it fly", "feedback": "Wings and feathers help it fly. The beak is for eating."}]},
    ],
}

# ---------------------------------------------------------------- The human skeleton: major bones
SKELETAL = {"title": "OpenStax Anatomy and Physiology 2e, 6.1 The Functions of the Skeletal System",
            "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/6-1-the-functions-of-the-skeletal-system"}
BONECLASS = {"title": "OpenStax Anatomy and Physiology 2e, 6.2 Bone Classification (206 bones)",
             "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/6-2-bone-classification"}
THORAX = {"title": "OpenStax Anatomy and Physiology 2e, 7.4 The Thoracic Cage",
          "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/7-4-the-thoracic-cage"}
CAVITIES = {"title": "OpenStax Anatomy and Physiology 2e, 1.6 Anatomical Terminology (skull and spine protect the brain and spinal cord)",
            "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology"}
LEG = {"title": "OpenStax Anatomy and Physiology 2e, 8.4 Bones of the Lower Limb",
       "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/8-4-bones-of-the-lower-limb"}
HIP = {"title": "OpenStax Anatomy and Physiology 2e, 11.6 Appendicular Muscles of the Pelvic Girdle and Lower Limbs",
       "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs"}


def rib(i):
    y = 262 + 40 * i
    return f"M 490 {y} C 432 {y - 6} 398 {y + 30} 404 {y + 68}"


ribs = [{"path": rib(i)} for i in range(4)]
ribs += [{"path": mirror_path(rib(i), 500)} for i in range(4)]
pelvis = "M 432 566 C 432 616 466 640 500 640 C 534 640 568 616 568 566 C 540 590 460 590 432 566 Z"
skeleton = {
    "id": "g4-human-skeleton", "title": "The human skeleton: major bones", "grade": "4", "subject": "Life science",
    "standard": "4-LS1-1", "minutes": 9,
    "sources": [NGSS, SKELETAL, BONECLASS, THORAX, CAVITIES, LEG, HIP],
    "keywords": ["skeleton", "bones", "skull", "spine", "backbone", "vertebrae", "ribs", "rib cage", "pelvis",
                 "hip", "femur", "thigh bone", "kneecap", "support", "protection", "internal structures"],
    "structures": [
        {"id": "skull", "name": "skull", "pen": "bold", "outlines": [{"ellipse": [500, 136, 54, 64]}]},
        {"id": "spine", "name": "spine", "pen": "bold", "outlines": [{"line": [500, 214, 500, 556]}]},
        {"id": "ribs", "name": "ribs", "outlines": ribs},
        {"id": "arms", "name": "collarbones and arm bones",
         "outlines": [{"line": [494, 226, 386, 240]}, {"line": [506, 226, 614, 240]},
                      {"line": [376, 254, 350, 420]}, {"line": [346, 442, 326, 592]},
                      {"line": [624, 254, 650, 420]}, {"line": [654, 442, 674, 592]}]},
        {"id": "pelvis", "name": "pelvis", "pen": "bold", "outlines": [{"path": pelvis}]},
        {"id": "legs", "name": "leg bones", "pen": "bold",
         "outlines": [{"line": [466, 652, 452, 804]}, {"line": [534, 652, 548, 804]},
                      {"line": [452, 836, 448, 968]}, {"line": [548, 836, 552, 968]}],
         "details": [{"circle": [452, 820, 9]}, {"circle": [548, 820, 9]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Skull", "structure": "skull", "instruction": "Trace the skull.",
         "note": {"text": "Your skull is a hard case of bone that protects your brain.",
                  "remember": "Skull protects the brain."}},
        {"type": "trace", "title": "Spine", "structure": "spine", "instruction": "Trace the spine down the middle.",
         "note": {"text": "Your spine, or backbone, is a stack of small bones. It holds your body up and protects the spinal cord inside it.",
                  "remember": "Spine: support and protection."}},
        {"type": "trace", "title": "Ribs", "structure": "ribs", "instruction": "Trace the four ribs on each side.",
         "note": {"text": "Your ribs form a cage around your chest. It protects your heart and lungs. Most people have 12 pairs; we've drawn 4.",
                  "remember": "Rib cage protects heart and lungs."}},
        {"type": "trace", "title": "Arm bones", "structure": "arms", "instruction": "Draw the two collarbones, then the upper and lower bones of each arm.",
         "note": {"text": "Your arms hang from your collarbones at the shoulders. Muscles pull on the arm bones to move them, so you can lift, throw and write."}},
        {"type": "trace", "title": "Pelvis", "structure": "pelvis", "instruction": "Trace the pelvis, or hip bones.",
         "note": {"text": "The pelvis connects your legs to your body. It's built to be steady, so it can support your weight when you stand and walk."}},
        {"type": "trace", "title": "Leg bones", "structure": "legs", "instruction": "Draw both legs: the thigh bones, then the shin bones.",
         "note": {"text": "The thigh bone, or femur, is the longest and strongest bone in your body. It's about a quarter of your height.",
                  "remember": "Femur: longest bone."}},
        {"type": "trace", "title": "Kneecaps", "structure": "legs", "part": "details", "instruction": "Dab both kneecaps.",
         "note": {"text": "Each kneecap sits in front of the knee joint, where the thigh bone meets the shin bone."}},
        {"type": "label", "title": "Label the bones", "instruction": "Pick the right name for each numbered bone.",
         "targets": [
             {"n": 1, "at": [500, 136], "answer": "Skull", "role": "Protects the brain."},
             {"n": 2, "at": [420, 320], "answer": "Ribs", "role": "Protect the heart and lungs."},
             {"n": 3, "at": [500, 470], "answer": "Spine", "synonyms": ["Backbone"], "role": "Supports the body; protects the spinal cord."},
             {"n": 4, "at": [500, 600], "answer": "Pelvis", "synonyms": ["Hip bones"], "role": "Connects the legs to the body."},
             {"n": 5, "at": [459, 728], "answer": "Femur", "synonyms": ["Thigh bone"], "role": "The longest, strongest bone.",
              "mistakes": {"Shin bone": "The shin bone is below the knee. Above it is the femur, the thigh bone."}}],
         "vocabulary": ["Skull", "Ribs", "Spine", "Pelvis", "Femur", "Shin bone", "Heart"],
         "commonMistakes": {"Heart": "The heart isn't a bone: it's a muscle, protected by the ribs."}},
        {"type": "choice", "title": "Explain", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "Which bones protect the organs you need to breathe?",
         "options": [
             {"text": "The ribs", "correct": True, "feedback": "Yes. The rib cage surrounds the lungs, and the heart beside them."},
             {"text": "The skull", "feedback": "The skull protects the brain. The ribs protect the lungs."},
             {"text": "The femur", "feedback": "The femur is the thigh bone: it holds you up. The ribs protect the lungs."},
             {"text": "The pelvis", "feedback": "The pelvis connects your legs. The rib cage protects your lungs."}]},
        {"type": "choice", "title": "Fun fact", "instruction": "One more about bones.", "showsDiagram": False,
         "question": "A baby is born with about 300 bones, but an adult has 206. What happens to the rest?",
         "options": [
             {"text": "Some of them fuse, growing together into one bone", "correct": True,
              "feedback": "Right. As babies grow, some bones join together. That's how 270 to 300 bones become 206."},
             {"text": "They fall out like baby teeth", "feedback": "Bones don't fall out. Some of them grow together, or fuse."},
             {"text": "They turn into muscles", "feedback": "Bones stay bone. Some of them join together as you grow."},
             {"text": "Babies don't really have more bones", "feedback": "They do: about 270 to 300. Some fuse together over time."}]},
    ],
}

for lesson in (flower, heart, fish, bird, skeleton):
    save(lesson)
