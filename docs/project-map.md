# Working Tools project map

## Current slice

This repository publishes the public directory formerly presented as the
Compass Suite storefront. The redesign keeps the existing Compass product
content and verified release links, but the visitor-facing brand is now
**Working Tools by J. Kyle Hobson**.

The homepage has one job: help a visitor find the right public tool, collection,
field guide, or local system for the work in front of them.

## Entrypoints

- `index.html`: semantic page shell and the no-JavaScript version of the core
  message.
- `assets/js/main.js`: starts the catalog, filters, navigation, copy buttons,
  and progressive disclosure.
- `assets/css/main.css`: imports the design tokens and layout layers.
- `suite-manifest.json`: verified Compass product status, release URLs,
  checksums, and safety gates. It remains the authority for Compass downloads.
- `data/tool-library.json`: public-facing directory of collections, field
  guides, public tools, connected services, and local-only systems.

## Ownership boundaries

```text
assets/
  css/                 Visual tokens, base rules, layout, components, responsive rules
  generated/           Generated atmosphere/identity assets and derivatives
  install-guide/       Real screenshots that document tested install paths
  js/                  Small browser modules; no framework or build step
content/
  site-copy.md         Editorial source for the public page copy
data/
  tool-library.json    Curated public-safe tool catalog
docs/
  design-direction.md  Visual thesis, anchor map, and QA target
  asset-manifest.md    Asset purpose, source status, crop, alt text, and verification
  qa-report.md         Release evidence, fixed findings, accessibility, and visual anchors
scripts/
  validate_suite_site.py  Static, content, privacy, and structural checks
suite-manifest.json    Compass release/download authority
```

## Core concepts

- **Working Tool**: one public artifact or local system with a bounded job.
- **Collection**: a group of related skills or plugins distributed together.
- **Field Guide**: a public, task-specific resource with prompts, guardrails,
  and source-aware instructions.
- **Public download**: a verified artifact with a public destination.
- **Local-only system**: a tool used in Jonathan's private workflow. The site
  may name its role but must not expose paths, credentials, configuration, or a
  download CTA.
- **Connected service**: an external service reached through an installed
  connector or plugin. Availability depends on the user's own account and host.

## Data flow

1. `main.js` loads `data/tool-library.json` and `suite-manifest.json`.
2. The catalog module normalizes both sources into searchable records.
3. Visitors filter by job or surface. Public tools expose verified destinations;
   local-only systems expose description only.
4. Install directions use the preserved screenshots under
   `assets/install-guide/` and remain behind native disclosure controls.

## Change paths

- New Compass release: update `suite-manifest.json`, then run the validator.
- New public collection or field guide: update `data/tool-library.json`.
- New visual asset: add it under `assets/generated/` or the appropriate evidence
  folder and update `docs/asset-manifest.md`.
- Copy revision: update `content/site-copy.md` first, then the matching HTML or
  catalog record.
- Brand or layout change: update the relevant CSS layer; do not add one-off
  visual literals to HTML or JavaScript.

## Onboarding packet

- First files to read: `docs/design-direction.md`, `content/site-copy.md`,
  `index.html`, `assets/css/tokens.css`, `assets/js/main.js`.
- Runtime: `python3 -m http.server 8787`.
- Safe checks: `python3 scripts/validate_suite_site.py` and the browser QA
  commands recorded in the release notes.
- Risky changes: release URLs, checksums, local/private system descriptions,
  license copy, and public deployment.
- Common failure: duplicating release facts in HTML instead of reading the
  manifest.
