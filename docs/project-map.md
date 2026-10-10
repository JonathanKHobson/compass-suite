# Working Tools project map

## Purpose

This repository owns the Working Tools public catalog source, shared site
assets, and compatibility pages for older releases. The live storefront leads
with the released plugin ecosystem; GitHub package pages carry installation,
dependencies, source, and license details.

## Entrypoints

- `index.html`: main catalog page, task filters, and storefront calls to action.
- `assets/js/catalog.js`: loads the released package projection and current
  standalone public guides, groups products, and renders accessible filters.
- `data/storefront-copy.json`: visitor-facing product descriptions and family
  groupings. It does not replace package technical metadata.
- `data/plugin-releases.json`: immutable projection of released public plugin
  packages, versioned destinations, skills, technical details, and source
  revision. Regenerate it from the public plugin source with
  `scripts/sync_plugin_registry.py`.
- `data/tool-library.json`: standalone public guides shown beside plugins.
- `legacy/index.html`: one entry point to preserved earlier product pages.
- `migration/forward.js`: keeps original GitHub Pages routes available.
- `scripts/build_working_tools_site.py`: builds the hosted projection from
  pinned commits and turns retired product pages into Legacy Library redirects,
  while preserving original archive and download destinations.
- `suite-manifest.json`: historical release status, preserved download URLs,
  checksums, and continuity constraints.
- `scripts/validate_suite_site.py`: catalog, privacy, content, route, and
  structural checks.

## Data flow

1. The catalog loads `data/plugin-releases.json` and `data/tool-library.json`.
2. Released packages are presented with benefit-led copy from
   `data/storefront-copy.json`; each card links to its versioned GitHub release.
3. Requirements, license, scope, and technical package overview stay behind a
   disclosure on the card and in the GitHub package documentation.
4. Earlier products are accessible through the single Legacy Library link.
   Their original GitHub Pages paths and release assets remain preserved.

## Safe changes

- Edit storefront language and grouping in `data/storefront-copy.json`.
- Update technical package facts at their source in `working-tools-plugins`,
  then regenerate the projection with `scripts/sync_plugin_registry.py`.
- Update standalone guide links in `data/tool-library.json`.
- Preserve `suite-manifest.json` release URLs and checksums during the archive
  transition.
- Keep old compatibility files available until every redirect, asset, and
  download destination has been verified from the replacement source.

## Verification

```bash
python3 scripts/validate_suite_site.py
python3 scripts/test_site_transition.py
python3 scripts/validate_suite_site.py --check-links
```

Use a local HTTP preview for catalog interaction checks. Before publishing,
verify desktop and mobile layouts, keyboard focus, filter states, package links,
and legacy destinations in a rendered browser.
