# Contributing

For a broken page, download, or install instruction, open an issue with the exact public URL, what you expected, what happened, and enough steps to reproduce it. Include your browser or client version when relevant. Remove personal records, credentials, and private paths from logs.

For a code or documentation change, read README.md and AGENTS.md, make a focused branch, and run `python3 scripts/validate_suite_site.py`. Check changed external destinations with `--check-links`. Include the verification result in your pull request; attach desktop and mobile evidence for visible changes.

Keep release facts in suite-manifest.json and catalog entries in data/tool-library.json. Do not add a package to the public catalog before its actual public destination and installation instructions work. Preserve existing asset and download URLs. Changes to third-party license terms require rights evidence.

This repository accepts reports about the public Working Tools directory. Report a specific product defect in that product’s repository when possible. A public issue is not an appropriate place for secrets or private application data.
