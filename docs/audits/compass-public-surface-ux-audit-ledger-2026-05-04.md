# Compass Public Surface UX Audit Ledger - 2026-05-04

This ledger closes the cross-site UX audit pass for the currently live Compass public family:

- Compass Suite: `https://jonathankhobson.github.io/compass-suite/`
- Critical Compass: `https://jonathankhobson.github.io/critical-compass/`
- Prompt Compass: `https://jonathankhobson.github.io/prompt-compass/`
- UX Heuristics Compass: `https://jonathankhobson.github.io/ux-heuristic-compass/`
- What Is an MCP: `https://jonathankhobson.github.io/what-is-an-mcp/`

## Source Reports

- `/Users/jonathanhobson/Desktop/compass-suite-ux-audit.md`
- `/Volumes/KyleSSD/ux-heuristic-compass/reports/compass-suite-2026-05-04/compass-suite-uxhc-advanced-audit.md`
- `/Volumes/KyleSSD/ux-heuristic-compass/reports/compass-suite-2026-05-04/compass-suite-uxhc-desktop-audit.md`

## Status Definitions

- `fixed_live`: fixed or verified on the public Pages surface.
- `partially_fixed`: user-facing surface is improved, but a deeper generator, process, or future-source cleanup remains.
- `needs_patch`: accepted into the current lane but not fixed yet.
- `defer_backlog`: valid but intentionally outside this Pages/content closeout.
- `not_applicable`: not a live public-surface defect, already satisfied, or not appropriate for this site family.

## Closeout Summary

| Area | Status | What Changed |
| --- | --- | --- |
| Mobile horizontal overflow and clipped controls | `fixed_live` | All five pages use shared containment rules, wrapped labels, mobile-safe buttons, and stacked mobile tabs where applicable. |
| Install-choice clarity | `fixed_live` | Suite plus Critical, Prompt, and UXHC now include a plain-language chooser near download decisions. |
| Download jargon and CTA hierarchy | `fixed_live` | Product pages use `Claude Code / Cowork Plugin`, `Claude Desktop Extension`, and `Download and Open Guide` for primary installs. |
| Point-of-need MCP literacy | `fixed_live` | Product pages and Suite expose `MCP Basics` near install/download decisions; FAQ links remain available. |
| Copy/download feedback | `fixed_live` | Copy buttons already confirm `Copied`; product install downloads now announce `Download started. Guide opened.` |
| MCP explainer navigation/recovery | `fixed_live` | What Is an MCP keeps `Back to Compass Suite`, adds recovery links to all three live Compass products, and gains mobile/focus containment. |
| Upstream generator parity | `partially_fixed` | Public Pages outputs are patched and published. Full release-builder/template hardening remains a follow-up before the next package rebuild. |
| Separate mobile-only view | `defer_backlog` | Current shared responsive pattern passes the closeout criteria. A separate mobile fork is deferred unless future testing proves it is necessary. |
| Full What Is an MCP redesign | `defer_backlog` | The support page was contained and given recovery links; a larger educational redesign is outside this closeout. |
| Alpha signup/notification flows | `defer_backlog` | Locked alpha cards remain non-dead-end but do not collect signups. |
| Package/release asset rebuilds | `not_applicable` | This is a Pages/content pass only. Existing release URLs and checksums remain unchanged. |

## Detailed Issue Mapping

