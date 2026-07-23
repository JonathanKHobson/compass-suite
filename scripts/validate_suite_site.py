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
COLLECTION_SLUGS = [
    "creative-writing-studio",
    "marketing-social-studio",
    "career-grants-studio",
    "ttrpg-gm-director",
    "ux-design-toolkit",
    "builder-tools",
]
EXPECTED_LIBRARY_IDS = {
    "humanizer",
    "creative-writing-studio",
    "marketing-social-studio",
    "career-grants-studio",
    "ttrpg-gm-director",
    "ux-design-toolkit",
    "builder-tools",
    "participatory-defense-field-guide",
    "understanding-ai-2026",
    "mcp-basics",
}
ALLOWED_JOBS = {"write", "research", "design", "build", "career", "teach", "table"}
ALLOWED_ACCESS = {"public-download", "public-site"}
CORE_PAGES = [Path("index.html"), Path("404.html"), Path("about/index.html"), Path("license/index.html")]
COLLECTION_PAGES = [Path(slug) / "index.html" for slug in COLLECTION_SLUGS]
PAGE_FILES = CORE_PAGES + COLLECTION_PAGES
REQUIRED_FILES = [
    *PAGE_FILES,
    Path("styles.css"),
    Path("assets/brand/working-tools-mark-64.png"),
    Path("assets/brand/working-tools-favicon-32.png"),
    Path("assets/brand/working-tools-icon-180.png"),
    Path("assets/css/main.css"),
    Path("assets/css/tokens.css"),
    Path("assets/css/base.css"),
    Path("assets/css/layout.css"),
    Path("assets/css/components.css"),
    Path("assets/css/collection.css"),
    Path("assets/css/responsive.css"),
    Path("assets/js/main.js"),
    Path("assets/js/site-nav.js"),
    Path("assets/js/collection.js"),
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
        is_compact_brand_asset = relative.parts[:2] == ("assets", "brand")
        minimum_size = 400 if is_compact_brand_asset else 10_000
        if path.suffix.lower() in {".png", ".jpg", ".jpeg"} and path.stat().st_size < minimum_size:
            fail(f"image appears empty or incomplete: {relative}")

    retired = [
        Path("assets/compass-badge.svg"),
        Path("assets/generated/working-tools-editorial-v01.png"),
        Path("assets/generated/working-tools-editorial-v01.jpg"),
        Path("site.js"),
    ]
    for path in retired:
        if (ROOT / path).exists():
            fail(f"retired asset is still present: {path}")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.name == ".DS_Store" or path.name.startswith("._"):
            fail(f"sidecar file found: {path.relative_to(ROOT)}")


def validate_public_text() -> None:
    text_files = [
        *PAGE_FILES,
        Path("styles.css"),
        Path("assets/css/tokens.css"),
        Path("assets/css/base.css"),
        Path("assets/css/layout.css"),
        Path("assets/css/components.css"),
        Path("assets/css/collection.css"),
        Path("assets/css/responsive.css"),
        Path("assets/js/main.js"),
        Path("assets/js/site-nav.js"),
        Path("assets/js/collection.js"),
        Path("assets/js/catalog.js"),
        Path("content/site-copy.md"),
        Path("data/tool-library.json"),
        Path("suite-manifest.json"),
        Path("snippets/universal-footer.html"),
    ]
    combined = "\n".join(read(path) for path in text_files)
    forbidden = [
        "/Volumes/",
        "/Users/",
        "compass-badge",
        "Choose the right Compass",
        "compass-public-visual-system: uxhc-v1",
        "working-tools-editorial",
        "#e7ff32",
        "--highlight",
        "Connected service",
        "Local system",
        "MCP collection",
        "plugin collection",
        ".DS_Store",
    ]
    for string in forbidden:
        if string.lower() in combined.lower():
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
        'class="hero-specimen"',
        'type="module"',
    ]:
        if required not in home:
            fail(f"homepage contract missing: {required}")

    for page in CORE_PAGES:
        text = read(page)
        for required in ["skip-link", "site-header", "site-footer", "working-tools-favicon-32.png"]:
            if required not in text:
                fail(f"{page} missing shared shell requirement: {required}")

    for slug, page in zip(COLLECTION_SLUGS, COLLECTION_PAGES):
        text = read(page)
        required = [
            "skip-link",
            "site-header",
            "collection-hero",
            "collection-specimen",
            "Starting prompt",
            "Good fit",
            "Not a substitute for",
            f"downloads/{'builder-tools-vibe-check' if slug == 'builder-tools' else slug}-claude-plugin.zip",
            "Download plugin ZIP",
        ]
        for contract in required:
            if contract not in text:
                fail(f"{page} missing collection-page requirement: {contract}")

    audit = ImageAudit()
    audit.feed(home)
    if len(audit.images) != 9:
        fail(f"expected 9 functional install images, found {len(audit.images)}")
    for image in audit.images:
        if "alt" not in image or not image["alt"].strip():
            fail(f"homepage image missing useful alt text: {image.get('src', 'unknown')}")
        if image.get("loading") != "lazy":
            fail(f"install screenshot must be lazy-loaded: {image.get('src', 'unknown')}")


