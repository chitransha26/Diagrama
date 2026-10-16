"""Grade 3 physical science · forces (3-PS2-1), a pendulum (3-PS2-2), magnets (3-PS2-3)."""
import math

from lib import arc_arrow, head_at, r, save, straight_arrow

# ---------------------------------------------------------------- Balanced and unbalanced forces
forces = {
    "id": "g3-balanced-forces", "title": "Balanced and unbalanced forces: tug of war", "grade": "3",
    "subject": "Physics", "standard": "3-PS2-1", "minutes": 8,
    "keywords": ["force", "push", "pull", "balanced", "unbalanced", "tug of war", "motion", "arrow"],
    "printed": [{"text": "Balanced", "at": [500, 150]}, {"text": "Unbalanced", "at": [500, 590]}],
    "structures": [
        {"id": "ropes", "name": "rope and flag",
         "outlines": [{"line": [150, 320, 850, 320]}, {"polygon": [500, 320, 500, 260, 540, 280]},
                      {"line": [150, 760, 850, 760]}, {"polygon": [500, 760, 500, 700, 540, 720]}]},
        {"id": "balanced", "name": "balanced pulls", "pen": "bold",
         "outlines": straight_arrow(420, 380, 200, 380) + straight_arrow(580, 380, 800, 380)},
        {"id": "unbalanced", "name": "unbalanced pulls", "pen": "bold",
         "outlines": straight_arrow(420, 820, 150, 820) + straight_arrow(580, 820, 690, 820)},
        {"id": "motion", "name": "motion arrow", "outlines": straight_arrow(560, 650, 440, 650)},
    ],
    "steps": [
        {"type": "trace", "title": "Ropes", "structure": "ropes",
         "instruction": "Trace both ropes and the flags tied to their middles.",
         "note": {"text": "In tug of war, two teams pull a rope in opposite directions. The flag shows which way the rope moves."}},
        {"type": "trace", "title": "Balanced pulls", "structure": "balanced",
         "instruction": "Draw the two arrows for the top rope. They're the same length.",
         "note": {"text": "An arrow shows a force: it points in the force's direction, and a longer arrow means a stronger force. Equal and opposite forces are balanced.",
                  "remember": "Balanced forces: no change in motion."}},
        {"type": "trace", "title": "Unbalanced pulls", "structure": "unbalanced",
         "instruction": "Draw the two arrows for the bottom rope. The left one is longer.",
         "note": {"text": "When one pull is stronger, the forces are unbalanced. Unbalanced forces change an object's motion.",
                  "remember": "The longer arrow wins."}},
        {"type": "trace", "title": "Motion", "structure": "motion",
         "instruction": "Draw the arrow showing which way the bottom flag moves.",
         "note": {"text": "The rope moves toward the stronger pull. The bigger the difference between the forces, the faster its motion changes."}},
        {"type": "choice", "title": "Predict", "instruction": "Use the arrows you drew.", "showsDiagram": True,
         "question": "In the top rope, both teams pull equally hard. What happens to the flag?",
         "options": [
             {"text": "It stays still", "correct": True,
              "feedback": "Right. The forces are balanced, so the rope's motion doesn't change: it stays still."},
             {"text": "It moves left", "feedback": "That needs a stronger pull to the left. These pulls are equal."},
             {"text": "It moves right", "feedback": "That needs a stronger pull to the right. These pulls are equal."},
             {"text": "The rope breaks", "feedback": "Equal pulls don't move the rope. A rope only breaks if the forces are too big for it."}]},
        {"type": "choice", "title": "Change it", "instruction": "Think about the bottom rope.", "showsDiagram": True,
         "question": "How could the right-hand team stop the flag from moving left?",
         "options": [
             {"text": "Pull harder until both pulls are equal", "correct": True,
              "feedback": "Yes. Making the forces equal balances them, and the rope stops changing its motion."},
             {"text": "Let go of the rope", "feedback": "Then only the left team pulls, and the flag moves left even faster."},
             {"text": "Pull more gently", "feedback": "A weaker pull makes the difference bigger, so the flag moves left faster."},
             {"text": "Nothing can stop it", "feedback": "Balancing the forces stops the change in motion."}]},
    ],
}

# ---------------------------------------------------------------- Pendulum
pivot = (500, 140)
length = 440


def bob_at(angle_deg):
    a = math.radians(angle_deg)
    return (r(pivot[0] + length * math.cos(a)), r(pivot[1] + length * math.sin(a)))


