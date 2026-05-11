#!/usr/bin/env python3
"""Validate the cross-Compass public-surface UX closeout."""

from __future__ import annotations

import re
import sys
import os
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_ROOT = Path(
    os.environ.get(
        "COMPASS_PUBLIC_SITES_ROOT",
        SUITE_ROOT.parent.parent if SUITE_ROOT.parent.name == "websites" else SUITE_ROOT.parent,
    )
).resolve()


def configured_path(env_name: str, *default_parts: str) -> Path:
    configured = os.environ.get(env_name)
    if configured:
        return Path(configured).expanduser().resolve()
    return (BUNDLE_ROOT / Path(*default_parts)).resolve()


LOCAL_USER_PATH = "/" + "Users/"
LOCAL_VOLUME_PATH = "/" + "Volumes/"
UNFILLED_SENTINEL = "PLACE" + "HOLDER"

PUBLIC_SURFACES = {
    "compass-suite": {
        "files": [
            SUITE_ROOT / "index.html",
            SUITE_ROOT / "404.html",
            SUITE_ROOT / "about" / "index.html",
            SUITE_ROOT / "license" / "index.html",
            SUITE_ROOT / "styles.css",
            SUITE_ROOT / "site.js",
        ],
        "kind": "suite",
    },
    "critical-compass": {
        "files": [configured_path("CRITICAL_COMPASS_PUBLIC_PAGE", "websites", "critical-compass", "index.html")],
        "kind": "product",
        "release_url": "https://github.com/JonathanKHobson/critical-compass/releases/download/v0.1.0-beta.10/",
    },
    "prompt-compass": {
        "files": [configured_path("PROMPT_COMPASS_PUBLIC_PAGE", "websites", "prompt-compass", "index.html")],
        "kind": "product",
        "release_url": "https://github.com/JonathanKHobson/prompt-compass/releases/download/v0.1.0-beta.3/",
    },
    "ux-heuristic-compass": {
        "files": [
            configured_path("UXHC_PUBLIC_PAGE", "websites", "ux-heuristic-compass", "index.html"),
            configured_path("UXHC_PUBLIC_STYLES", "websites", "ux-heuristic-compass", "styles.css"),
            configured_path("UXHC_PUBLIC_SCRIPT", "websites", "ux-heuristic-compass", "site.js"),
        ],
        "kind": "product",
        "release_url": "https://github.com/JonathanKHobson/ux-heuristic-compass/releases/download/v0.1.0-beta.10/",
    },
    "what-is-an-mcp": {
        "files": [configured_path("MCP_EXPLAINER_PUBLIC_PAGE", "websites", "what-is-an-mcp", "index.html")],
        "kind": "support",
    },
    "ai-basics": {
        "files": [configured_path("AI_BASICS_PUBLIC_PAGE", "websites", "shareables", "s", "understanding-ai-2026", "index.html")],
        "kind": "resource",
    },
}

LEDGER = SUITE_ROOT / "docs/audits/compass-public-surface-ux-audit-ledger-2026-05-04.md"

FORBIDDEN_PUBLIC_STRINGS = [
    "About & FAQ",
    "About &amp; FAQ",
    UNFILLED_SENTINEL,
    "Download + Learn",
    "package-pending",
    LOCAL_USER_PATH,
    LOCAL_VOLUME_PATH,
]

PRODUCT_REQUIRED = [
    "Back to Compass Suite",
    "Not sure what to download?",
    "Claude Code / Cowork Plugin",
    "Claude Desktop Extension",
    "Download and Open Guide",
    "MCP Basics (opens in a new tab)",
    "AI Basics",
    "data-guide-hash",
    "Download started. Guide opened.",
    "overflow-x: hidden",
    ".download-chooser",
    "site-nav",
    "site-nav-toggle",
    "section-nav-toggle",
    "progress-bar",
    "--font-display",
    "--site-nav-h",
    ".sr-only",
    "suite-footer",
    "Compass Suite is created and maintained by Jonathan Kyle Hobson.",
    "License &amp; Attribution",
]

