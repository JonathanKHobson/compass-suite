# Compass Suite Storefront

Static storefront for the Compass Suite. This page links people to individual Compass home pages and public downloads without replacing the product-specific pages.

## Current V1 Boundary

- Tabs: `Get Started`, `About`, `Install Guide`, `FAQ`.
- No `Advanced` or `Examples` tab in the suite site yet.
- Critical Compass and Prompt Compass are the only products with public download buttons.
- Alpha and early-alpha products stay preview-only until their packages, pages, and privacy boundaries are verified.
- Job Application Compass must not publish downloads, screenshots, examples, or home-page content until a personal-information scrub passes.

## Source of Truth

Use `suite-manifest.json` for product status, download URLs, checksums, maturity labels, and safety gates.

When a product release changes:

1. Update `suite-manifest.json`.
2. Update matching card content in `index.html`.
3. Run the validator.
4. Verify public URLs before publishing.

## Local Preview

```bash
python3 -m http.server 8787
```

Then open:

```text
http://127.0.0.1:8787/
```

## Validate

```bash
python3 scripts/validate_suite_site.py
```

Optional live link check:

```bash
python3 scripts/validate_suite_site.py --check-links
```

## Publish Guardrails

- Do not copy a generated individual Compass page over this suite site.
- Do not combine `About` and `FAQ`.
- Do not add direct alpha downloads until package and public/private-boundary checks pass.
- Do not publish Job Application Compass material until the personal-information scrub passes.
- Individual Compass pages remain authoritative for install specifics, checksums, examples, and release notes.
