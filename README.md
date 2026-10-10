# Working Tools by J. Kyle Hobson

Working Tools is the rebuilt public directory that replaces the old Compass
Suite storefront. It connects the existing Compass products with Humanizer,
public field guides, downloadable skill collections, connected services, and a
carefully bounded view of local systems.

The visitor starts with a job: write, research, design, build, career, teach, or run a game.

## Current plugins and historical compatibility

Installable packages now live in [Working Tools Plugins](https://github.com/JonathanKHobson/working-tools-plugins). Use that repository for plugin releases, host installation, contribution and support. This repository continues to own the catalog source, Compass compatibility pages and retained downloads. It stays active because existing sites depend on those assets. Older Compass source and release tags remain in their original repositories.

[Open the public catalog](https://working-tools.jkylehobson.chatgpt.site/) or read the [successor guide](https://github.com/JonathanKHobson/working-tools-plugins/blob/main/docs/compass-transition.md).

## Sources of truth

- `suite-manifest.json`: Compass release status, public URLs, checksums, and
  safety gates. Do not duplicate these facts in HTML.
- `data/plugin-releases.json`: generated projection of a pinned public plugin registry revision; update with `scripts/sync_plugin_registry.py`.
- `data/tool-library.json`: the larger public-safe directory and access labels.
- `content/site-copy.md`: editorial copy source.
- `docs/project-map.md`: architecture, ownership, and change paths.
- `docs/design-direction.md`: design thesis and visual QA anchors.
- `docs/asset-manifest.md`: source status and intended use for visuals.

## Local preview

```bash
python3 -m http.server 8787
```

Open `http://127.0.0.1:8787/`.

## Validate

```bash
python3 scripts/validate_suite_site.py
```

To check public destinations as well:

```bash
python3 scripts/validate_suite_site.py --check-links
```

## Publishing guardrails

- Public downloads must use a verified HTTPS destination.
- Local-only records must not expose a path, credential, private setup, or CTA.
- Preview Compass products do not gain downloads until their release and
  public/private reviews are complete.
- Job Application Compass remains skills-only; its private MCP and packet
  engine are not published.
- Generated artwork supplies atmosphere, not evidence. Install screenshots are
  documentary assets and remain separate.
- Run the validator and desktop/mobile visual QA before publishing.
