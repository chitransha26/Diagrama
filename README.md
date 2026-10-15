# Forma

Scientific diagram learning app for iPhone and iPad (SwiftUI + PencilKit),
based on the *Forma Scientific Diagram Platform PRD* v1.2.

## First version scope
- Lessons: plant cell, leaf transverse section, water (H₂O) Lewis structure
- Step-by-step guided drawing with two separate scores:
  drawing execution and scientific correctness (PRD §05)
- Chemistry checked as atoms and bonds, not pixels (PRD §18)
- Personal gallery and saved progress
- Email sign-in and progress sync via Supabase; users 13+ only until the
  COPPA review (PRD §12) is complete

## Setup
1. Install Xcode, then run
   `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`
2. Copy `Config/Secrets.example.xcconfig` to `Config/Secrets.xcconfig`
   and fill in your Supabase URL and anon key.
