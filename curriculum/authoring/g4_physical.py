"""Grade 4 physical science · circuits (4-PS3-2), a wind turbine (4-PS3-4), waves (4-PS4-1),
seeing by reflected light (4-PS4-2) and sending a coded message (4-PS4-3).

Facts checked against OpenStax University Physics (searched with curriculum/tools/openstax.py),
the U.S. Department of Energy and the ITU's International Morse code standard.
"""
import math

from lib import save, straight_arrow


def ngss(code, text):
    return {"title": f"NGSS {code}: {text}"}


def up(vol, section, slug, title):
    return {"title": f"OpenStax University Physics Volume {vol}, {section} {title}",
            "url": f"https://openstax.org/books/university-physics-volume-{vol}/pages/{slug}"}


# ---------------------------------------------------------------- A simple circuit
circuit = {
    "id": "g4-simple-circuit", "title": "A simple circuit: battery, wire, bulb", "grade": "4", "subject": "Physics",
    "standard": "4-PS3-2", "minutes": 7,
    "sources": [ngss("4-PS3-2", "Make observations to provide evidence that energy can be transferred from place to place by "
                                 "sound, light, heat, and electric currents"),
                up(2, "10.1", "10-1-electromotive-force", "Electromotive Force (a battery needs a complete circuit)")],
    "keywords": ["circuit", "battery", "wire", "bulb", "switch", "electricity", "electric current", "energy transfer",
                 "closed circuit", "open circuit"],
    "structures": [
        {"id": "battery", "name": "battery", "pen": "bold",
         "outlines": [{"rect": [180, 420, 90, 160, 8]}, {"rect": [210, 400, 30, 16, 3]}]},
        {"id": "wires", "name": "wires",
         "outlines": [{"line": [225, 398, 225, 250, 860, 250, 860, 495, 804, 495]},
                      {"line": [775, 518, 775, 750, 556, 750]}, {"line": [444, 750, 225, 750, 225, 584]}]},
        {"id": "switch", "name": "switch",
         "outlines": [{"line": [450, 750, 546, 742]}],
         "details": [{"circle": [446, 750, 8]}, {"circle": [554, 750, 8]}]},
        {"id": "bulb", "name": "bulb",
         "outlines": [{"circle": [775, 410, 60]}, {"rect": [750, 476, 50, 38, 4]}],
         "details": [{"line": [745, 432, 760, 400, 775, 432, 790, 400, 805, 432]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Battery", "structure": "battery", "instruction": "Trace the battery and its bump on top.",
         "note": {"text": "A battery stores energy. When it's connected in a complete loop, it pushes an electric current around.",
                  "remember": "Battery = stored energy."}},
        {"type": "trace", "title": "Wires", "structure": "wires", "instruction": "Trace the wires that run from the battery to the bulb and back.",
         "note": {"text": "Metal wires carry the electric current. Energy travels along them from the battery to the bulb.",
                  "remember": "Wires carry the current."}},
        {"type": "trace", "title": "Switch", "structure": "switch", "instruction": "Draw the switch closing the gap in the wire.",
         "note": {"text": "A switch opens or closes the loop. Closed, current can flow all the way round. Open, the loop is broken and it stops.",
                  "remember": "Closed switch = complete circuit."}},
        {"type": "trace", "title": "Contacts", "structure": "switch", "part": "details", "instruction": "Dab the two metal contacts of the switch.",
         "note": {"text": "The switch's metal bar touches both contacts to join the wire."}},
        {"type": "trace", "title": "Bulb", "structure": "bulb", "instruction": "Trace the glass bulb and its metal base.",
         "note": {"text": "Current flows in through the base and out again, so the bulb is part of the loop too."}},
        {"type": "trace", "title": "Filament", "structure": "bulb", "part": "details", "instruction": "Draw the zigzag wire inside the bulb.",
         "note": {"text": "As the current flows through the bulb, energy from the battery comes out as light. Energy has moved from place to place.",
                  "remember": "Electric current carries energy."}},
        {"type": "label", "title": "Label the parts", "instruction": "Pick the right name for each numbered part.",
         "targets": [
             {"n": 1, "at": [225, 500], "answer": "Battery", "role": "Stores energy and pushes current."},
             {"n": 2, "at": [540, 250], "answer": "Wire", "role": "Carries the current."},
             {"n": 3, "at": [500, 746], "answer": "Switch", "role": "Opens or closes the loop."},
             {"n": 4, "at": [775, 410], "answer": "Bulb", "role": "Gives off light."}],
         "vocabulary": ["Battery", "Wire", "Switch", "Bulb", "Magnet"],
         "commonMistakes": {"Magnet": "There's no magnet in this circuit. It's a battery, wires, a switch and a bulb."}},
        {"type": "choice", "title": "Predict", "instruction": "Think about the loop.", "showsDiagram": True,
         "question": "What happens to the bulb if you open the switch?",
         "options": [
             {"text": "It goes out, because the loop is broken", "correct": True,
              "feedback": "Yes. Current only flows around a complete loop. Open the switch and no energy reaches the bulb."},
             {"text": "It gets brighter", "feedback": "Opening the switch breaks the loop, so current stops and the bulb goes out."},
             {"text": "It stays the same", "feedback": "The bulb needs a complete loop. With the switch open, it goes out."},
             {"text": "The battery fills back up", "feedback": "Opening the switch just stops the current. The bulb goes out."}]},
        {"type": "choice", "title": "Energy", "instruction": "Where does the energy go?", "showsDiagram": True,
         "question": "In this circuit, how does energy get from the battery to the bulb?",
         "options": [
             {"text": "An electric current carries it through the wires", "correct": True,
              "feedback": "Right. Electric currents are one way energy moves from place to place. Sound, light and heat are others."},
             {"text": "It jumps through the air", "feedback": "The energy travels through the wires, carried by the electric current."},
             {"text": "The switch makes the energy", "feedback": "The switch only opens or closes the loop. The battery supplies the energy."},
             {"text": "Light carries it from the battery", "feedback": "Light comes out of the bulb. Getting there, the energy travels as an electric current."}]},
    ],
}

# ---------------------------------------------------------------- A wind turbine
DOE = {"title": "U.S. Department of Energy: Explore a Wind Turbine (text version)",
       "url": "https://www.energy.gov/eere/wind/how-wind-turbine-works-text-version"}


def blade(angle):
    """A blade from the hub at (462, 342), pointing `angle` degrees clockwise from straight up."""
    a = math.radians(angle)
    def at(x, y):  # local (x across, y along the blade, negative = outward)
        return f"{462 + x * math.cos(a) - y * math.sin(a):.1f} {342 + x * math.sin(a) + y * math.cos(a):.1f}"
    return {"path": f"M {at(0, -26)} C {at(30, -60)} {at(36, -150)} {at(0, -236)} C {at(-14, -150)} {at(-12, -60)} {at(0, -26)} Z"}


turbine = {
    "id": "g4-wind-turbine", "title": "A wind turbine making electricity", "grade": "4", "subject": "Physics",
    "standard": "4-PS3-4", "minutes": 8,
    "sources": [ngss("4-PS3-4", "Apply scientific ideas to design, test, and refine a device that converts energy from one form to another"), DOE],
    "keywords": ["wind turbine", "wind", "energy", "electricity", "generator", "blades", "rotor", "tower", "renewable",
                 "energy conversion", "engineering design"],
    "printed": [{"text": "Wind", "at": [120, 250]}],
    "structures": [
        {"id": "tower", "name": "tower", "pen": "bold", "outlines": [{"polygon": [478, 900, 522, 900, 510, 372, 490, 372]}]},
        {"id": "nacelle", "name": "nacelle", "outlines": [{"rect": [480, 318, 120, 48, 10]}]},
        {"id": "rotor", "name": "blades and hub", "outlines": [{"circle": [462, 342, 22]}, blade(0), blade(120), blade(240)]},
        {"id": "wind", "name": "wind", "pen": "bold", "outlines": straight_arrow(60, 300, 220, 300) + straight_arrow(60, 420, 220, 420)},
        {"id": "cable", "name": "power line", "outlines": [{"line": [524, 880, 640, 880, 640, 790, 756, 790]}]},
        {"id": "house", "name": "house", "outlines": [{"rect": [762, 700, 140, 120, 4]}, {"line": [740, 704, 832, 618, 924, 704]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Tower", "structure": "tower", "instruction": "Trace the tall tower.",
         "note": {"text": "The tower lifts the turbine high up, where the wind blows faster. Faster wind means more electricity.",
                  "remember": "Taller tower, faster wind."}},
        {"type": "trace", "title": "Nacelle", "structure": "nacelle", "instruction": "Trace the box at the top of the tower.",
         "note": {"text": "This box, the nacelle, holds the generator: the machine that turns spinning motion into electricity.",
                  "remember": "Generator: motion into electricity."}},
        {"type": "trace", "title": "Blades", "structure": "rotor", "instruction": "Trace the hub and all three blades.",
         "note": {"text": "Wind pushes on the blades, which are shaped like airplane wings. They spin the hub, which turns a shaft in the nacelle.",
                  "remember": "Wind spins the blades."}},
        {"type": "trace", "title": "Wind", "structure": "wind", "instruction": "Draw the two arrows of wind blowing in.",
         "note": {"text": "Moving air has energy. The turbine changes the wind's energy of motion into electrical energy."}},
        {"type": "trace", "title": "Power line", "structure": "cable", "instruction": "Draw the power line from the tower to the house.",
         "note": {"text": "Wires carry the electricity from the turbine to where people use it."}},
        {"type": "trace", "title": "House", "structure": "house", "instruction": "Trace the house and its roof.",
         "note": {"text": "In the house, the electricity can change form again: into light from lamps or sound from a radio."}},
        {"type": "order", "title": "Energy's path", "items": ["Wind blows", "Blades spin", "Generator makes electricity", "Lights glow in the house"],
         "instruction": "Tap the steps in order.",
         "why": "The wind's motion spins the blades, the generator turns that spinning into electricity, and wires carry it to the house.",
         "hint": "What makes the blades move?"},
        {"type": "choice", "title": "Improve the design", "instruction": "Think like an engineer.", "showsDiagram": True,
         "question": "Engineers want this turbine to make more electricity. Which change would help?",
         "options": [
             {"text": "Build a taller tower to reach faster wind", "correct": True,
              "feedback": "Yes. Wind usually blows faster higher up, and faster wind spins the blades harder, making more electricity."},
             {"text": "Paint the blades a brighter color", "feedback": "Color doesn't change how hard the wind pushes. A taller tower reaches faster wind."},
             {"text": "Move the turbine indoors", "feedback": "Indoors there's no wind to spin it. It needs to be up in fast-moving air."},
             {"text": "Take off one blade", "feedback": "The blades catch the wind. A taller tower, reaching faster wind, would help more."}]},
    ],
}

# ---------------------------------------------------------------- Parts of a wave
WAVES = up(1, "16.1", "16-1-traveling-waves", "Traveling Waves")
wave_pts = []
for i in range(0, 81):
    x = 80 + i * 10
    wave_pts += [x, round(520 - 120 * math.sin(2 * math.pi * (x - 80) / 400), 1)]
wave = {
    "id": "g4-wave-parts", "title": "Parts of a wave: crest, trough, wavelength", "grade": "4", "subject": "Physics",
    "standard": "4-PS4-1", "minutes": 7,
    "sources": [ngss("4-PS4-1", "Develop a model of waves to describe patterns in terms of amplitude and wavelength and that "
                                 "waves can cause objects to move"), WAVES],
    "keywords": ["wave", "crest", "trough", "wavelength", "amplitude", "water waves", "motion", "pattern"],
    "structures": [
        {"id": "rest", "name": "calm water line", "outlines": [{"line": [80, 520, 920, 520]}]},
        {"id": "wave", "name": "wave", "pen": "bold", "outlines": [{"line": wave_pts}]},
        {"id": "wavelength", "name": "wavelength", "outlines": [{"line": [180, 330, 580, 330]}, {"line": [180, 310, 180, 350]}, {"line": [580, 310, 580, 350]}]},
        {"id": "amplitude", "name": "amplitude", "outlines": straight_arrow(580, 520, 580, 408)},
        {"id": "ball", "name": "floating ball", "outlines": [{"circle": [780, 608, 30]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Calm water", "structure": "rest", "instruction": "Trace the straight line where calm water would be.",
         "note": {"text": "This line shows where the water would sit if there were no waves. We measure the wave from here."}},
        {"type": "trace", "title": "Wave", "structure": "wave", "instruction": "Trace the wave, up and down along the water.",
         "note": {"text": "The highest points are crests; the lowest points are troughs. A wave repeats this pattern again and again.",
                  "remember": "Crest = top, trough = bottom."}},
        {"type": "trace", "title": "Wavelength", "structure": "wavelength", "instruction": "Draw the line from one crest to the next.",
         "note": {"text": "The wavelength is the distance from one crest to the next crest. Short waves have crests close together.",
                  "remember": "Wavelength: crest to crest."}},
        {"type": "trace", "title": "Amplitude", "structure": "amplitude", "instruction": "Draw the arrow from the calm line up to a crest.",
         "note": {"text": "The amplitude is how high the wave rises above the calm line. Bigger waves have a bigger amplitude.",
                  "remember": "Amplitude: how tall."}},
        {"type": "trace", "title": "Floating ball", "structure": "ball", "instruction": "Trace the ball floating in a trough.",
         "note": {"text": "As waves pass, a floating ball bobs up and down. Waves can make objects move!",
                  "remember": "Waves can move things."}},
        {"type": "label", "title": "Label the wave", "instruction": "Pick the right name for each numbered part.",
         "targets": [
             {"n": 1, "at": [180, 400], "answer": "Crest", "role": "The highest point."},
             {"n": 2, "at": [380, 640], "answer": "Trough", "role": "The lowest point.",
              "mistakes": {"Crest": "Crests are the tops. This low point is a trough."}},
             {"n": 3, "at": [380, 330], "answer": "Wavelength", "role": "Crest to crest."},
             {"n": 4, "at": [580, 470], "answer": "Amplitude", "role": "How high the wave rises."}],
         "vocabulary": ["Crest", "Trough", "Wavelength", "Amplitude", "Shore"]},
        {"type": "choice", "title": "Predict", "instruction": "Think about the ball.", "showsDiagram": True,
         "question": "A storm makes waves with a much bigger amplitude. What happens to the floating ball?",
         "options": [
             {"text": "It bobs up and down much farther", "correct": True,
              "feedback": "Yes. Taller waves lift it higher and drop it lower: the ball's motion follows the wave's amplitude."},
             {"text": "It stops moving", "feedback": "Bigger waves move it more, not less."},
             {"text": "It moves up and down the same amount", "feedback": "The amplitude changed, so the ball's bobbing changes too: it moves farther."},
             {"text": "It sinks", "feedback": "A ball still floats. Bigger waves just make it bob farther up and down."}]},
    ],
}

# ---------------------------------------------------------------- Seeing by reflected light
REFLECTION = up(3, "1.2", "1-2-the-law-of-reflection", "The Law of Reflection")
VISION = {"title": "OpenStax Biology 2e, 36.5 Vision", "url": "https://openstax.org/books/biology-2e/pages/36-5-vision"}
apple = "M 520 586 C 470 556 410 590 418 652 C 426 720 480 760 520 736 C 560 760 614 720 622 652 C 630 590 570 556 520 586 Z"
sun_rays = [{"line": [round(150 + 84 * math.cos(math.radians(a)), 1), round(180 + 84 * math.sin(math.radians(a)), 1),
                      round(150 + 118 * math.cos(math.radians(a)), 1), round(180 + 118 * math.sin(math.radians(a)), 1)]}
            for a in range(0, 360, 45)]
light = {
    "id": "g4-light-into-eye", "title": "Light reflecting into the eye", "grade": "4", "subject": "Physics",
    "standard": "4-PS4-2", "minutes": 7,
    "sources": [ngss("4-PS4-2", "Develop a model to describe that light reflecting from objects and entering the eye allows "
                                 "objects to be seen"), REFLECTION, VISION],
    "keywords": ["light", "reflection", "seeing", "eye", "sun", "light source", "reflect", "vision", "model"],
    "structures": [
        {"id": "sun", "name": "sun", "pen": "bold", "outlines": [{"circle": [150, 180, 66]}], "details": sun_rays},
        {"id": "apple", "name": "apple", "outlines": [{"path": apple}, {"line": [520, 586, 532, 540]}]},
        {"id": "eye", "name": "eye", "outlines": [{"path": "M 786 420 C 828 376 892 376 934 420 C 892 464 828 464 786 420 Z"}, {"circle": [860, 420, 22]}]},
        {"id": "rays", "name": "light", "pen": "bold", "outlines": straight_arrow(206, 236, 470, 566) + straight_arrow(590, 600, 780, 446)},
    ],
    "steps": [
        {"type": "trace", "title": "Sun", "structure": "sun", "instruction": "Trace the sun.",
         "note": {"text": "The sun gives off its own light. Things that give off light, like the sun or a lamp, are light sources.",
                  "remember": "Light sources make light."}},
        {"type": "trace", "title": "Sunbeams", "structure": "sun", "part": "details", "instruction": "Draw the sun's rays.",
         "note": {"text": "Light spreads out from the sun in every direction."}},
        {"type": "trace", "title": "Apple", "structure": "apple", "instruction": "Trace the apple and its stem.",
         "note": {"text": "An apple makes no light of its own. We can only see it when light shines on it.",
                  "remember": "Most things don't make their own light."}},
        {"type": "trace", "title": "Eye", "structure": "eye", "instruction": "Trace the eye and its colored iris.",
         "note": {"text": "Your eye takes in light. Inside, it turns the light into signals for your brain."}},
        {"type": "trace", "title": "Light's path", "structure": "rays", "instruction": "Draw the light from the sun to the apple, then from the apple to the eye.",
         "note": {"text": "Light bounces, or reflects, off the apple. Some of it enters your eye, and that's how you see the apple.",
                  "remember": "We see light that reflects into our eyes."}},
        {"type": "order", "title": "How you see", "items": ["Sun gives off light", "Light hits the apple", "Light reflects off the apple", "Light enters your eye"],
         "instruction": "Tap the steps in order.",
         "why": "Light from a source hits the apple, reflects off it, and travels into your eye.",
         "hint": "Where does the light come from?"},
        {"type": "choice", "title": "Explain", "instruction": "Use your model.", "showsDiagram": True,
         "question": "In a room with no light at all, can you see the apple?",
         "options": [
             {"text": "No, because no light can reflect off it into your eyes", "correct": True,
              "feedback": "Right. Seeing needs light to bounce off the apple and enter your eyes. With no light, there's nothing to see."},
             {"text": "Yes, if you look hard enough", "feedback": "Looking harder doesn't help: you can only see light that enters your eyes."},
             {"text": "Yes, apples glow a little", "feedback": "Apples don't make their own light. They can only be seen by light reflecting off them."},
             {"text": "Only if it's a red apple", "feedback": "Color doesn't matter. Without light to reflect, you can't see any apple."}]},
        {"type": "choice", "title": "Explain", "instruction": "One more about reflection.", "showsDiagram": False,
         "question": "Why can everyone in a classroom see the same poster, wherever they sit?",
         "options": [
             {"text": "Its rough surface reflects light in every direction", "correct": True,
              "feedback": "Yes. Rough surfaces like paper scatter light every way, so some reaches every eye in the room."},
             {"text": "The poster makes its own light", "feedback": "Posters don't make light. They reflect light in every direction."},
             {"text": "Light only reflects straight back", "feedback": "That's how a mirror reflects. Rough paper scatters light in every direction."},
             {"text": "The poster is very big", "feedback": "Size isn't the reason. Its rough surface reflects light every way, into every eye."}]},
    ],
}

# ---------------------------------------------------------------- Sending a message in code
ITU = {"title": "ITU-R M.1677-1: International Morse code",
       "url": "https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1677-1-200910-I!!PDF-E.pdf"}
code = {
    "id": "g4-message-in-code", "title": "Sending a message in code", "grade": "4", "subject": "Physics",
    "standard": "4-PS4-3", "minutes": 7,
    "sources": [ngss("4-PS4-3", "Generate and compare multiple solutions that use patterns to transfer information"), ITU],
    "keywords": ["code", "Morse code", "pattern", "information", "message", "flashlight", "signal", "dots", "dashes",
                 "communication", "engineering design"],
    "structures": [
        {"id": "torch", "name": "flashlight", "pen": "bold", "outlines": [{"rect": [120, 440, 180, 80, 14]}]},
        {"id": "head", "name": "flashlight head", "outlines": [{"polygon": [310, 430, 370, 400, 370, 560, 310, 530]}]},
        {"id": "beam", "name": "flash of light", "outlines": [{"line": [392, 440, 572, 384]}, {"line": [392, 480, 572, 480]}, {"line": [392, 520, 572, 576]}]},
        {"id": "tape", "name": "message strip", "outlines": [{"rect": [100, 700, 800, 120, 10]}]},
        {"id": "letterO", "name": "letter O", "pen": "bold",
         "outlines": [{"line": [150, 760, 210, 760]}, {"line": [240, 760, 300, 760]}, {"line": [330, 760, 390, 760]}]},
        {"id": "letterK", "name": "letter K", "pen": "bold",
         "outlines": [{"line": [470, 760, 530, 760]}, {"circle": [560, 760, 9]}, {"line": [590, 760, 650, 760]}]},
    ],
    "steps": [
        {"type": "trace", "title": "Flashlight", "structure": "torch", "instruction": "Trace the flashlight's handle.",
         "note": {"text": "You can send a message without words by using a pattern: flashing a light on and off."}},
        {"type": "trace", "title": "Flashlight head", "structure": "head", "instruction": "Trace the flashlight's head.",
         "note": {"text": "A short flash is a dot. A long flash, three times as long, is a dash. That's Morse code.",
                  "remember": "Dash = three dots long."}},
        {"type": "trace", "title": "Flash", "structure": "beam", "instruction": "Draw the three lines of the flash.",
         "note": {"text": "Light travels fast and far, so a friend across a field can read your flashes, even at night."}},
        {"type": "trace", "title": "Message strip", "structure": "tape", "instruction": "Trace the strip where we'll write the message.",
         "note": {"text": "Writing the pattern down lets you check it, send it again, or decode it later."}},
        {"type": "trace", "title": "Letter O", "structure": "letterO", "instruction": "Draw three dashes: that's the letter O.",
         "note": {"text": "In Morse code, O is dash, dash, dash. Every letter has its own pattern of dots and dashes.",
                  "remember": "O = − − −"}},
        {"type": "trace", "title": "Letter K", "structure": "letterK", "instruction": "Draw dash, dot, dash: the letter K. Dab the dot.",
         "note": {"text": "K is dash, dot, dash. A longer gap between letters, as long as three dots, shows where one letter ends.",
                  "remember": "Gaps separate letters."}},
        {"type": "choice", "title": "Decode", "instruction": "Read your message.", "showsDiagram": True,
         "question": "O is − − − and K is − · −. What does your strip say?",
         "options": [
             {"text": "OK", "correct": True, "feedback": "Yes! Patterns of short and long signals can carry any message, letter by letter."},
             {"text": "KO", "feedback": "Read left to right: first − − − (O), then − · − (K)."},
             {"text": "OO", "feedback": "The second letter has a dot in the middle: − · − is K."},
             {"text": "SOS", "feedback": "There are only two letters here, made of dashes and one dot: O and K."}]},
        {"type": "choice", "title": "Compare solutions", "instruction": "Think like an engineer.", "showsDiagram": False,
         "question": "You need to send a message to a friend across a big, dark field at night. Which way works best?",
         "options": [
             {"text": "Flash a flashlight in code", "correct": True,
              "feedback": "Yes. Light can be seen from far away in the dark, and the code carries the message."},
             {"text": "Whisper the message", "feedback": "A whisper won't carry across a big field. A flashing light can be seen from far away."},
             {"text": "Wave a note in the air", "feedback": "Your friend couldn't read it in the dark. Flashes of light show up at night."},
             {"text": "Tap a pattern on the ground", "feedback": "Taps won't carry across a whole field. Light flashes travel much farther."}]},
        {"type": "choice", "title": "Patterns", "instruction": "Why do the gaps matter?", "showsDiagram": True,
         "question": "Why does Morse code leave a longer gap between letters?",
         "options": [
             {"text": "So you can tell where one letter ends and the next begins", "correct": True,
              "feedback": "Right. Without the gaps, − − − − · − would be hard to split into O and K. The pattern needs to be clear."},
             {"text": "To give the flashlight a rest", "feedback": "The gaps are part of the pattern: they mark where each letter ends."},
             {"text": "Gaps don't matter", "feedback": "They do: without them you couldn't tell where one letter stops and the next starts."},
             {"text": "To make the message longer", "feedback": "The gap isn't padding: it shows where one letter ends."}]},
    ],
}

for lesson in (circuit, turbine, wave, light, code):
    save(lesson)
