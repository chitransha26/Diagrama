"""Grade 4 · lungs, digestion and the earthworm (4-LS1-1), and the eye and ear (4-LS1-2).

Facts checked against the sources each lesson lists (OpenStax text searched with
curriculum/tools/openstax.py; the Science Learning Hub for earthworm bristles).
"""
from lib import mirror_path, save, straight_arrow

NGSS1 = {"title": "NGSS 4-LS1-1: Construct an argument that plants and animals have internal and external "
                  "structures that function to support survival, growth, behavior, and reproduction"}
NGSS2 = {"title": "NGSS 4-LS1-2: Use a model to describe that animals receive different types of information through "
                  "their senses, process the information in their brain, and respond to the information in different ways"}


def ap(section, slug, title):
    return {"title": f"OpenStax Anatomy and Physiology 2e, {section} {title}",
            "url": f"https://openstax.org/books/anatomy-and-physiology-2e/pages/{slug}"}


def bio(section, slug, title):
    return {"title": f"OpenStax Biology 2e, {section} {title}", "url": f"https://openstax.org/books/biology-2e/pages/{slug}"}


BRAIN = ("M 712 404 C 700 326 780 286 850 304 C 930 292 982 360 962 430 C 982 500 902 544 842 524 "
         "C 782 546 708 506 712 404 Z")

# ---------------------------------------------------------------- The human lungs
right_lung = "M 466 384 C 426 364 330 382 290 470 C 250 560 252 676 272 728 C 342 718 420 700 462 690 C 482 600 480 470 466 384 Z"
left_lung = ("M 534 384 C 574 364 670 382 710 470 C 750 560 748 676 728 728 C 660 718 604 706 566 698 "
             "C 596 642 604 602 566 566 C 548 528 538 474 534 384 Z")
