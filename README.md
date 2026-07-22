# Working Tools by J. Kyle Hobson

Working Tools is the rebuilt public directory that replaces the old Compass
Suite storefront. It connects the existing Compass products with Humanizer,
public field guides, downloadable skill collections, connected services, and a
carefully bounded view of local systems.

The visitor starts with a job—write, research, design, build, career, teach, or
run a game—rather than a product family.

## Sources of truth

- `suite-manifest.json`: Compass release status, public URLs, checksums, and
  safety gates. Do not duplicate these facts in HTML.
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
