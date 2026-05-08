# Universal Compass Footer Contract

The universal footer is the shared trust and navigation layer for public Compass pages.

## Required Surfaces

- Compass Suite home
- Compass Suite 404
- Compass Suite About page
- Compass Suite License page
- Critical Compass public page
- Prompt Compass public page
- UX Heuristics Compass public page
- What Is an MCP support page
- Future public Compass and support pages

## Link Scope

Footer product links include only public, downloadable Compasses:

- Critical Compass
- Prompt Compass
- UX Heuristics Compass

Alpha and future Compasses remain discoverable from Compass Suite, not from the footer.

## Required Footer Content

- `Compass Suite is created and maintained by Jonathan Kyle Hobson.`
- Network purpose line
- Link groups: `Start Here`, `Public Compasses`, `Trust & Attribution`
- Links to Compass Suite, Install Guide, MCP Basics, Critical Compass, Prompt Compass, UX Heuristics Compass, About the Author, License & Attribution, and LinkedIn
- Copyright/license line:
  `© 2026 Jonathan Kyle Hobson. Code AGPL-3.0-only; docs, prompts, skills, and methodology CC BY-SA 4.0 unless otherwise noted. Compass names, logos, author photo, and official trade dress reserved.`

## Accessibility And Behavior

- Use `<footer class="suite-footer" role="contentinfo">`.
- Use `<nav aria-label="Compass network footer">`.
- Internal Compass network links open in the same tab.
- External links use `target="_blank" rel="noopener"`.
- Footer links must remain at least 44px tall on small screens and must not cause horizontal scrolling.

## Legal Source Of Truth

The footer must match the Compass legal imprint kit:

- Code: `AGPL-3.0-only`
- Docs, prompts, skills, rubrics, checklists, examples, and public methodology text: `CC BY-SA 4.0`
- Names, logos, author photo, and creator identity: reserved brand assets

The public License page explains the terms in plain language, but included license files remain authoritative.
