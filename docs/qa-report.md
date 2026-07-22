# Working Tools release QA

Date: 2026-07-22

## Design Taste Gate

- Mode: Design Taste Gate
- Surface: public brand directory and working-library hub
- Audience: people choosing, inspecting, or installing one of Jonathan Kyle
  Hobson's public tools; collaborators who need to understand the larger system
- Register: editorial field manual with a functional catalog
- Control dials: variance 7/10; motion 2/10; density 6/10; trust 9/10
- Reference source: Humanizer's paper/ink/vermilion system and the Participatory
  Defense field guide's task-led headings, hard rules, and signal yellow
- Verdict: Ready to ship

The gate found two implementation issues and one accessibility issue during the
first pass. All were fixed and rechecked:

1. The hero image retained its HTML height after CSS width scaling, making the
   first section 1,883 px tall. `height: auto` now preserves the intended ratio;
   the final desktop hero is 1,058 px tall and the primary message is visible.
2. Async catalog rendering displaced direct `#install` links. The catalog now
   corrects the initial hash after its first render; mobile verification places
   the install section 16 px from the viewport top.
3. Axe found three contrast failures and one unsupported ARIA label. Dark-surface
   eyebrows now use a lighter vermilion, the vermilion button uses ink text, and
   the library controls use a named `search` landmark.

## Visual anchor map

| ID | Source / viewport | Region / selector | Observation | Action | Final verification |
| --- | --- | --- | --- | --- | --- |
| A1 | `output/playwright/final-desktop-1440-viewport.png`, 1440×1000 | hero / `h1`, `.hero-figure` | task-first identity and generated artwork share the first scan | preserve asymmetry; correct image scaling | headline, lede, actions, and artwork visible; no horizontal overflow |
| A2 | `output/playwright/working-tools-task-index-final.png`, 1440×1000 | work index / `.task-grid` | seven jobs need one deliberate strip | use seven columns on wide screens and collapse responsively | seven equal task lanes; each link filters the catalog |
| A3 | `output/playwright/final-desktop-1440-full.png`, 1440 wide | library / `.library-row` | 36 records need density without equal-card clutter | editorial rows, access labels, progressive detail | all records render; public/local/connected/preview differences remain visible |
| M1 | `output/playwright/final-mobile-390-viewport.png`, 390×844 | header and hero | navigation and large display type must stay intentional | mobile menu; stacked actions; cropped art below copy | no horizontal overflow; menu and first actions visible |
| M2 | `output/playwright/final-mobile-390-install.png`, 390×844 | `#install` | shared deep link shifted before catalog settled | post-render anchor correction | final top offset 16 px; all three disclosure rows visible |
| N1 | desktop and mobile hero screenshots | generated editorial artwork | atmosphere must not impersonate evidence | label as generated; keep install screenshots separate | caption present; alt text specific; natural width 1023 px loaded |
| L1 | `output/playwright/working-tools-404-desktop-fixed.png`, 1280×800 | 404 shell | GitHub project-root asset paths must survive recovery routing | project-absolute CSS and mark paths | styled 404; no console warnings; no overflow |

The `output/playwright/` evidence directory is local QA output and is excluded
from the public repository.

## Interaction and responsive checks

- Viewports: 1440×1000, 1024×768, and 390×844.
- Mobile navigation: closed by default; exposes `Close` and primary links after
  activation; returns to closed state after a navigation link.
- Task filter: `Write & revise` changed the library from 36 records to 18.
- Search: matched `Figma`; a deliberately absent query produced the specific
  empty state; clearing restored the library.
- Compass details: Critical Compass revealed five HTTPS downloads with recorded
  SHA-256 values.
- Install details: the Claude plugin disclosure revealed the steps and three
  documentary screenshots.
- Layout: `scrollWidth` equaled `clientWidth` at all tested viewports.
- Console: zero page errors and zero warnings before the test-only Axe injection.

## Accessibility checks

Axe 4.10.3 was injected only into the local QA browser and run against WCAG 2 A,
AA, 2.1 A, and 2.1 AA tags:

- Homepage: 0 violations, 28 passes. Two caption-contrast checks were marked
  incomplete because a decorative pseudo-element obscured background detection;
  manual calculation is 5.71:1 (`#625d54` on `#f4efe6`).
- About: 0 violations, 17 passes, 0 incomplete.
- License: 0 violations, 18 passes, 0 incomplete.
- 404: 0 violations, 16 passes, 0 incomplete.

Keyboard-focus styling, skip links, landmarks, named controls, reduced-motion
behavior, non-color access labels, descriptive image alternatives, and 48 px
primary touch targets are present in the shipped source.

## Content and link checks

- Humanizer lint: only informational cues for intentional three-part phrasing,
  curly quotes, and Markdown emphasis; no citation cues or unsupported claims.
- Static validator: pass.
- Public destination validator: 39 unique HTTPS destinations returned success,
  including all 20 preserved Compass release assets.
- `git diff --check`: pass.
