# Compass Suite historical maintenance

This is the read-only predecessor. Maintained catalog source and builds belong in
JonathanKHobson/working-tools-site. Preserve the existing Pages, migration, shared
asset and download paths here. The following instructions describe the historical
source and do not authorize reopening it for routine catalog work.

Read README.md and docs/project-map.md. data/plugin-releases.json is the pinned projection of current public plugin releases; regenerate it from the verified public package registry. data/storefront-copy.json owns product descriptions and grouping, and data/tool-library.json owns the standalone public guides. suite-manifest.json preserves historical Compass release and download records. Keep editorial changes aligned with content/site-copy.md.

Run `python3 scripts/validate_suite_site.py`; use `--check-links` when public destinations change. Browser QA is required for affected page interactions and layout. The site is static and needs no package installation for its documented validator or Python preview.

Other Compass sites consume shared assets from this repository. Preserve public asset paths, legal pages and compatibility routes. Shared portfolio network source is maintained separately and copied deliberately; do not confuse that update-time dependency with assets fetched at runtime.

Keep private systems and unshipped packages out of the public catalog. A successor release requires its own verified installation and distribution evidence. Preserve existing download URLs while successors are prepared.
