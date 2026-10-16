# ArtWorkout: how the experience works

Research notes, 15 October 2026. ArtWorkout is the PRD's primary experience reference
(PRD §01). Sources are listed at the end. Most are the developer's own pages, the App
Store listing and reviews; no source describes every control, so a few points are marked
as unconfirmed.

## Lesson structure
- A drawing is split into **stages: lines → shapes → details → color**
  ("basic lines and proportions", "shapes and details", "finished drawing in color").
- Each lesson has **10–30 small steps**. Each step is one layer and one clear action
  ("one clear action at a time, which reduces cognitive load").
- **The app sets the brush, color and zoom for each layer.** The learner doesn't pick
  tools during a guided step. A brush picker and size slider exist, mainly for free drawing.
- Setting: **advance automatically** to the next layer when a step is done.
- **Left-handed mode.**
- The first lesson starts with overdrawing basic shapes and step-by-step help with the tools.

## Drawing and feedback
- You **trace outlines** over a template; there's no finished picture to copy.
- **A progress bar fills with each stroke: green for accurate parts, red for inaccurate ones.**
- Each stroke is compared with its target line on **distance, angle and curvature**.
- **If the inaccurate parts outweigh the accurate ones, the app asks you to restart the step.**
- **Undo** is the arrow in the top-left; **Restart step** is in the menu.
- **There is an eraser** (confirmed by the product owner, who has used the app). One App
  Store reviewer asks for the eraser "during every step", and another says cleanup and
  layer tools appear mainly in the final step, so it may be limited during guided tracing.
  To confirm.
- **Layers:** ArtWorkout creates a layer for each step automatically; learners don't set
  them up (confirmed by the product owner). Layer management suits an illustration app,
  but **Diagrama won't expose layers**: each step's strokes are kept apart internally so
  a step can be scored or restarted on its own.
- **Brushes are similar to Procreate's** (confirmed by the product owner): a library of
  textured brushes with pressure on Apple Pencil, not a single round pen.
- "Magnetic guidance" pulls strokes toward the template (added in 1.14.11).
- Hints highlight which parts to focus on, and explain why.

## Color
- Color is the last stage. A **fill tool** ("smart fill" / "lasso fill") fills an area and
  stays inside the lines. The app sets the color for each layer.
- Color-mixing lessons exist.

## End of lesson
- A scorecard with four scores: **Match** (e.g. 975/1000), **Smoothness** (272/300),
  **First try** (50/50) and **Time** (04:01).
- Asks whether to save; the drawing goes to a **gallery**. A share-able result screen.

## Habit, progression and social
- **Lesson of the Day**, a **streak calendar**, **daily goals**, **achievements**, usernames.
- Categories work as levels, with a circular progress meter.
- Daily free **energy** unlocks lessons; PRO subscription removes limits and ads.
- **Multiplayer:** invite a friend in one tap, draw together on a shared canvas in real
  time, race through the same guided lesson side by side, draw over a recorded session,
  and "Chameleon" (a hide-and-seek mode).
- Founder's stance: AI helps make lessons behind the scenes, never does the drawing.

## What this means for Diagrama
| ArtWorkout | Diagrama |
|---|---|
| Stages: lines → shapes → details → color | Outlines → inner details (palisade cells, thylakoids, xylem) → color, then labels and explanation |
| App sets brush, color and zoom per step; Procreate-like brushes | Procreate-like brush set (PencilKit has fine liner, pen, marker, pencil, crayon, watercolor, fountain pen); brush per structure; zoom in on small parts |
| Green/red progress bar per stroke | Same, replacing the two percentages |
| Restart prompt when mistakes outweigh accuracy | Same |
| Undo, restart step, eraser; layers added automatically | Undo, restart step, eraser (scope to confirm); no layer UI, steps kept apart internally |
| Magnetic guidance | Conflicts with PRD §11: never grade a stroke the app has changed without saying so. If added, it must be disclosed and recorded |
| Fill tool, color set by the app | App picks the color and names the part; the learner finds and fills it |
| Match / Smoothness / First try / Time | Same, plus a separate Science score (PRD §05) |
| Lesson of the Day, streaks, goals | Same |
| Multiplayer race and shared canvas | Invite-only rooms (PRD §08), after accounts and sync |

## Sources
- App Store listing: https://apps.apple.com/us/app/artworkout-learn-how-to-draw/id1564657118
- ArtWorkout method: https://artworkout.app/method/
- iGeeksBlog review: https://www.igeeksblog.com/artworkout-drawing-app-for-ipad/
- Beebom review: https://beebom.com/artworkout-ipad-drawing-app/
- VentureBeat: https://venturebeat.com/business/how-artworkout-is-working-on-the-future-of-creativity-through-its-learn-to
- Inverse: https://www.inverse.com/tech/how-5-minute-learn-how-to-draw-artworkout-app-uses-micro-learning-to-make-creativity-easier
- Digital Trends (via search summary): https://www.digitaltrends.com/contributor-content/meet-the-artworkout-app-the-personal-trainer-for-learning-how-to-draw/
