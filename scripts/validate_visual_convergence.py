#!/usr/bin/env python3
"""Validate shared visual and IA guardrails across Compass public pages."""

from __future__ import annotations

import re
import sys
import os
from pathlib import Path


WEBSITES_ROOT = Path(os.environ.get("COMPASS_PUBLIC_PAGE_BASE", Path(__file__).resolve().parents[2])).resolve()
LOCAL_VOLUME_PATH = "/" + "Volumes/"
LOCAL_USER_PATH = "/" + "Users/"
UNFILLED_SENTINEL = "PLACE" + "HOLDER"

LOCAL_PAGES = {
    "critical": {
        "path": WEBSITES_ROOT / "critical-compass" / "index.html",
        "tabs": ["Get Started", "About", "Install Guide", "Example", "FAQ", "Advanced"],
        "marker_file": WEBSITES_ROOT / "critical-compass" / "index.html",
        "kind": "product",
    },
    "prompt": {
        "path": WEBSITES_ROOT / "prompt-compass" / "index.html",
        "tabs": ["Get Started", "About", "Install Guide", "Example", "FAQ", "Advanced"],
        "marker_file": WEBSITES_ROOT / "prompt-compass" / "index.html",
        "kind": "product",
    },
    "uxhc": {
        "path": WEBSITES_ROOT / "ux-heuristic-compass" / "index.html",
        "tabs": ["Get Started", "About", "Install Guide", "Example", "FAQ", "Advanced"],
        "marker_file": WEBSITES_ROOT / "ux-heuristic-compass" / "styles.css",
        "downloads_enabled": True,
        "kind": "product",
    },
    "suite": {
        "path": WEBSITES_ROOT / "compass-suite" / "index.html",
        "tabs": ["Get Started", "About", "Install Guide", "FAQ"],
        "marker_file": WEBSITES_ROOT / "compass-suite" / "styles.css",
        "kind": "suite",
    },
    "mcp": {
        "path": WEBSITES_ROOT / "what-is-an-mcp" / "index.html",
        "tabs": [],
        "marker_file": WEBSITES_ROOT / "what-is-an-mcp" / "index.html",
        "kind": "support",
    },
    "ai-basics": {
        "path": WEBSITES_ROOT / "shareables" / "s" / "understanding-ai-2026" / "index.html",
        "tabs": [],
        "marker_file": WEBSITES_ROOT / "shareables" / "s" / "understanding-ai-2026" / "index.html",
        "kind": "resource",
    },
}

FORBIDDEN_PUBLIC_STRINGS = [
    "About & FAQ",
    "About &amp; FAQ",
    UNFILLED_SENTINEL,
    LOCAL_VOLUME_PATH,
    LOCAL_USER_PATH,
    ".DS_Store",
]

UXHC_RELEASE_URL = (
    "https://github.com/JonathanKHobson/ux-heuristic-compass/releases/download/"
)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def tab_labels(html: str) -> list[str]:
    return re.findall(r'data-tab-target="[^"]+">([^<]+)</button>', html)


def validate_page(name: str, config: dict) -> None:
    html = read(config["path"])
    labels = tab_labels(html)
    expected = config["tabs"]
    if labels != expected:
        fail(f"{name} tab order mismatch: got {labels}, expected {expected}")

    marker_text = read(config["marker_file"])
    if "compass-public-visual-system: uxhc-v1" not in marker_text:
        fail(f"{name} missing shared visual-system marker")
    combined = html + "\n" + marker_text
    for required in ["site-nav", "site-nav-toggle", "progress-bar", "--font-display", "--site-nav-h", "suite-footer"]:
        if required not in combined:
            fail(f"{name} missing shared visual-system requirement: {required}")
    if "AI Basics" not in combined:
        fail(f"{name} missing AI Basics network/resource link")
    if config.get("kind") in {"product", "suite", "resource"}:
        for required in ["section-nav-toggle", 'aria-controls="section-nav-menu"']:
            if required not in combined:
                fail(f"{name} missing mobile section-nav requirement: {required}")

    for forbidden in FORBIDDEN_PUBLIC_STRINGS:
        if forbidden in html:
            fail(f"{name} contains forbidden public string: {forbidden}")

    if config.get("kind") in {"product", "support"} and "Back to Compass Suite" not in html:
        fail(f"{name} missing Back to Compass Suite affordance")

    if name == "suite":
        for disallowed in ("Example", "Advanced"):
            if f">{disallowed}</button>" in html:
                fail(f"suite must not include {disallowed} tab")

    if config.get("downloads_enabled"):
        if UXHC_RELEASE_URL not in html:
            fail("UXHC release download links are missing after package verification")
        if "Download Opens After" in html or "Skill Download Coming Soon" in html:
            fail("UXHC still has pending download copy after package verification")


def validate_sidecars() -> None:
    for config in LOCAL_PAGES.values():
        root = config["path"].parent
        for path in root.rglob("*"):
            if ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if path.name == ".DS_Store" or path.name.startswith("._"):
                fail(f"sidecar file found: {path}")


def main() -> int:
    for name, config in LOCAL_PAGES.items():
        validate_page(name, config)
    validate_sidecars()
    print("Compass public page visual convergence validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