lungs = {
    "id": "g4-human-lungs", "title": "The human lungs", "grade": "4", "subject": "Life science",
    "standard": "4-LS1-1", "minutes": 9,
    "sources": [NGSS1, ap("22.1", "22-1-organs-and-structures-of-the-respiratory-system", "Organs and Structures of the Respiratory System"),
                ap("22.2", "22-2-the-lungs", "The Lungs"), ap("22.3", "22-3-the-process-of-breathing", "The Process of Breathing"),
                ap("20.2", "20-2-blood-flow-blood-pressure-and-resistance", "Blood Flow, Blood Pressure, and Resistance (the diaphragm moves down)"),
                ap("20.5", "20-5-circulatory-pathways", "Circulatory Pathways (gas exchange in the alveoli)")],
    "keywords": ["lungs", "breathing", "trachea", "windpipe", "bronchi", "alveoli", "diaphragm", "oxygen",
                 "carbon dioxide", "respiratory system", "lobes", "internal structures"],
    "structures": [
        {"id": "trachea", "name": "windpipe", "outlines": [{"rect": [482, 112, 36, 230, 18]}]},
        {"id": "bronchi", "name": "bronchi", "outlines": [{"line": [490, 350, 396, 430, 382, 566]}, {"line": [510, 350, 604, 430, 618, 566]}]},
        {"id": "rightLung", "name": "right lung", "outlines": [{"path": right_lung}],
         "details": [{"path": "M 292 516 C 362 516 420 534 462 552"}, {"path": "M 272 640 C 340 604 418 594 462 602"}]},
        {"id": "leftLung", "name": "left lung", "outlines": [{"path": left_lung}],
         "details": [{"path": "M 728 610 C 680 580 640 572 600 574"}]},
        {"id": "alveoli", "name": "air sacs",
         "outlines": [{"circle": [356, 598, 11]}, {"circle": [380, 590, 11]}, {"circle": [368, 618, 11]},
                      {"circle": [392, 612, 11]}, {"circle": [346, 622, 11]}]},
        {"id": "diaphragm", "name": "diaphragm", "pen": "bold", "outlines": [{"path": "M 226 768 C 330 690 670 690 774 768"}]},
    ],
    "steps": [
        {"type": "trace", "title": "Windpipe", "structure": "trachea", "instruction": "Trace the windpipe.",
         "note": {"text": "Air you breathe in through your nose or mouth goes down the windpipe, or trachea. Stiff rings keep it open.",
                  "remember": "Trachea = windpipe."}},
        {"type": "trace", "title": "Bronchi", "structure": "bronchi", "instruction": "Draw the two tubes branching to each lung.",
         "note": {"text": "The windpipe splits into two bronchi, one for each lung. Inside, they branch again and again into tiny tubes."}},
        {"type": "trace", "title": "Right lung", "structure": "rightLung", "instruction": "Trace the lung on the left of the picture.",
         "note": {"text": "This is your right lung: the body faces you, so its right is on your left. It's the bigger lung.",
                  "remember": "Two lungs, one on each side of the heart."}},
        {"type": "trace", "title": "Left lung", "structure": "leftLung", "instruction": "Trace the other lung, with its dip in the middle.",
         "note": {"text": "The left lung is smaller. It has a dip, the cardiac notch, that makes room for your heart.",
                  "remember": "The left lung makes room for the heart."}},
        {"type": "trace", "title": "Lobes", "structure": "rightLung", "part": "details", "instruction": "Draw the two lines that split the right lung into lobes.",
         "note": {"text": "The right lung has three lobes, or sections. The left lung has two."}},
        {"type": "trace", "title": "Lobe", "structure": "leftLung", "part": "details", "instruction": "Draw the line that splits the left lung into two lobes.",
         "note": {"text": "The lobes are separated by deep grooves called fissures."}},
        {"type": "trace", "title": "Air sacs", "structure": "alveoli", "instruction": "Dab the tiny air sacs at the end of the airway.",
         "note": {"text": "The tiniest tubes end in air sacs called alveoli. Here oxygen passes into your blood, and carbon dioxide passes out to be breathed away.",
                  "remember": "Alveoli: where oxygen enters the blood."}},
        {"type": "trace", "title": "Diaphragm", "structure": "diaphragm", "instruction": "Trace the dome-shaped muscle under the lungs.",
         "note": {"text": "The diaphragm is a muscle. When it squeezes, it moves down, making room in your chest, and air rushes into your lungs.",
                  "remember": "Diaphragm down = breathe in."}},
        {"type": "order", "title": "Air's path", "items": ["Nose or mouth", "Windpipe", "Bronchi", "Air sacs"],
         "instruction": "Tap the parts in the order air reaches them.",
         "why": "Air goes in through the nose or mouth, down the windpipe, into the bronchi, and on to the tiny air sacs.",
         "hint": "Which tube does air go down first?"},
        {"type": "label", "title": "Label the parts", "instruction": "Pick the right name for each numbered part.",
         "targets": [
             {"n": 1, "at": [500, 226], "answer": "Windpipe", "synonyms": ["Trachea"], "role": "Carries air down to the lungs."},
             {"n": 2, "at": [396, 430], "answer": "Bronchus", "role": "Carries air into one lung."},
             {"n": 3, "at": [370, 606], "answer": "Air sacs", "synonyms": ["Alveoli"], "role": "Where oxygen enters the blood."},
             {"n": 4, "at": [500, 708], "answer": "Diaphragm", "role": "Muscle that moves to pull air in.",
              "mistakes": {"Stomach": "The stomach is below the diaphragm. This dome-shaped muscle is the diaphragm."}}],
         "vocabulary": ["Windpipe", "Bronchus", "Air sacs", "Diaphragm", "Stomach", "Heart"],
         "commonMistakes": {"Heart": "The heart sits between the lungs, in the dip of the left lung. It isn't drawn here."}},
        {"type": "choice", "title": "Explain", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "Why do your lungs need so many tiny air sacs?",
         "options": [
             {"text": "So lots of oxygen can pass into the blood at once", "correct": True,
              "feedback": "Yes. Every air sac is a place where oxygen moves into the blood and carbon dioxide moves out, so more sacs means more oxygen."},
             {"text": "To store food", "feedback": "Lungs don't store food. The air sacs are where oxygen gets into the blood."},
             {"text": "To make the lungs heavier", "feedback": "The air sacs are about passing oxygen into the blood, not weight."},
             {"text": "To pump blood", "feedback": "The heart pumps blood. The air sacs are where oxygen enters it."}]},
    ],
}