| Audit Theme | Checklist Items | Status | Closeout Decision |
| --- | --- | --- | --- |
| H01 Visibility and feedback | `h01_d_02`, `h01_d_04`, `h01_d_07`, `h01_m_02`, `h01_m_04`, `h01_m_07` | `fixed_live` | Copy/download feedback is visible; install actions explain that the guide opened. |
| H02 Real-world match | `h02_d_01`, `h02_d_03`, `h02_m_01`, `h02_m_03` | `fixed_live` | Download choices now start from the user's host app instead of raw package jargon. |
| H03 Control and recovery | `h03_d_01`, `h03_d_02`, `h03_d_05`, `h03_m_01`, `h03_m_02`, `h03_m_05` | `fixed_live` | Product pages include `Back to Compass Suite`; MCP explainer adds recovery links. |
| H04 Consistency and containment | `h04_d_01`, `h04_d_02`, `h04_d_03`, `h04_d_05`, `h04_d_06`, `h04_d_11`, `h04_d_13`, `h04_d_14`, `h04_d_18`, `h04_d_20`, `h04_d_21`, `h04_m_01`, `h04_m_02`, `h04_m_03`, `h04_m_05`, `h04_m_06`, `h04_m_11`, `h04_m_13`, `h04_m_14`, `h04_m_18`, `h04_m_20`, `h04_m_21` | `fixed_live` | Product and support pages share labels, button hierarchy, wrapping, and mobile containment. |
| H05 Error prevention | `h05_d_02`, `h05_d_04`, `h05_d_05`, `h05_m_02`, `h05_m_04`, `h05_m_05` | `fixed_live` | Chooser and prerequisites reduce wrong-package selection before download. |
| H06 Recognition over recall | `h06_d_02`, `h06_d_04`, `h06_m_02`, `h06_m_04` | `fixed_live` | The correct file type is shown at the point of decision rather than only in FAQ/install docs. |
| H07 Efficiency | `h07_d_01`, `h07_d_02`, `h07_d_04`, `h07_d_05`, `h07_m_01`, `h07_m_02`, `h07_m_04`, `h07_m_05` | `fixed_live` | Returning users still have direct links; first-time users get a chooser before the cards. |
| H08 Visual hierarchy | `h08_d_01`, `h08_d_02`, `h08_d_03`, `h08_d_06`, `h08_d_10`, `h08_d_12`, `h08_d_13`, `h08_d_16`, `h08_m_01`, `h08_m_02`, `h08_m_03`, `h08_m_06`, `h08_m_10`, `h08_m_12`, `h08_m_13`, `h08_m_16` | `fixed_live` | Primary install actions are visually consistent; secondary actions are quieter. |
| H09 Recovery | `h09_d_01`, `h09_d_02`, `h09_m_01`, `h09_m_02` | `fixed_live` | Suite has a custom 404; MCP support page has cross-site recovery links. |
| H10 Help and docs | `h10_d_01`, `h10_d_04`, `h10_d_05`, `h10_m_01`, `h10_m_04`, `h10_m_05` | `fixed_live` | MCP Basics moved closer to install decisions and remains linked from FAQ/support content. |
| H11 Accessibility | `h11_d_01`, `h11_d_02`, `h11_d_03`, `h11_d_04`, `h11_m_01`, `h11_m_02`, `h11_m_03`, `h11_m_04` | `fixed_live` | Focus states, touch-target minimums, wrapping, alt text preservation, and no-overflow checks are part of validation. |
| H12 Inclusion | `h12_d_01`, `h12_d_03`, `h12_d_04`, `h12_d_05`, `h12_d_06`, `h12_m_01`, `h12_m_03`, `h12_m_04`, `h12_m_05`, `h12_m_06` | `fixed_live` | Beginner-safe language and point-of-need MCP help reduce assumed technical knowledge. |
| H13 Journey | `h13_d_02`, `h13_d_03`, `h13_d_04`, `h13_d_06`, `h13_m_02`, `h13_m_03`, `h13_m_04`, `h13_m_06` | `fixed_live` | CTAs now tell users that the guide opens after download, making the next step clearer. |
| H14 UX writing | `h14_d_01`, `h14_d_03`, `h14_d_04`, `h14_d_05`, `h14_d_06`, `h14_d_07`, `h14_m_01`, `h14_m_03`, `h14_m_04`, `h14_m_05`, `h14_m_06`, `h14_m_07` | `fixed_live` | Labels are shorter, more conversational, and consistent across live public pages. |
| Low/no-defect checklist items | All desktop IDs and mobile IDs not listed in the rows above | `not_applicable` | The audits include the full 204-item checklist. Items not named above were either already passing, not observed as public-surface defects, or not suited to this Pages-only closeout. |
| Release-builder/template parity | Cross-site generated-page contract | `partially_fixed` | Pages outputs are fixed now; future product-package builders still need an explicit parity gate before the next artifact rebuild. |
| Full educational IA redesign for What Is an MCP | Support-page IA | `defer_backlog` | Preserve current educational structure in this pass. |
| Signup/waitlist for alpha Compass cards | Alpha product journey | `defer_backlog` | Do not add data collection without a real workflow and privacy copy. |
| New examples, product docs, or release packages | Product content and artifacts | `defer_backlog` | Out of scope for this public-page closeout. |

## Full Checklist ID Index

Desktop IDs covered by this ledger:

