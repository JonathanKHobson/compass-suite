# Working Tools maintenance

Read README.md and docs/project-map.md. suite-manifest.json owns Compass release facts; data/tool-library.json owns the wider public catalog. Keep editorial changes aligned with content/site-copy.md.

Run `python3 scripts/validate_suite_site.py`; use `--check-links` when public destinations change. Browser QA is required for affected page interactions and layout. The site is static and needs no package installation for its documented validator or Python preview.

Other Compass sites consume shared assets from this repository. Preserve public asset paths, legal pages and compatibility routes. Shared portfolio network source is maintained separately and copied deliberately; do not confuse that update-time dependency with assets fetched at runtime.

Keep private systems and unshipped packages out of the public catalog. A successor release requires its own verified installation and distribution evidence. Preserve existing download URLs while successors are prepared.