# ---------------------------------------------------------------- The digestive system (simple)
stomach = ("M 506 366 C 562 346 644 376 644 448 C 644 520 584 560 524 546 C 498 540 494 508 520 498 "
           "C 562 488 584 470 574 438 C 564 408 524 398 506 398 Z")
digestion = {
    "id": "g4-digestive-system", "title": "The digestive system (simple)", "grade": "4", "subject": "Life science",
    "standard": "4-LS1-1", "minutes": 8,
    "sources": [NGSS1, ap("23.1", "23-1-overview-of-the-digestive-system", "Overview of the Digestive System"),
                ap("23.2", "23-2-digestive-system-processes-and-regulation", "Digestive System Processes and Regulation"),
                ap("23.3", "23-3-the-mouth-pharynx-and-esophagus", "The Mouth, Pharynx, and Esophagus"),
                ap("17.10", "17-10-organs-with-secondary-endocrine-functions", "Organs with Secondary Endocrine Functions (stomach acid)")],
    "keywords": ["digestion", "digestive system", "mouth", "teeth", "saliva", "esophagus", "stomach", "small intestine",
                 "large intestine", "nutrients", "absorption", "internal structures"],
    "structures": [
        {"id": "mouth", "name": "mouth", "outlines": [{"ellipse": [500, 104, 44, 22]}]},
        {"id": "esophagus", "name": "esophagus", "outlines": [{"line": [500, 132, 500, 362]}]},
        {"id": "stomach", "name": "stomach", "outlines": [{"path": stomach}]},
        {"id": "small", "name": "small intestine",
         "outlines": [{"path": "M 520 556 C 470 600 380 594 400 640 C 420 690 600 662 600 712 C 600 762 400 742 410 792 "
                               "C 416 822 380 836 356 846"}]},
        {"id": "large", "name": "large intestine", "pen": "bold",
         "outlines": [{"path": "M 340 860 C 326 846 324 826 324 800 L 324 612 C 324 594 338 584 360 584 L 640 584 "
                               "C 662 584 676 594 676 612 L 676 830 C 676 858 646 870 614 874 C 602 884 600 904 600 934"}]},
    ],
    "steps": [
        {"type": "trace", "title": "Mouth", "structure": "mouth", "instruction": "Trace the mouth.",
         "note": {"text": "Digestion starts here. Teeth break food into small pieces, and saliva wets it and starts breaking it down.",
                  "remember": "Chewing makes food smaller."}},
        {"type": "trace", "title": "Esophagus", "structure": "esophagus", "instruction": "Trace the tube down from the mouth.",
         "note": {"text": "The esophagus is a muscular tube. When you swallow, its muscles squeeze food down to your stomach.",
                  "remember": "Esophagus: mouth to stomach."}},
        {"type": "trace", "title": "Stomach", "structure": "stomach", "instruction": "Trace the J-shaped stomach.",
         "note": {"text": "The stomach's strong muscles churn food, and it makes acid that helps break the food down into a thick liquid.",
                  "remember": "Stomach: churn and acid."}},
        {"type": "trace", "title": "Small intestine", "structure": "small", "instruction": "Trace the long, winding small intestine.",
         "note": {"text": "Most of the food's nutrients pass from the small intestine into your blood, which carries them all over your body.",
                  "remember": "Small intestine absorbs nutrients."}},
        {"type": "trace", "title": "Large intestine", "structure": "large", "instruction": "Trace the large intestine around the outside.",
         "note": {"text": "The large intestine soaks up most of the water that's left, then moves the leftover waste out of the body.",
                  "remember": "Large intestine absorbs water."}},
        {"type": "order", "title": "Food's path", "items": ["Mouth", "Esophagus", "Stomach", "Small intestine", "Large intestine"],
         "instruction": "Tap the parts in the order food passes through them.",
         "why": "Food is chewed in the mouth, swallowed down the esophagus, churned in the stomach, absorbed in the small intestine, and dried out in the large intestine.",
         "hint": "Where does swallowed food go first?"},
        {"type": "label", "title": "Label the parts", "instruction": "Pick the right name for each numbered part.",
         "targets": [
             {"n": 1, "at": [500, 250], "answer": "Esophagus", "role": "Squeezes food down to the stomach."},
             {"n": 2, "at": [610, 450], "answer": "Stomach", "role": "Churns food with acid."},
             {"n": 3, "at": [500, 700], "answer": "Small intestine", "role": "Absorbs nutrients.",
              "mistakes": {"Large intestine": "The large intestine goes around the outside. This winding tube in the middle is the small intestine."}},
             {"n": 4, "at": [330, 720], "answer": "Large intestine", "role": "Absorbs water."}],
         "vocabulary": ["Esophagus", "Stomach", "Small intestine", "Large intestine", "Windpipe", "Lung"],
         "commonMistakes": {"Windpipe": "The windpipe carries air to the lungs. Food goes down the esophagus."}},
        {"type": "choice", "title": "Explain", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "How do the nutrients in your lunch get to the muscles in your legs?",
         "options": [
             {"text": "They pass from the small intestine into the blood, which carries them there", "correct": True,
              "feedback": "Yes. Digestion breaks food down small enough to pass into the blood, and the heart pumps it around the body."},
             {"text": "The stomach squeezes them down to the legs", "feedback": "The stomach churns food. Nutrients reach the legs through the blood."},
             {"text": "They travel through the large intestine to the legs", "feedback": "The large intestine absorbs water. Most nutrients enter the blood from the small intestine."},
             {"text": "They stay in the stomach", "feedback": "Food moves on from the stomach. Its nutrients enter the blood in the small intestine."}]},
    ],
}

