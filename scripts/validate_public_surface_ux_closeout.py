#!/usr/bin/env python3
"""Validate the cross-Compass public-surface UX closeout."""

from __future__ import annotations

import re
import sys
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parents[1]

PUBLIC_SURFACES = {
    "compass-suite": {
        "files": [SUITE_ROOT / "index.html", SUITE_ROOT / "404.html", SUITE_ROOT / "styles.css", SUITE_ROOT / "site.js"],
        "kind": "suite",
    },
    "critical-compass": {
        "files": [Path("/Volumes/KyleSSD/CriticalThinking/dist/share/github-pages/index.html")],
        "kind": "product",
    },
    "prompt-compass": {
        "files": [Path("/Volumes/KyleSSD/prompt-compass/dist/share/github-pages/index.html")],
        "kind": "product",
    },
    "ux-heuristic-compass": {
        "files": [
            Path("/Volumes/KyleSSD/ux-heuristic-compass/dist/share/github-pages/index.html"),
            Path("/Volumes/KyleSSD/ux-heuristic-compass/dist/share/github-pages/styles.css"),
            Path("/Volumes/KyleSSD/ux-heuristic-compass/dist/share/github-pages/site.js"),
        ],
        "kind": "product",
    },
    "what-is-an-mcp": {
        "files": [Path("/Volumes/KyleSSD/CriticalThinking/dist/share/mcp-explainer-site/index.html")],
        "kind": "support",
    },
}

LEDGER = SUITE_ROOT / "docs/audits/compass-public-surface-ux-audit-ledger-2026-05-04.md"

FORBIDDEN_PUBLIC_STRINGS = [
    "About & FAQ",
    "About &amp; FAQ",
    "PLACEHOLDER",
    "Download + Learn",
    "package-pending",
    "/Users/",
    "/Volumes/",
]

PRODUCT_REQUIRED = [
    "Back to Compass Suite",
    "Not sure what to download?",
    "Claude Code / Cowork Plugin",
    "Claude Desktop Extension",
    "Download and Open Guide",
    "MCP Basics (opens in a new tab)",
    "data-guide-hash",
    "Download started. Guide opened.",
    "overflow-x: hidden",
    ".download-chooser",
    ".sr-only",
]

SUPPORT_REQUIRED = [
    "Back to Compass Suite",
    "Compass Recovery Links",
    "https://jonathankhobson.github.io/critical-compass/",
    "https://jonathankhobson.github.io/prompt-compass/",
    "https://jonathankhobson.github.io/ux-heuristic-compass/",
    "overflow-x: hidden",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


def validate_forbidden_text(name: str, text: str) -> None:
    for forbidden in FORBIDDEN_PUBLIC_STRINGS:
        if forbidden in text:
            fail(f"{name} contains forbidden public string: {forbidden}")


def validate_mcp_links(name: str, text: str) -> None:
    for match in re.finditer(r'<a\\s+[^>]*href="([^"]*what-is-an-mcp[^"]*)"[^>]*>', text):
        tag = match.group(0)
        href = match.group(1)
        if 'target="_blank"' not in tag or 'rel="noopener"' not in tag:
            fail(f"{name} MCP link must open in a new tab with noopener: {href}")


def validate_product(name: str, text: str) -> None:
    for required in PRODUCT_REQUIRED:
        if required not in text:
            fail(f"{name} missing product-page closeout requirement: {required}")
    if text.count("Download and Open Guide") < 2:
        fail(f"{name} should have primary plugin and extension guide-download CTAs")
    validate_mcp_links(name, text)


def validate_support(name: str, text: str) -> None:
    for required in SUPPORT_REQUIRED:
        if required not in text:
            fail(f"{name} missing support-page closeout requirement: {required}")
    if "target=\"_blank\"" in text and "rel=\"noopener\"" not in text:
        fail(f"{name} has a new-tab link without noopener")


def validate_surface(name: str, config: dict[str, object]) -> None:
    combined = "\n".join(read(path) for path in config["files"])  # type: ignore[index]
    validate_forbidden_text(name, combined)
    kind = config["kind"]
    if kind == "product":
        validate_product(name, combined)
    elif kind == "support":
        validate_support(name, combined)


def validate_sidecars() -> None:
    roots = [
        SUITE_ROOT,
        Path("/Volumes/KyleSSD/CriticalThinking/dist/share/github-pages"),
        Path("/Volumes/KyleSSD/prompt-compass/dist/share/github-pages"),
        Path("/Volumes/KyleSSD/ux-heuristic-compass/dist/share/github-pages"),
        Path("/Volumes/KyleSSD/CriticalThinking/dist/share/mcp-explainer-site"),
    ]
    for root in roots:
        for path in root.rglob("*"):
            if ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if path.name == ".DS_Store" or path.name.startswith("._"):
                fail(f"sidecar file found: {path}")


def validate_ledger() -> None:
    text = read(LEDGER)
    for status in ["fixed_live", "partially_fixed", "needs_patch", "defer_backlog", "not_applicable"]:
        if status not in text:
            fail(f"audit ledger missing status: {status}")
    for source in [
        "Compass Suite",
        "Critical Compass",
        "Prompt Compass",
        "UX Heuristics Compass",
        "What Is an MCP",
        "h01_d_01",
        "h14_m_07",
        "Release-builder/template parity",
    ]:
        if source not in text:
            fail(f"audit ledger missing required coverage note: {source}")


def main() -> int:
    for name, config in PUBLIC_SURFACES.items():
        validate_surface(name, config)
        print(f"OK: {name}")
    validate_sidecars()
    validate_ledger()
    print("Compass public-surface UX closeout validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
