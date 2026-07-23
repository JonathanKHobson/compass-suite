# Working Tools design direction

## Design harness

- **Surface:** public brand hub, portfolio directory, and install gateway.
- **Audience:** people using Claude or Codex who need a concrete tool for a
  writing, research, design, building, career, or table-facing task.
- **Visual thesis:** an editor's working table on warm paper: black rules,
  serif display type, plain sans-serif controls, and vermilion corrections.
- **Content thesis:** within five seconds, a visitor should understand that this
  is Jonathan's working library and know how to choose a tool by task.
- **Dominant idea:** a task index leads into a filterable library. The page feels
  assembled from useful working notes, not a row of product cards.
- **Reference source:** the Humanizer ChatGPT Site supplies paper, ink,
  vermilion, editorial type, and honest proof language. The Participatory
  Defense Field Guide supplies hard borders, numbered navigation, and
  task-first sections. Its electric lime is intentionally not reused.

## Control dials

- **Variance:** 7/10. Strong editorial composition, but repeated library rows
  share a disciplined system.
- **Motion:** 2/10. Only filter, focus, menu, and disclosure feedback. Reduced
  motion is fully respected.
- **Density:** 6/10. The first screen is calm; the library can carry a large
  inventory through search, filters, and native details.
- **Trust:** 9/10. Every listing has a working public resource. Private and
  unfinished systems are omitted instead of appearing as dead-end inventory.

## Token intent

- Paper: `#f4efe6`
- Ink: `#171512`
- Muted ink: `#625d54`
- Rule: `#bdb3a4`
- Vermilion: `#d95d3a`
- Vermilion dark: `#94331f`
- Signal wash: `#efd8ce`
- Night: `#20211e`
- Display: Iowan/Palatino/Georgia serif stack
- Body: Avenir Next/Segoe UI/system sans stack
- Code and metadata: SFMono/Consolas monospace stack

## Generic-risk list

- No centered hero plus three equal cards.
- No purple/blue glow, glass panels, abstract orbit graphics, or floating pills.
- No icon tile above every heading.
- No repeated “learn more” CTAs when the destination can be named.
- No download wall before the visitor knows which tool fits.
- No private MCP or account-bound connector presented as a catalog item.
- No old compass badge, directional needle, starburst, or navigation metaphor.

## Visual anchor map

| ID | Source | Region / ref | Observation | Asset role | Action | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Current live Compass Suite | First viewport / `.hero` | Old badge and “Choose the right Compass” make the retired metaphor the main idea | identity | Replace with typographic Working Tools wordmark and task-first headline | desktop and mobile screenshots |
| A2 | Current live Compass Suite | Below hero / tab interface | Tabs hide the product context and make the page feel like an app shell | interface | Replace with ordinary anchored sections and a sticky task index | keyboard and mobile QA |
| A3 | Current live Compass Suite | Product grid | Every product carries the same visual weight and repeats download choices | interface | Use editorial library rows, explicit status, and progressive disclosure | long-content desktop/mobile QA |
| A4 | Current repo | `assets/install-guide/**` | Real install screenshots are useful evidence but currently dominate a long guide | evidence | Keep screenshots behind format-specific disclosure controls | image-load and alt-text QA |
| R1 | Humanizer ChatGPT Site | Hero and revision window | Warm editorial system is distinctive, legible, and grounded in a real before/after | reference | Reuse its material language, not its exact layout | token and typography review |
| R2 | Participatory Defense Field Guide | Hero safety rail and numbered sections | Hard rules and numbered sections create urgency without visual effects | reference | Reuse border logic; translate the conflicting lime into a warm signal wash | Design Taste Gate |
| N1 | New Working Tools hero | Right-side working-note specimen | Needs to help a visitor use the library, not add atmosphere | interface | Show the three-step choose/open/check loop as a semantic specimen | desktop/mobile screenshots and text clipping check |

## First-order UX rules

- A skip link and landmark structure are mandatory.
- Search and filter controls keep visible labels.
- Results announce the count through a polite live region.
- Native links, buttons, and details elements carry interaction.
- Touch targets are at least 44px.
- The library works without animation and remains readable without JavaScript.
- On load or data failure, the core HTML still explains the library and links to
  Humanizer, the public Compasses, and the field guides.