# ---------------------------------------------------------------- Earthworm external anatomy
ANNELIDS = bio("28.4", "28-4-superphylum-lophotrochozoa-mollusks-and-annelids", "Superphylum Lophotrochozoa: Mollusks and Annelids")
GAS = bio("39.1", "39-1-systems-of-gas-exchange", "Systems of Gas Exchange")
SLH = {"title": "Science Learning Hub (University of Waikato): Physical adaptations for life underground",
       "url": "https://www.sciencelearn.org.nz/videos/3-physical-adaptations-for-life-underground"}
worm_body = ("M 150 500 C 150 458 204 452 244 454 L 780 454 C 834 456 866 480 866 500 C 866 520 834 544 780 546 "
             "L 244 546 C 204 548 150 542 150 500 Z")
segments = [{"line": [x, 466, x, 534]} for x in list(range(220, 300, 28)) + list(range(408, 830, 28))]
worm = {
    "id": "g4-earthworm", "title": "Earthworm external anatomy", "grade": "4", "subject": "Zoology",
    "standard": "4-LS1-1", "minutes": 7,
    "sources": [NGSS1, ANNELIDS, GAS, SLH],
    "keywords": ["earthworm", "worm", "segments", "setae", "bristles", "clitellum", "annelid", "skin breathing",
                 "soil", "burrowing", "external structures"],
    "structures": [
        {"id": "body", "name": "body", "outlines": [{"path": worm_body}]},
        {"id": "segments", "name": "segments", "outlines": segments},
        {"id": "clitellum", "name": "clitellum", "pen": "bold", "outlines": [{"rect": [304, 440, 84, 120, 16]}]},
        {"id": "mouth", "name": "mouth", "outlines": [{"circle": [164, 500, 8]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Body", "structure": "body", "instruction": "Trace the earthworm's long body.",
         "note": {"text": "A long, thin, slippery body lets an earthworm push through soil, digging tunnels as it goes.",
                  "remember": "Shaped for burrowing."}},
        {"type": "trace", "title": "Segments", "structure": "segments", "instruction": "Draw the rings that divide the body into segments.",
         "note": {"text": "The body is made of many ring-shaped segments. Each has tiny bristles, called setae, that grip the soil as the worm moves.",
                  "remember": "Segments with gripping bristles."}},
        {"type": "trace", "title": "Clitellum", "structure": "clitellum", "instruction": "Trace the wide band near the front end.",
         "note": {"text": "This thick band is the clitellum. It makes a cocoon where the worm's eggs are kept, so it helps earthworms reproduce.",
                  "remember": "Clitellum: makes the egg cocoon."}},
        {"type": "trace", "title": "Mouth", "structure": "mouth", "instruction": "Dab the mouth at the front end.",
         "note": {"text": "Earthworms eat soil as they burrow, digesting the tiny bits of dead plants and living things in it."}},
        {"type": "label", "title": "Label the parts", "instruction": "Pick the right name for each numbered part.",
         "targets": [
             {"n": 1, "at": [345, 500], "answer": "Clitellum", "role": "Makes the egg cocoon."},
             {"n": 2, "at": [164, 500], "answer": "Mouth", "role": "Takes in soil and food."},
             {"n": 3, "at": [600, 500], "answer": "Segment", "role": "One of many rings, each with gripping bristles."}],
         "vocabulary": ["Clitellum", "Mouth", "Segment", "Tail"],
         "commonMistakes": {"Tail": "The tail end is at the far right. This part is near the front."}},
        {"type": "choice", "title": "Explain", "instruction": "Think about how an earthworm breathes.", "showsDiagram": True,
         "question": "Earthworms have no lungs. Why do they need to stay damp?",
         "options": [
             {"text": "They breathe through their skin, which only works when it's moist", "correct": True,
              "feedback": "Yes. Oxygen passes in through their moist skin. If an earthworm dries out, it can't breathe."},
             {"text": "So they can swim", "feedback": "Earthworms don't swim. Damp skin lets them take in oxygen."},
             {"text": "Water is their only food", "feedback": "They eat bits of dead plants in soil. Moist skin is for breathing."},
             {"text": "To keep their bristles soft", "feedback": "The bristles grip the soil. Moist skin is what lets them breathe."}]},
    ],
}

# ---------------------------------------------------------------- The human eye (simple)
VISION = bio("36.5", "36-5-vision", "Vision")
eye = {
    "id": "g4-human-eye", "title": "The human eye (simple)", "grade": "4", "subject": "Life science",
    "standard": "4-LS1-2", "minutes": 9,
    "sources": [NGSS2, VISION],
    "keywords": ["eye", "vision", "sight", "cornea", "iris", "pupil", "lens", "retina", "optic nerve", "brain",
                 "senses", "light", "information processing"],
    "printed": [{"text": "Light", "at": [130, 470]}],
    "structures": [
        {"id": "eyeball", "name": "eyeball", "pen": "bold", "outlines": [{"circle": [420, 500, 150]}]},
        {"id": "cornea", "name": "cornea", "outlines": [{"path": "M 286 436 C 238 466 238 534 286 564"}]},
        {"id": "iris", "name": "iris", "outlines": [{"line": [292, 430, 292, 474]}, {"line": [292, 526, 292, 570]}]},
        {"id": "lens", "name": "lens", "outlines": [{"ellipse": [322, 500, 18, 42]}]},
        {"id": "retina", "name": "retina", "outlines": [{"path": "M 470 372 C 580 420 580 580 470 628"}]},
        {"id": "nerve", "name": "optic nerve", "outlines": [{"line": [566, 476, 712, 430]}, {"line": [566, 524, 716, 476]}]},
        {"id": "brain", "name": "brain", "outlines": [{"path": BRAIN}]},
        {"id": "light", "name": "light", "pen": "bold", "outlines": straight_arrow(60, 500, 232, 500)},
    ],
    "steps": [
        {"type": "trace", "title": "Eyeball", "structure": "eyeball", "instruction": "Trace the round eyeball.",
         "note": {"text": "Your eyes take in information about the world as light, so you can see what's around you."}},
        {"type": "trace", "title": "Cornea", "structure": "cornea", "instruction": "Trace the clear bulge at the front.",
         "note": {"text": "The cornea is the clear front of the eye. It protects the eye and starts bending light so you can see clearly.",
                  "remember": "Cornea: clear, protective front."}},
        {"type": "trace", "title": "Iris", "structure": "iris", "instruction": "Draw the iris, leaving the gap of the pupil between.",
         "note": {"text": "The iris is the colored ring of your eye. It makes the pupil, the hole in the middle, smaller in bright light and bigger in dim light.",
                  "remember": "Iris controls how much light enters."}},
        {"type": "trace", "title": "Lens", "structure": "lens", "instruction": "Trace the lens behind the iris.",
         "note": {"text": "The lens focuses light onto the back of the eye. It changes shape to focus on things near and far.",
                  "remember": "Lens focuses."}},
        {"type": "trace", "title": "Retina", "structure": "retina", "instruction": "Trace the retina lining the back of the eye.",
         "note": {"text": "The retina turns light into signals, a bit like a camera's sensor.", "remember": "Retina: light into signals."}},
        {"type": "trace", "title": "Optic nerve", "structure": "nerve", "instruction": "Draw the optic nerve running to the brain.",
         "note": {"text": "The optic nerve carries the signals from the retina to your brain."}},
        {"type": "trace", "title": "Brain", "structure": "brain", "instruction": "Trace the brain.",
         "note": {"text": "Your brain makes sense of the signals: it works out what you're seeing, then decides how you respond.",
                  "remember": "Senses gather; the brain decides."}},
        {"type": "trace", "title": "Light", "structure": "light", "instruction": "Draw the arrow of light coming into the eye.",
         "note": {"text": "You see an object when light from it enters your eye."}},
        {"type": "order", "title": "From light to brain", "items": ["Cornea", "Pupil", "Lens", "Retina", "Optic nerve", "Brain"],
         "instruction": "Tap the parts in the order light and its signals reach them.",
         "why": "Light passes the cornea, goes through the pupil, is focused by the lens onto the retina, and the optic nerve carries the signals to the brain.",
         "hint": "What's at the very front of the eye?"},
        {"type": "choice", "title": "Respond", "instruction": "Senses, brain, response.", "showsDiagram": True,
         "question": "You walk from a dark room into bright sunshine. What does your eye do?",
         "options": [
             {"text": "The iris makes the pupil smaller to let in less light", "correct": True,
              "feedback": "Yes. In bright light the iris shrinks the pupil, letting less light in. It happens without you even thinking about it."},
             {"text": "The pupil gets bigger", "feedback": "Pupils get bigger in dim light, to let more light in. In bright light they shrink."},
             {"text": "The lens falls back", "feedback": "The lens stays put. The iris changes the size of the pupil."},
             {"text": "Nothing changes", "feedback": "Your eye responds: the iris makes the pupil smaller in bright light."}]},
    ],
}

# ---------------------------------------------------------------- The human ear (simple)
HEARING = bio("36.4", "36-4-hearing-and-vestibular-sensation", "Hearing and Vestibular Sensation")
SKELETONS = bio("38.1", "38-1-types-of-skeletal-systems", "Types of Skeletal Systems (the smallest bones)")
outer_ear = ("M 232 300 C 142 320 118 450 158 540 C 188 610 250 640 260 600 C 270 560 240 522 260 482 "
             "C 280 432 300 360 232 300 Z")
ear = {
    "id": "g4-human-ear", "title": "The human ear (simple)", "grade": "4", "subject": "Life science",
    "standard": "4-LS1-2", "minutes": 9,
    "sources": [NGSS2, HEARING, SKELETONS],
    "keywords": ["ear", "hearing", "sound", "outer ear", "ear canal", "eardrum", "ossicles", "hammer", "anvil",
                 "stirrup", "cochlea", "auditory nerve", "brain", "senses", "information processing"],
    "printed": [{"text": "Sound", "at": [84, 372]}],
    "structures": [
        {"id": "outer", "name": "outer ear", "outlines": [{"path": outer_ear}]},
        {"id": "canal", "name": "ear canal", "outlines": [{"line": [264, 472, 420, 462]}, {"line": [262, 524, 420, 522]}]},
        {"id": "eardrum", "name": "eardrum", "pen": "bold", "outlines": [{"line": [428, 448, 432, 534]}]},
        {"id": "ossicles", "name": "ear bones",
         "outlines": [{"ellipse": [460, 468, 12, 26]}, {"circle": [494, 456, 14]},
                      {"polygon": [512, 474, 546, 482, 546, 502, 512, 506]}]},
        {"id": "cochlea", "name": "cochlea",
         "outlines": [{"path": "M 554 492 C 554 430 642 420 652 480 C 662 540 592 562 576 512 C 566 476 616 470 616 500"}]},
        {"id": "nerve", "name": "hearing nerve", "outlines": [{"line": [660, 470, 724, 446]}]},
        {"id": "brain", "name": "brain", "outlines": [{"path": BRAIN}]},
        {"id": "sound", "name": "sound", "pen": "bold", "outlines": straight_arrow(40, 450, 160, 470)},
    ],
    "steps": [
        {"type": "trace", "title": "Outer ear", "structure": "outer", "instruction": "Trace the outer ear.",
         "note": {"text": "Your ears take in information about the world as sound. The outer ear's shape helps collect sound and funnel it in.",
                  "remember": "Outer ear collects sound."}},
        {"type": "trace", "title": "Ear canal", "structure": "canal", "instruction": "Draw both sides of the ear canal.",
         "note": {"text": "Sound travels down the ear canal, a short tunnel into your head."}},
        {"type": "trace", "title": "Eardrum", "structure": "eardrum", "instruction": "Trace the eardrum at the end of the canal.",
         "note": {"text": "The eardrum is a thin sheet stretched across the canal. Sound makes it vibrate, like the skin of a drum.",
                  "remember": "Sound makes the eardrum vibrate."}},
        {"type": "trace", "title": "Ear bones", "structure": "ossicles", "instruction": "Trace the three tiny ear bones.",
         "note": {"text": "The hammer, anvil and stirrup pass the eardrum's vibrations inward. They're the smallest bones in your body.",
                  "remember": "Hammer, anvil, stirrup."}},
        {"type": "trace", "title": "Cochlea", "structure": "cochlea", "instruction": "Trace the snail-shaped cochlea.",
         "note": {"text": "The cochlea is filled with fluid. It turns the vibrations into signals your nerves can carry.",
                  "remember": "Cochlea: vibrations into signals."}},
        {"type": "trace", "title": "Hearing nerve", "structure": "nerve", "instruction": "Draw the nerve to the brain.",
         "note": {"text": "A nerve carries the signals from the cochlea to your brain."}},
        {"type": "trace", "title": "Brain", "structure": "brain", "instruction": "Trace the brain.",
         "note": {"text": "Your brain works out what the sound is, like a voice or a bell, and decides how you'll respond.",
                  "remember": "Senses gather; the brain decides."}},
        {"type": "trace", "title": "Sound", "structure": "sound", "instruction": "Draw the arrow of sound coming in.",
         "note": {"text": "Sound is made by vibrations that travel through the air to your ear."}},
        {"type": "order", "title": "From sound to brain", "items": ["Outer ear", "Ear canal", "Eardrum", "Ear bones", "Cochlea", "Brain"],
         "instruction": "Tap the parts in the order sound and its signals reach them.",
         "why": "The outer ear collects sound, it travels down the canal, shakes the eardrum and ear bones, the cochlea turns it into signals, and a nerve carries them to the brain.",
         "hint": "Which part catches the sound first?"},
        {"type": "choice", "title": "Respond", "instruction": "Senses, brain, response.", "showsDiagram": True,
         "question": "A friend calls your name from behind you, and you turn around. What happened?",
         "options": [
             {"text": "Your ears took in the sound, your brain recognized your name, and it told your body to turn", "correct": True,
              "feedback": "Yes. Senses gather information, the brain makes sense of it, and then you respond."},
             {"text": "Your ears turned your head", "feedback": "Ears only gather sound. Your brain decides to turn, and your muscles do it."},
             {"text": "Your eyes heard the sound", "feedback": "Eyes sense light. Sound is sensed by your ears, then your brain decides."},
             {"text": "The sound pushed your head around", "feedback": "Sound is too gentle for that. Your brain recognized your name and chose to turn."}]},
    ],
}

for lesson in (lungs, digestion, worm, eye, ear):
    save(lesson)
