# Diagrama experience rules

The user experience every diagram lesson must follow. Agreed with the product owner,
16 October 2026. Rules marked **(enforced)** are checked by automated tests or built into
the app, so a lesson can't break them; the rest need checking by hand when authoring.

## Lesson flow
1. **Draw the parts, in order.** Outlines first, then inner details. Learners draw
   everything themselves, including every copy of a part (all four chloroplasts, both
   guard cells). The app never draws or fills anything for them.
2. **Find-it steps** for important parts that can't be drawn (the cytoplasm, a leaf's air
   spaces): tap the part in your own drawing; wrong taps are explained.
3. **Color stage.** The app picks the color and names the part ("Fill the chloroplasts");
   the learner finds and taps every piece of it. Colors are scientifically accurate.
4. **Questions:** labeling, quizzes and ordering, with every wrong answer explained.
5. **Copy it:** the finished diagram (real colors) above, a blank space below to recreate it.
   **(enforced)**
6. **Draw from memory:** a separate screen without the picture. Peek is allowed after a
   first try. **(enforced)**
7. **Results:** Match /1000, Smoothness /300, First try /50, Time, plus a separate Science
   score; a "Your notes" study sheet; the drawing is saved to the gallery.

## The drawing screen
- **One place to read: under the canvas.** The instruction, then progress hints, then the
  note card. Drawing steps show no title or instruction above the canvas.
- **A name tag on the canvas**, beside the part being drawn, kept clear of the start dot.
- **The app picks the pen** for each part (fine liner 2 pt, pen 3.5 pt, bold pen 6.5 pt,
  fixed on screen at every zoom). Learners never choose tools.
- **Toolbar:** the pen in use, eraser, undo, and ⋯ › Restart step. No layer controls:
  each step and each zoomed piece is its own hidden layer.
- **Eraser** rubs out only what it touches, and the pen comes back automatically when
  you lift.
- **Feedback while drawing:** a demo stroke from a blue start dot; a progress bar (green on
  the guide, red off it); red rings where the line strays; blue marks on parts still
  untraced; a restart prompt when most of the line is off the guide.
- **Note card** pops up when a part is finished: its name, what it does and how it helps,
  and a 💡 tip to remember it. At most 180 characters, so it fits. **(enforced)**
- **Automatic zoom** into any part too small for a finger, with nearby small parts sharing
  a view and an "x of N" counter. **(enforced)**
- **Nothing moves:** the canvas never shifts or resizes during a step, and toolbar buttons
  always respond, zoomed or not.

## Tracing rules (how strict)
- A part is complete only when **every** piece of it is traced (96%+), with no untraced gap
  wider than a pen line. **(enforced)**
- Ink only counts for a part if it **runs along** it, and only for the nearest part, so
  ink near an arrow's tip can't complete its arrowhead. **(enforced)**
- **Tolerance is fixed on screen:** 10 pt for a finger, 6 pt for Apple Pencil, at every
  zoom. Sharp corners (tail tips, arrow points) get twice the leeway, because hands and
  stroke smoothing round them off. **(enforced)**
- **Dots are dabbed, not traced** (eyes, embryos, seeds, lone-pair electrons); a dab only
  fills its own dot. **(enforced)**
- **Every part must be big enough to trace** on a small iPhone: closed shapes 24 pt,
  strokes 14 pt, after zoom. **(enforced)**
- **Copy and memory drawings** are judged on overall shapes and layout, at any size and
  position, not on tiny details. Two-finger pinch zooms; one finger draws. After three
  tries the learner can move on.

## Science and content
- **Colors mean something real.** Each lesson declares Microscope colors (a fresh,
  unstained sample), Real colors (simplified, as seen by eye) or Ink only (no real color),
  and the legend explains each color. Clear parts stay unfilled.
- **Notes are accurate and teach function**: what the part is, what it does, how it helps.
  Every drawn part has one. **(enforced)**
- **Chemistry is drawn like on paper:** trace the printed element letters (no handwriting),
  draw bonds as lines and lone pairs as dots; graded by the bond structure, not the picture.
- **Words on the page** (axis labels, N/S poles) are printed, never answers to a question.
- **Every fact is checked against an authoritative source** (OpenStax, NGSS, NOAA, NPS,
  university extension services, peer-reviewed work), and every lesson cites its NGSS (or AP)
  standard and its sources, shown in the lesson's info panel. Links are checked to be real;
  a source is never guessed. **(enforced)**
- **Every lesson must match its standard**, not just its topic (e.g. 3-LS3-1 needs both
  inheritance and variation).
- Teacher or scientist review is a later, pre-launch step (PRD §09).

## Curriculum
- NGSS for grades 3–12, plus AP Biology and AP Chemistry; mapped in `curriculum/coverage.csv`.
- Browse by grade band: Grades 3–5, Middle school, High school. K–2 is deferred until
  read-aloud audio exists.

## How changes ship
- Built and checked on a spare simulator; installed on the product owner's simulator only
  after telling them (installing restarts the app); pushed to GitHub only after they've
  tried it and approved.

## Still open
- **A content notice** for legal protection, such as "Content is checked against [sources].
  Spot a mistake? Report it." plus terms of service. A lawyer should review the wording;
  "not intended for educational use" is not recommended for an education app.
- A **Watch** button to replay the demo stroke (it currently plays once at the start).
- A **targeted hint after repeated mistakes** (PRD §04).
- **Read-aloud audio**, needed before K–2.
- Whether the from-memory step should cover the whole diagram or only key parts for
  younger grades.