SUPPORT_REQUIRED = [
    "Back to Compass Suite",
    "AI Basics",
    "Compass Recovery Links",
    "site-nav",
    "site-nav-toggle",
    "progress-bar",
    "--font-display",
    "--site-nav-h",
    "https://jonathankhobson.github.io/critical-compass/",
    "https://jonathankhobson.github.io/prompt-compass/",
    "https://jonathankhobson.github.io/ux-heuristic-compass/",
    "overflow-x: hidden",
    "suite-footer",
    "Compass Suite is created and maintained by Jonathan Kyle Hobson.",
    "License &amp; Attribution",
]

RESOURCE_REQUIRED = [
    "AI Basics",
    "site-nav",
    "site-nav-toggle",
    "section-nav-toggle",
    "progress-bar",
    "--font-display",
    "--site-nav-h",
    "Compass Suite is created and maintained by Jonathan Kyle Hobson.",
    "suite-footer",
    "License &amp; Attribution",
    "compass-public-visual-system: uxhc-v1",
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
    skip_ranges = [
        (match.start(), match.end())
        for match in re.finditer(r'<footer class="suite-footer"[^>]*>.*?</footer>', text, flags=re.DOTALL)
    ]
    skip_ranges += [
        (match.start(), match.end())
        for match in re.finditer(r'<nav class="site-nav"[^>]*>.*?</nav>', text, flags=re.DOTALL)
    ]
    for match in re.finditer(r'<a\s+[^>]*href="([^"]*what-is-an-mcp[^"]*)"[^>]*>', text):
        tag = match.group(0)
        href = match.group(1)
        if any(start <= match.start() < end for start, end in skip_ranges):
            continue
        if 'target="_blank"' not in tag or 'rel="noopener"' not in tag:
            fail(f"{name} MCP link must open in a new tab with noopener: {href}")


def validate_product(name: str, text: str) -> None:
    for required in PRODUCT_REQUIRED:
        if required not in text:
            fail(f"{name} missing product-page closeout requirement: {required}")
    release_url = PUBLIC_SURFACES[name].get("release_url")
    if release_url and str(release_url) not in text:
        fail(f"{name} missing expected release URL prefix: {release_url}")
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
    if "site-nav-toggle" not in combined or 'aria-controls="site-nav-menu"' not in combined:
        fail(f"{name} missing mobile network menu contract")
    if config["kind"] in {"product", "suite"} and "section-nav-toggle" not in combined:
        fail(f"{name} missing mobile section menu contract")
    if "AI Basics" not in combined:
        fail(f"{name} missing AI Basics network/resource link")
    kind = config["kind"]
    if kind == "product":
        validate_product(name, combined)
    elif kind == "support":
        validate_support(name, combined)
    elif kind == "resource":
        for required in RESOURCE_REQUIRED:
            if required not in combined:
                fail(f"{name} missing resource-page closeout requirement: {required}")
        for dark_token in ["#09090e", "--bg:       #09090e", "--surf:     #111118"]:
            if dark_token in combined:
                fail(f"{name} contains dark-mode token regression: {dark_token}")


def validate_sidecars() -> None:
    roots = [
        SUITE_ROOT,
        configured_path("CRITICAL_COMPASS_PUBLIC_ROOT", "websites", "critical-compass"),
        configured_path("PROMPT_COMPASS_PUBLIC_ROOT", "websites", "prompt-compass"),
        configured_path("UXHC_PUBLIC_ROOT", "websites", "ux-heuristic-compass"),
        configured_path("MCP_EXPLAINER_PUBLIC_ROOT", "websites", "what-is-an-mcp"),
        configured_path("AI_BASICS_PUBLIC_ROOT", "websites", "shareables"),
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