`h01_d_01`, `h01_d_02`, `h01_d_03`, `h01_d_04`, `h01_d_05`, `h01_d_06`, `h01_d_07`, `h01_d_08`, `h01_d_09`, `h02_d_01`, `h02_d_02`, `h02_d_03`, `h03_d_01`, `h03_d_02`, `h03_d_03`, `h03_d_04`, `h03_d_05`, `h04_d_01`, `h04_d_02`, `h04_d_03`, `h04_d_04`, `h04_d_05`, `h04_d_06`, `h04_d_07`, `h04_d_08`, `h04_d_09`, `h04_d_10`, `h04_d_11`, `h04_d_12`, `h04_d_13`, `h04_d_14`, `h04_d_15`, `h04_d_16`, `h04_d_17`, `h04_d_18`, `h04_d_19`, `h04_d_20`, `h04_d_21`, `h05_d_01`, `h05_d_02`, `h05_d_03`, `h05_d_04`, `h05_d_05`, `h06_d_01`, `h06_d_02`, `h06_d_03`, `h06_d_04`, `h07_d_01`, `h07_d_02`, `h07_d_03`, `h07_d_04`, `h07_d_05`, `h07_d_06`, `h07_d_07`, `h07_d_08`, `h07_d_09`, `h08_d_01`, `h08_d_02`, `h08_d_03`, `h08_d_04`, `h08_d_05`, `h08_d_06`, `h08_d_07`, `h08_d_08`, `h08_d_09`, `h08_d_10`, `h08_d_11`, `h08_d_12`, `h08_d_13`, `h08_d_14`, `h08_d_15`, `h08_d_16`, `h09_d_01`, `h09_d_02`, `h10_d_01`, `h10_d_02`, `h10_d_03`, `h10_d_04`, `h10_d_05`, `h11_d_01`, `h11_d_02`, `h11_d_03`, `h11_d_04`, `h12_d_01`, `h12_d_02`, `h12_d_03`, `h12_d_04`, `h12_d_05`, `h12_d_06`, `h13_d_01`, `h13_d_02`, `h13_d_03`, `h13_d_04`, `h13_d_05`, `h13_d_06`, `h14_d_01`, `h14_d_02`, `h14_d_03`, `h14_d_04`, `h14_d_05`, `h14_d_06`, `h14_d_07`

Mobile IDs covered by this ledger:

`h01_m_01`, `h01_m_02`, `h01_m_03`, `h01_m_04`, `h01_m_05`, `h01_m_06`, `h01_m_07`, `h01_m_08`, `h01_m_09`, `h02_m_01`, `h02_m_02`, `h02_m_03`, `h03_m_01`, `h03_m_02`, `h03_m_03`, `h03_m_04`, `h03_m_05`, `h04_m_01`, `h04_m_02`, `h04_m_03`, `h04_m_04`, `h04_m_05`, `h04_m_06`, `h04_m_07`, `h04_m_08`, `h04_m_09`, `h04_m_10`, `h04_m_11`, `h04_m_12`, `h04_m_13`, `h04_m_14`, `h04_m_15`, `h04_m_16`, `h04_m_17`, `h04_m_18`, `h04_m_19`, `h04_m_20`, `h04_m_21`, `h05_m_01`, `h05_m_02`, `h05_m_03`, `h05_m_04`, `h05_m_05`, `h06_m_01`, `h06_m_02`, `h06_m_03`, `h06_m_04`, `h07_m_01`, `h07_m_02`, `h07_m_03`, `h07_m_04`, `h07_m_05`, `h07_m_06`, `h07_m_07`, `h07_m_08`, `h07_m_09`, `h08_m_01`, `h08_m_02`, `h08_m_03`, `h08_m_04`, `h08_m_05`, `h08_m_06`, `h08_m_07`, `h08_m_08`, `h08_m_09`, `h08_m_10`, `h08_m_11`, `h08_m_12`, `h08_m_13`, `h08_m_14`, `h08_m_15`, `h08_m_16`, `h09_m_01`, `h09_m_02`, `h10_m_01`, `h10_m_02`, `h10_m_03`, `h10_m_04`, `h10_m_05`, `h11_m_01`, `h11_m_02`, `h11_m_03`, `h11_m_04`, `h12_m_01`, `h12_m_02`, `h12_m_03`, `h12_m_04`, `h12_m_05`, `h12_m_06`, `h13_m_01`, `h13_m_02`, `h13_m_03`, `h13_m_04`, `h13_m_05`, `h13_m_06`, `h14_m_01`, `h14_m_02`, `h14_m_03`, `h14_m_04`, `h14_m_05`, `h14_m_06`, `h14_m_07`

## Backlog From This Closeout

1. Add a future cross-repo generated-page parity gate before rebuilding any product release packages.
2. Revisit a larger What Is an MCP educational redesign only after the product pages stay stable.
3. Design alpha-product notification or waitlist flows only if there is a real collection, consent, and privacy path.
4. Keep the mobile-only visual fork deferred unless the shared responsive system fails future browser checks.
5. Refresh product examples/docs in their own product lanes, not as part of this public-surface UX closeout.
