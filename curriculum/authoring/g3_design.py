"""Grade 3 design-solution lessons · a fish ladder (3-LS4-4) and sorting cans with a magnet (3-PS2-4)."""
import math

from lib import head_at, save, straight_arrow


def fish(x, y, length=70, facing=1):
    f, L, h = facing, length, length * 0.42
    nose, joint = x + f * 0.5 * L, x - f * 0.38 * L
    body = (f"M {nose} {y} C {x + f * 0.3 * L} {y - 0.55 * h} {x - f * 0.2 * L} {y - 0.6 * h} {joint} {y} "
            f"C {x - f * 0.2 * L} {y + 0.6 * h} {x + f * 0.3 * L} {y + 0.55 * h} {nose} {y} Z")
    back = x - f * 0.66 * L
    return [{"path": body}, {"polygon": [round(v, 1) for v in [joint, y, back, y - 0.5 * h, x - f * 0.56 * L, y, back, y + 0.5 * h]]}]


# ---------------------------------------------------------------- Fish ladder
stairs = [940, 800]
x, y = 940, 800
for _ in range(6):
    x -= 55
    stairs += [x, y]
    y -= 76
    stairs += [x, y]
ladder = {
    "id": "g3-fish-ladder", "title": "When a dam blocks salmon: a fish ladder", "grade": "3", "subject": "Life science",
    "standard": "3-LS4-4", "minutes": 9,
    "sources": [{"title": "NGSS 3-LS4-4: Make a claim about the merit of a solution to a problem caused when the environment changes"},
                {"title": "NOAA Fisheries: Fish ladders", "url": "https://www.westcoast.fisheries.noaa.gov/fish_passage/about_dams_and_fish/fish_ladders.html"},
                {"title": "NOAA Fisheries: Adult upstream passage on the West Coast",
                 "url": "https://www.fisheries.noaa.gov/west-coast/endangered-species-conservation/adult-upstream-passage-west-coast"}],
    "keywords": ["dam", "salmon", "fish ladder", "fish passage", "habitat change", "environment", "solution", "migration"],
    "printed": [{"text": "Upstream", "at": [230, 250]}, {"text": "Downstream", "at": [790, 880]}],
    "structures": [
        {"id": "river", "name": "river", "outlines": [{"line": [60, 320, 430, 320]}, {"line": [570, 760, 940, 760]},
                                                     {"line": [60, 900, 940, 900]}]},
        {"id": "dam", "name": "dam", "pen": "bold", "outlines": [{"rect": [430, 260, 140, 640, 6]}]},
        {"id": "ladder", "name": "fish ladder", "outlines": [{"line": stairs + [570, y]}]},
        {"id": "salmon", "name": "salmon", "outlines": fish(780, 830, 120, -1),
         "details": [{"circle": [737, 826, 9]}]},
        {"id": "route", "name": "route past the dam", "pen": "bold",
         "outlines": [{"line": [880, 690, 620, 360, 580, 220, 420, 220, 370, 290]},
                      head_at((370, 290), ((370 - 420) / math.hypot(50, 70), (290 - 220) / math.hypot(50, 70)), 34)]},
    ],
    "steps": [
        {"type": "trace", "title": "River", "structure": "river", "instruction": "Trace the water on both sides and the riverbed.",
         "note": {"text": "Salmon hatch in rivers, swim to the sea, then return upstream to the same river to lay their eggs.",
                  "remember": "Salmon must swim upstream to have young."}},
        {"type": "trace", "title": "Dam", "structure": "dam", "instruction": "Trace the dam across the river.",
         "note": {"text": "People build dams to store water and make electricity. But a dam is a wall the salmon can't swim past: their environment has changed."}},
        {"type": "trace", "title": "Fish ladder", "structure": "ladder", "instruction": "Trace the steps beside the dam.",
         "note": {"text": "A fish ladder is a set of water-filled steps. Salmon swim or leap from pool to pool to climb past the dam, resting in the pools.",
                  "remember": "A ladder lets fish climb over a dam."}},
        {"type": "trace", "title": "Salmon", "structure": "salmon", "instruction": "Trace the salmon waiting below the dam.",
         "note": {"text": "Salmon are strong swimmers and jumpers, which is why ladders work well for them."}},
        {"type": "trace", "title": "Eye", "structure": "salmon", "part": "details", "instruction": "Dab the salmon's eye.",
         "note": {"text": "Salmon use smell and other senses to find their way back to the river where they hatched."}},
        {"type": "trace", "title": "Route", "structure": "route", "instruction": "Draw the arrow showing the salmon's way up the ladder and over the dam.",
         "note": {"text": "The flowing water at the bottom of the ladder attracts the fish and guides them in."}},
        {"type": "choice", "title": "The problem", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "Why could fewer salmon live in this river after the dam was built?",
         "options": [
             {"text": "The dam blocks them from swimming upstream to lay eggs", "correct": True,
              "feedback": "Yes. If adults can't reach their spawning grounds, fewer young salmon hatch each year."},
             {"text": "Salmon don't like electricity", "feedback": "The problem is the wall itself: it blocks their path upstream."},
             {"text": "The dam makes the water too cold", "feedback": "The main problem is that the dam blocks the way upstream."},
             {"text": "Salmon live only in the sea", "feedback": "Salmon need rivers too: they lay their eggs upstream."}]},
        {"type": "choice", "title": "Judge the solution", "instruction": "Think about what each idea solves.", "showsDiagram": True,
         "question": "Which solution best helps the salmon while keeping the dam working?",
         "options": [
             {"text": "Build a fish ladder beside the dam", "correct": True,
              "feedback": "Yes. Salmon can climb past, and the dam still stores water and makes electricity. Engineers design each ladder to suit the kind of fish."},
             {"text": "Remove the dam", "feedback": "That would help the salmon, but people would lose the water and electricity. A ladder solves both problems."},
             {"text": "Build the dam taller", "feedback": "That makes the wall even harder to pass. Salmon need a way around it."},
             {"text": "Add more fish below the dam", "feedback": "They still couldn't reach their spawning grounds upstream."}]},
    ],
}

