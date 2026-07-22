#!/usr/bin/env python3
"""Validate the Working Tools public site before publishing."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COMPASS_IDS = [
    "critical-compass",
    "prompt-compass",
    "ux-heuristics-compass",
    "ttrpg-compass",
    "research-compass",
    "job-application-compass",
]
ALLOWED_JOBS = {"write", "research", "design", "build", "career", "teach", "table"}
ALLOWED_ACCESS = {"public-download", "public-site", "connected-service", "local-only", "preview"}
PAGE_FILES = [Path("index.html"), Path("404.html"), Path("about/index.html"), Path("license/index.html")]
REQUIRED_FILES = [
    *PAGE_FILES,
    Path("styles.css"),
    Path("assets/working-tools-mark.svg"),
    Path("assets/generated/working-tools-editorial-v01.png"),
    Path("assets/generated/working-tools-editorial-v01.jpg"),
    Path("assets/css/main.css"),
    Path("assets/css/tokens.css"),
    Path("assets/css/base.css"),
    Path("assets/css/layout.css"),
    Path("assets/css/components.css"),
    Path("assets/css/responsive.css"),
    Path("assets/js/main.js"),
    Path("assets/js/catalog.js"),
    Path("content/site-copy.md"),
    Path("data/tool-library.json"),
    Path("suite-manifest.json"),
    Path("docs/project-map.md"),
    Path("docs/design-direction.md"),
    Path("docs/asset-manifest.md"),
    Path("snippets/universal-footer.html"),
    Path("legal/LICENSE-CODE-AGPL-3.0.txt"),
    Path("legal/LICENSE-DOCS-CC-BY-SA-4.0.md"),
    Path("legal/BRAND-AND-ATTRIBUTION.md"),
    Path("legal/NOTICE.md"),
    Path("legal/THIRD_PARTY_NOTICES.md"),
]
INSTALL_IMAGES = [
    Path("assets/install-guide/plugin/plugin-02-customize.png"),
    Path("assets/install-guide/plugin/plugin-06-upload-plugin-menu.png"),
    Path("assets/install-guide/plugin/plugin-09-installed.png"),
    Path("assets/install-guide/mcpb/mcpb-01-download.png"),
    Path("assets/install-guide/mcpb/mcpb-03-extensions.png"),
    Path("assets/install-guide/mcpb/mcpb-05-installed.png"),
    Path("assets/install-guide/skill/skill-01-open-skills.png"),
    Path("assets/install-guide/skill/skill-03-upload-skill-menu.png"),
    Path("assets/install-guide/skill/skill-05-installed.png"),
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(relative: Path | str) -> str:
    path = ROOT / relative
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(relative: Path | str) -> dict:
    try:
        return json.loads(read(relative))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {relative}: {exc}")


class ImageAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "img":
            self.images.append({key: value or "" for key, value in attrs})


def validate_files() -> None:
    for relative in REQUIRED_FILES + INSTALL_IMAGES:
        path = ROOT / relative
        if not path.is_file():
            fail(f"missing required file: {relative}")
        if path.suffix.lower() in {".png", ".jpg", ".jpeg"} and path.stat().st_size < 10_000:
            fail(f"image appears empty or incomplete: {relative}")

    if (ROOT / "assets/compass-badge.svg").exists():
        fail("retired Compass badge is still present")
    if (ROOT / "site.js").exists():
        fail("retired monolithic site.js is still present")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.name == ".DS_Store" or path.name.startswith("._"):
            fail(f"sidecar file found: {path.relative_to(ROOT)}")


def validate_public_text() -> None:
    relative_text_files = [
        *PAGE_FILES,
        Path("styles.css"),
        Path("assets/css/tokens.css"),
        Path("assets/css/base.css"),
        Path("assets/css/layout.css"),
        Path("assets/css/components.css"),
        Path("assets/css/responsive.css"),
        Path("assets/js/main.js"),
        Path("assets/js/catalog.js"),
        Path("content/site-copy.md"),
        Path("data/tool-library.json"),
        Path("suite-manifest.json"),
        Path("snippets/universal-footer.html"),
    ]
    combined = "\n".join(read(path) for path in relative_text_files)
    forbidden = [
        "/Volumes/",
        "/Users/",
        "compass-badge",
        "Choose the right Compass",
        "compass-public-visual-system: uxhc-v1",
        "PLACE" + "HOLDER",
        ".DS_Store",
    ]
    for string in forbidden:
        if string in combined:
            fail(f"forbidden public string found: {string}")

    home = read("index.html")
    for required in [
        "Working Tools by J. Kyle Hobson",
        "Use the tool that fits the work.",
        'href="#work"',
        'id="library"',
        'data-library-search',
        'data-library-filter="all"',
        'data-library-list',
        'aria-live="polite"',
        'id="install"',
        "humanizer-writing-tools.jkylehobson.chatgpt.site",
        "shareables/s/humanizer-writing-enhancement/",
        "assets/generated/working-tools-editorial-v01.jpg",
        'type="module"',
    ]:
        if required not in home:
            fail(f"homepage contract missing: {required}")

    for page in PAGE_FILES:
        text = read(page)
        for required in ["skip-link", "site-header", "site-footer", "working-tools-mark.svg"]:
            if required not in text:
                fail(f"{page} missing shared shell requirement: {required}")

    audit = ImageAudit()
    audit.feed(home)
    if len(audit.images) != 10:
        fail(f"expected 10 homepage images, found {len(audit.images)}")
    for image in audit.images:
        if "alt" not in image or not image["alt"].strip():
            fail(f"homepage image missing useful alt text: {image.get('src', 'unknown')}")
        if "install-guide" in image.get("src", "") and image.get("loading") != "lazy":
            fail(f"install screenshot must be lazy-loaded: {image['src']}")
    hero = next((image for image in audit.images if "working-tools-editorial" in image.get("src", "")), None)
    if not hero or hero.get("width") != "1023" or hero.get("height") != "1600":
        fail("hero artwork must reserve its verified 1023 by 1600 dimensions")


def validate_css_and_js() -> None:
    css = "\n".join(
        read(path)
        for path in [
            "assets/css/tokens.css",
            "assets/css/base.css",
            "assets/css/layout.css",
            "assets/css/components.css",
            "assets/css/responsive.css",
        ]
    )
    for contract in [
        ":focus-visible",
        "overflow-x: hidden",
        "@media (max-width: 48rem)",
        "@media (prefers-reduced-motion: reduce)",
        ".library-row",
        ".task-grid",
        ".install-gallery",
        ".content-grid",
        "--signal: #d95d3a",
        "--highlight: #e7ff32",
    ]:
        if contract not in css:
            fail(f"CSS contract missing: {contract}")
    if "fonts.googleapis.com" in css or "linear-gradient" in css:
        fail("visual system must remain dependency-light and gradient-free")

    js = read("assets/js/catalog.js") + read("assets/js/main.js")
    for contract in [
        'fetch("data/tool-library.json")',
        'fetch("suite-manifest.json")',
        'setAttribute("aria-pressed"',
        "replaceChildren",
        "textContent",
    ]:
        if contract not in js:
            fail(f"JavaScript contract missing: {contract}")
    if "innerHTML" in js:
        fail("catalog rendering must not inject innerHTML")


def validate_manifest(manifest: dict) -> None:
    site = manifest.get("site", {})
    if site.get("name") != "Working Tools by J. Kyle Hobson":
        fail("manifest site name is not the new public brand")
    products = manifest.get("products", [])
    if [item.get("id") for item in products] != EXPECTED_COMPASS_IDS:
        fail("Compass products changed order, identity, or count")

    download_count = 0
    for product in products:
        product_id = product["id"]
        downloads = product.get("downloads", [])
        if product_id in {"ttrpg-compass", "research-compass"} and downloads:
            fail(f"preview product exposes downloads: {product_id}")
        if product_id == "job-application-compass":
            if product.get("safety_gate") != "public_skills_only_private_mcp_locked":
                fail("Job Application Compass private MCP gate changed")
            for item in downloads:
                if "mcp" in item.get("kind", "") or "source" in item.get("kind", ""):
                    fail("Job Application Compass may publish skills only")
        for item in downloads:
            download_count += 1
            if item.get("availability") != "available":
                fail(f"download is not marked available: {product_id}/{item.get('filename')}")
            if not item.get("url", "").startswith("https://"):
                fail(f"download is not HTTPS: {product_id}/{item.get('filename')}")
            if not re.fullmatch(r"[a-f0-9]{64}", item.get("checksum", "")):
                fail(f"download checksum is not SHA-256: {product_id}/{item.get('filename')}")
    if download_count != 20:
        fail(f"expected 20 preserved Compass downloads, found {download_count}")


def validate_library(library: dict) -> None:
    if library.get("schema_version") != "working-tools.library.v1":
        fail("unexpected tool library schema")
    labels = library.get("access_labels", {})
    if set(labels) != ALLOWED_ACCESS:
        fail(f"access label set changed: {sorted(labels)}")
    items = library.get("items", [])
    if len(items) < 30:
        fail(f"tool library is unexpectedly small: {len(items)} records")
    ids = [item.get("id") for item in items]
    if len(ids) != len(set(ids)) or None in ids:
        fail("tool library IDs must be present and unique")

    required_ids = {
        "humanizer",
        "creative-writing-studio",
        "ux-design-toolkit",
        "builder-tools",
        "participatory-defense-field-guide",
        "sites",
        "figma-service",
        "kyle-second-brain",
        "shareables-mcp",
        "arxiv-scout",
    }
    if not required_ids.issubset(ids):
        fail(f"required catalog records missing: {sorted(required_ids - set(ids))}")

    for item in items:
        access = item.get("access")
        if access not in ALLOWED_ACCESS:
            fail(f"unknown access label on {item['id']}: {access}")
        jobs = set(item.get("jobs", []))
        if not jobs or not jobs.issubset(ALLOWED_JOBS):
            fail(f"invalid or empty job mapping on {item['id']}: {sorted(jobs)}")
        href = item.get("href")
        action = item.get("action")
        if access in {"local-only", "connected-service", "preview"} and (href or action):
            fail(f"non-public record exposes an action: {item['id']}")
        if access in {"public-download", "public-site"}:
            if not href or not href.startswith("https://") or not action:
                fail(f"public record lacks a verified HTTPS action: {item['id']}")
        public_blob = json.dumps(item)
        if "/Volumes/" in public_blob or "/Users/" in public_blob:
            fail(f"local path exposed in catalog record: {item['id']}")


def check_url(url: str) -> None:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "WorkingToolsValidator/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            if response.status >= 400:
                fail(f"URL returned HTTP {response.status}: {url}")
    except urllib.error.HTTPError as exc:
        if exc.code not in {403, 405}:
            fail(f"URL returned HTTP {exc.code}: {url}")
        fallback = urllib.request.Request(url, headers={"User-Agent": "WorkingToolsValidator/1.0", "Range": "bytes=0-0"})
        try:
            with urllib.request.urlopen(fallback, timeout=25) as response:
                if response.status >= 400:
                    fail(f"URL returned HTTP {response.status}: {url}")
        except urllib.error.URLError as fallback_exc:
            fail(f"URL check failed for {url}: {fallback_exc}")
    except urllib.error.URLError as exc:
        fail(f"URL check failed for {url}: {exc}")


def validate_links(manifest: dict, library: dict) -> None:
    urls: set[str] = {
        "https://humanizer-writing-tools.jkylehobson.chatgpt.site",
        "https://jonathankhobson.github.io/shareables/s/humanizer-writing-enhancement/",
        "https://jonathankhobson.github.io/shareables/s/participatory-defense-field-guide/",
    }
    for product in manifest["products"]:
        for key in ("homepage_url", "repo_url", "learn_more_url"):
            value = product.get(key, "")
            if value.startswith("https://"):
                urls.add(value)
        urls.update(item["url"] for item in product.get("downloads", []))
    urls.update(item["href"] for item in library["items"] if item.get("href"))
    for url in sorted(urls):
        check_url(url)
        print(f"OK: {url}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-links", action="store_true", help="verify public destinations over the network")
    args = parser.parse_args()

    validate_files()
    validate_public_text()
    validate_css_and_js()
    manifest = load_json("suite-manifest.json")
    library = load_json("data/tool-library.json")
    validate_manifest(manifest)
    validate_library(library)
    if args.check_links:
        validate_links(manifest, library)
    print("Working Tools site validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