def validate_css_and_js() -> None:
    css = "\n".join(
        read(path)
        for path in [
            "assets/css/tokens.css",
            "assets/css/base.css",
            "assets/css/layout.css",
            "assets/css/components.css",
            "assets/css/collection.css",
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
        ".collection-hero",
        ".collection-specimen",
        "--signal: #d95d3a",
        "--signal-wash: #efd8ce",
    ]:
        if contract not in css:
            fail(f"CSS contract missing: {contract}")
    if "fonts.googleapis.com" in css or "gradient(" in css:
        fail("visual system must remain dependency-light and gradient-free")

    js = read("assets/js/catalog.js") + read("assets/js/main.js") + read("assets/js/site-nav.js")
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
    if library.get("schema_version") != "working-tools.library.v2":
        fail("unexpected tool library schema")
    if library.get("public_only") is not True:
        fail("tool library must declare public_only")
    labels = library.get("access_labels", {})
    if set(labels) != ALLOWED_ACCESS:
        fail(f"access label set changed: {sorted(labels)}")
    items = library.get("items", [])
    if len(items) != len(EXPECTED_LIBRARY_IDS):
        fail(f"expected {len(EXPECTED_LIBRARY_IDS)} public records, found {len(items)}")
    ids = [item.get("id") for item in items]
    if set(ids) != EXPECTED_LIBRARY_IDS or len(ids) != len(set(ids)):
        fail(f"public catalog identity changed: {sorted(set(ids))}")

    for item in items:
        access = item.get("access")
        if access not in ALLOWED_ACCESS:
            fail(f"unknown or non-public access label on {item['id']}: {access}")
        jobs = set(item.get("jobs", []))
        if not jobs or not jobs.issubset(ALLOWED_JOBS):
            fail(f"invalid or empty job mapping on {item['id']}: {sorted(jobs)}")
        href = item.get("href")
        action = item.get("action")
        if not href or not href.startswith("https://") or not action:
            fail(f"public record lacks a verified HTTPS action: {item['id']}")
        public_blob = json.dumps(item)
        if "/Volumes/" in public_blob or "/Users/" in public_blob:
            fail(f"local path exposed in catalog record: {item['id']}")


def check_url(url: str) -> None:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "WorkingToolsValidator/2.0"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            if response.status >= 400:
                fail(f"URL returned HTTP {response.status}: {url}")
    except urllib.error.HTTPError as exc:
        if exc.code not in {403, 405}:
            fail(f"URL returned HTTP {exc.code}: {url}")
        fallback = urllib.request.Request(url, headers={"User-Agent": "WorkingToolsValidator/2.0", "Range": "bytes=0-0"})
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
    urls.update(item["href"] for item in library["items"])
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
