#!/usr/bin/env python3
"""Validate the cross-Compass public-surface UX closeout."""

from __future__ import annotations

import re
import sys
import os
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parents[1]


def configured_path(env_name: str, *default_parts: str) -> Path:
    configured = os.environ.get(env_name)
    if configured:
        return Path(configured).expanduser().resolve()
    return (SUITE_ROOT.parent / Path(*default_parts)).resolve()


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
        "files": [configured_path("CRITICAL_COMPASS_PUBLIC_PAGE", "CriticalThinking", "dist", "share", "github-pages", "index.html")],
        "kind": "product",
    },
    "prompt-compass": {
        "files": [configured_path("PROMPT_COMPASS_PUBLIC_PAGE", "prompt-compass", "dist", "share", "github-pages", "index.html")],
        "kind": "product",
    },
    "ux-heuristic-compass": {
        "files": [
            configured_path("UXHC_PUBLIC_PAGE", "ux-heuristic-compass", "dist", "share", "github-pages", "index.html"),
            configured_path("UXHC_PUBLIC_STYLES", "ux-heuristic-compass", "dist", "share", "github-pages", "styles.css"),
            configured_path("UXHC_PUBLIC_SCRIPT", "ux-heuristic-compass", "dist", "share", "github-pages", "site.js"),
        ],
        "kind": "product",
    },
    "what-is-an-mcp": {
        "files": [configured_path("MCP_EXPLAINER_PUBLIC_PAGE", "CriticalThinking", "dist", "share", "mcp-explainer-site", "index.html")],
        "kind": "support",
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
    "data-guide-hash",
    "Download started. Guide opened.",
    "overflow-x: hidden",
    ".download-chooser",
    ".sr-only",
    "suite-footer",
    "Compass Suite is created and maintained by Jonathan Kyle Hobson.",
    "License &amp; Attribution",
]

SUPPORT_REQUIRED = [
    "Back to Compass Suite",
    "Compass Recovery Links",
    "https://jonathankhobson.github.io/critical-compass/",
    "https://jonathankhobson.github.io/prompt-compass/",
    "https://jonathankhobson.github.io/ux-heuristic-compass/",
    "overflow-x: hidden",
    "suite-footer",
    "Compass Suite is created and maintained by Jonathan Kyle Hobson.",
    "License &amp; Attribution",
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
    footer_ranges = [
        (match.start(), match.end())
        for match in re.finditer(r'<footer class="suite-footer"[^>]*>.*?</footer>', text, flags=re.DOTALL)
    ]
    for match in re.finditer(r'<a\\s+[^>]*href="([^"]*what-is-an-mcp[^"]*)"[^>]*>', text):
        tag = match.group(0)
        href = match.group(1)
        if any(start <= match.start() < end for start, end in footer_ranges):
            continue
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
        configured_path("CRITICAL_COMPASS_PUBLIC_ROOT", "CriticalThinking", "dist", "share", "github-pages"),
        configured_path("PROMPT_COMPASS_PUBLIC_ROOT", "prompt-compass", "dist", "share", "github-pages"),
        configured_path("UXHC_PUBLIC_ROOT", "ux-heuristic-compass", "dist", "share", "github-pages"),
        configured_path("MCP_EXPLAINER_PUBLIC_ROOT", "CriticalThinking", "dist", "share", "mcp-explainer-site"),
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
