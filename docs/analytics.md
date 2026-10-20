# Analytics (PostHog)

Set up in `Diagrama/App/Analytics.swift`. The project token and host come from
`Config/Secrets.xcconfig` (never committed; copy `Secrets.example.xcconfig`). Without it, the
app runs with analytics off. Nothing is sent during unit or UI tests, or when the debug launch
arguments `-openLesson`, `-autodraw` or `-step` are used. Launch with the environment
variable `POSTHOG_DEBUG=1` to log every event the SDK queues and sends.

**Privacy.** Learners can be children (lessons start at grade 3). So: no person profiles
(nobody is identified), no autocaptured taps or screens, no session replay, and nothing the
learner types is sent (search text and diagram requests stay on the device). Review with
counsel before launch, alongside COPPA (see `experience-rules.md`, "Still open").

## Screens
`Learn` (grade_band), `Lesson`, `Results`, `Gallery` (drawings), `Gallery drawing` (lesson_id).

## Events
While a lesson is open, every event also carries: lesson_id, lesson_title, grade, grade_band,
subject, standard, step_index, step_type, step_title.

| Event | When | Properties |
|---|---|---|
| grade band selected | Grade picker changed | grade_band |
| search found nothing | A search has no lessons | query_length |
| diagram requested | "Request this diagram" tapped | |
| lesson opened | Lesson card tapped | lesson fields, from (browse/search) |
| lesson started | Lesson screen shown | steps |
| step completed | Continue on any step | |
| drawing step completed | A tracing step passes | match (/1000), smoothness (/300), first_try |
| drawing tool used | Eraser on, undo, restart step | tool |
| science check answered | First answer to a question, find-it or color task | correct_first_try, topic |
| drawing checked | Check on Copy it / Draw from memory | mode, passed, attempt, peeked, missing_parts, stray_lines, coverage, precision |
| peeked at picture | Peek during Draw from memory | |
| color legend opened | Color legend opened | |
| lesson closed | ✕ tapped | finished, progress (0 to 1) |
| lesson completed | Last step finished | match, smoothness, first_try, science_correct, science_total, duration_seconds, drew_from_memory |

The SDK also sends Application Installed, Opened and Backgrounded.