# ---------------------------------------------------------------- Magnetic sorting
def can(x, y):
    return {"rect": [x - 34, y - 48, 68, 96, 10]}


sort = {
    "id": "g3-magnet-sorting", "title": "Design problem: sorting cans with a magnet", "grade": "3", "subject": "Physics",
    "standard": "3-PS2-4", "minutes": 8,
    "sources": [{"title": "NGSS 3-PS2-4: Define a simple design problem that can be solved by applying scientific ideas about magnets"},
                {"title": "Bunting: Recovering steel and aluminum cans with magnetic separators",
                 "url": "https://buntingmagnetics.com/blog/parry-evans-recover-metal-with-bunting-magnetic-separators"}],
    "keywords": ["magnet", "recycling", "steel", "aluminum", "sorting", "design", "engineering", "magnetic force"],
    "printed": [{"text": "Mixed cans", "at": [250, 470]}, {"text": "Magnet", "at": [600, 250]}],
    "structures": [
        {"id": "belt", "name": "conveyor belt", "outlines": [{"rect": [80, 640, 820, 60, 30]}],
         "details": [{"circle": [110, 670, 22]}, {"circle": [870, 670, 22]}]},
        {"id": "magnet", "name": "magnet", "pen": "bold", "outlines": [{"rect": [480, 290, 240, 90, 10]}]},
        {"id": "steelCans", "name": "steel cans", "outlines": [can(190, 590), can(600, 490)]},
        {"id": "aluminumCans", "name": "aluminum cans", "outlines": [can(310, 590), can(820, 590)]},
        {"id": "arrows", "name": "arrows", "pen": "bold",
         "outlines": straight_arrow(600, 430, 600, 395) + straight_arrow(760, 760, 900, 760)},
    ],
    "steps": [
        {"type": "trace", "title": "Conveyor belt", "structure": "belt", "instruction": "Trace the moving belt.",
         "note": {"text": "At a recycling center, a belt carries a jumble of cans. The design problem: separate steel cans from aluminum ones.",
                  "remember": "A design problem says what needs to be solved."}},
        {"type": "trace", "title": "Rollers", "structure": "belt", "part": "details", "instruction": "Draw the rollers at each end.",
         "note": {"text": "The rollers turn and keep the belt moving, so the cans pass under the magnet one after another."}},
        {"type": "trace", "title": "Magnet", "structure": "magnet", "instruction": "Trace the big magnet hanging above the belt.",
         "note": {"text": "Magnets attract objects made of iron or steel, even without touching them."}},
        {"type": "trace", "title": "Steel cans", "structure": "steelCans", "instruction": "Trace the steel can on the belt and the one being lifted.",
         "note": {"text": "Steel contains iron, so the magnet pulls steel cans up off the belt.", "remember": "Magnets attract iron and steel."}},
        {"type": "trace", "title": "Aluminum cans", "structure": "aluminumCans", "instruction": "Trace the two aluminum cans.",
         "note": {"text": "Aluminum isn't attracted to magnets, so aluminum cans stay on the belt and ride on to their own bin."}},
        {"type": "trace", "title": "Arrows", "structure": "arrows", "instruction": "Draw the arrows: one lifting the steel can, one moving the aluminum on.",
         "note": {"text": "One simple idea, that magnets attract steel but not aluminum, solves the sorting problem."}},
        {"type": "choice", "title": "Explain", "instruction": "Use what you've drawn.", "showsDiagram": True,
         "question": "Why does the aluminum can stay on the belt?",
         "options": [
             {"text": "Aluminum isn't attracted to magnets", "correct": True, "feedback": "Right. Only iron and steel (and a few other metals) are pulled by the magnet."},
             {"text": "It's too heavy", "feedback": "Aluminum cans are light. They stay because magnets don't attract aluminum."},
             {"text": "The magnet is switched off", "feedback": "The magnet is working: it's lifting the steel can."},
             {"text": "It's stuck to the belt", "feedback": "Nothing holds it down. The magnet just doesn't attract aluminum."}]},
        {"type": "choice", "title": "Define a problem", "instruction": "Think like an engineer.", "showsDiagram": False,
         "question": "Which of these problems could you solve with a magnet?",
         "options": [
             {"text": "Picking up spilled steel paper clips from the floor", "correct": True,
              "feedback": "Yes. Steel clips are attracted to a magnet, so you can sweep it over the floor and lift them up."},
             {"text": "Separating paper from plastic", "feedback": "Neither paper nor plastic is attracted to magnets."},
             {"text": "Picking up spilled sand", "feedback": "Ordinary sand isn't attracted to magnets."},
             {"text": "Sorting glass bottles by color", "feedback": "Glass isn't attracted to magnets, whatever its color."}]},
    ],
}

for lesson in (ladder, sort):
    save(lesson)