positions = [bob_at(a) for a in (120, 90, 60)]
swing = arc_arrow(pivot[0], pivot[1], 560, 66, 114)
t0 = math.radians(66)
swing.append(head_at((pivot[0] + 560 * math.cos(t0), pivot[1] + 560 * math.sin(t0)), (math.sin(t0), -math.cos(t0))))
pendulum = {
    "id": "g3-pendulum", "title": "A pendulum's swing", "grade": "3", "subject": "Physics",
    "standard": "3-PS2-2", "minutes": 7,
    "keywords": ["pendulum", "swing", "pattern", "motion", "predict", "clock"],
    "structures": [
        {"id": "pivot", "name": "pivot", "pen": "bold", "outlines": [{"line": [420, 140, 580, 140]}]},
        {"id": "strings", "name": "strings", "pen": "fine",
         "outlines": [{"line": [pivot[0], pivot[1], p[0], p[1]]} for p in positions]},
        {"id": "bobs", "name": "bob", "outlines": [{"circle": [p[0], p[1], 32]} for p in positions]},
        {"id": "swing", "name": "swing path", "outlines": swing},
    ],
    "steps": [
        {"type": "trace", "title": "Pivot", "structure": "pivot", "instruction": "Trace the bar the pendulum hangs from.",
         "note": {"text": "The pivot is the fixed point the pendulum swings around. It doesn't move."}},
        {"type": "trace", "title": "Strings", "structure": "strings",
         "instruction": "Trace the string in all three positions: left, middle and right.",
         "note": {"text": "We draw the same pendulum three times to show where it is at different moments as it swings."}},
        {"type": "trace", "title": "Bob", "structure": "bobs", "instruction": "Trace the weight, called the bob, in each position.",
         "note": {"text": "The bob swings fastest at the bottom and slows to a stop for an instant at each side before swinging back.",
                  "remember": "Fastest at the bottom, slowest at the sides."}},
        {"type": "trace", "title": "Swing path", "structure": "swing", "instruction": "Draw the curved path the bob follows, with arrows at both ends.",
         "note": {"text": "The bob swings back and forth along the same path, and each swing takes the same time. That repeating pattern lets us predict it.",
                  "remember": "Pendulum clocks use this steady pattern."}},
        {"type": "choice", "title": "Predict", "instruction": "Use the pattern you drew.", "showsDiagram": True,
         "question": "The bob has just reached the far left. Where will it go next?",
         "options": [
             {"text": "Back through the middle toward the right", "correct": True,
              "feedback": "Yes. It always swings back along the same path: the pattern repeats."},
             {"text": "It stays on the left", "feedback": "It stops only for an instant at the side, then gravity pulls it back down."},
             {"text": "Higher up on the left", "feedback": "A pendulum never swings higher than where it started. It swings back."},
             {"text": "Somewhere random", "feedback": "Its motion follows a pattern, so we can predict exactly where it goes next."}]},
    ],
}

# ---------------------------------------------------------------- Magnets
def magnet(x, y):
    return {"rect": [x, y, 300, 90, 8]}


magnets = {
    "id": "g3-magnets", "title": "Magnets attract and repel", "grade": "3", "subject": "Physics",
    "standard": "3-PS2-3", "minutes": 7,
    "keywords": ["magnet", "north pole", "south pole", "attract", "repel", "magnetic force"],
    "printed": [
        {"text": "Attract", "at": [500, 170]}, {"text": "Repel", "at": [500, 600]},
        {"text": "N", "at": [195, 265]}, {"text": "S", "at": [345, 265]}, {"text": "N", "at": [655, 265]}, {"text": "S", "at": [805, 265]},
        {"text": "N", "at": [195, 695]}, {"text": "S", "at": [345, 695]}, {"text": "S", "at": [655, 695]}, {"text": "N", "at": [805, 695]},
    ],
    "structures": [
        {"id": "attract", "name": "attracting magnets", "outlines": [magnet(120, 220), magnet(580, 220)],
         "details": [{"line": [270, 220, 270, 310]}, {"line": [730, 220, 730, 310]}]},
        {"id": "attractArrows", "name": "attraction arrows", "pen": "bold",
         "outlines": straight_arrow(330, 380, 450, 380) + straight_arrow(670, 380, 550, 380)},
        {"id": "repel", "name": "repelling magnets", "outlines": [magnet(120, 650), magnet(580, 650)],
         "details": [{"line": [270, 650, 270, 740]}, {"line": [730, 650, 730, 740]}]},
        {"id": "repelArrows", "name": "repulsion arrows", "pen": "bold",
         "outlines": straight_arrow(450, 810, 330, 810) + straight_arrow(550, 810, 670, 810)},
    ],
    "steps": [
        {"type": "trace", "title": "Magnets", "structure": "attract", "instruction": "Trace the two top magnets.",
         "note": {"text": "Every magnet has two ends, called poles: north (N) and south (S). The magnetic force is strongest at the poles."}},
        {"type": "trace", "title": "Poles", "structure": "attract", "part": "details", "instruction": "Draw the line splitting each magnet into its two poles.",
         "note": {"text": "Here, the south pole of one magnet faces the north pole of the other.", "remember": "Opposite poles attract."}},
        {"type": "trace", "title": "Attract", "structure": "attractArrows", "instruction": "Draw the arrows showing the magnets pulling together.",
         "note": {"text": "Opposite poles pull toward each other, even without touching. Magnetic force can act across a gap."}},
        {"type": "trace", "title": "Magnets", "structure": "repel", "instruction": "Trace the two bottom magnets.",
         "note": {"text": "This time the second magnet is turned around, so two south poles face each other."}},
        {"type": "trace", "title": "Poles", "structure": "repel", "part": "details", "instruction": "Draw the line splitting each magnet into its two poles.",
         "note": {"text": "Look at the letters in the middle: S faces S.", "remember": "Same poles repel."}},
        {"type": "trace", "title": "Repel", "structure": "repelArrows", "instruction": "Draw the arrows showing the magnets pushing apart.",
         "note": {"text": "Like poles push each other away. You can feel this push when you try to force them together."}},
        {"type": "choice", "title": "Predict", "instruction": "Use the magnets you drew.", "showsDiagram": True,
         "question": "You turn the bottom-right magnet around so its N faces the other magnet's S. What happens?",
         "options": [
             {"text": "They attract", "correct": True, "feedback": "Yes. Now opposite poles face each other, so they pull together."},
             {"text": "They repel even harder", "feedback": "Repelling happens when the same poles face each other. N and S are opposites."},
             {"text": "Nothing changes", "feedback": "Turning a magnet around swaps which pole faces the other magnet, which changes the force."},
             {"text": "They lose their magnetism", "feedback": "Turning a magnet doesn't remove its magnetism. It changes which poles face each other."}]},
    ],
}

for lesson in (forces, pendulum, magnets):
    save(lesson)
