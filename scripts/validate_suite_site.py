#!/usr/bin/env python3
"""Validate the Compass Suite static storefront before publishing."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCAL_VOLUME_PATH = "/" + "Volumes/"
LOCAL_USER_PATH = "/" + "Users/"
UNFILLED_SENTINEL = "PLACE" + "HOLDER"
PUBLIC_FILES = [
    ROOT / "index.html",
    ROOT / "404.html",
    ROOT / "about" / "index.html",
    ROOT / "license" / "index.html",
    ROOT / "styles.css",
    ROOT / "site.js",
    ROOT / "suite-manifest.json",
    ROOT / "snippets" / "universal-footer.html",
    ROOT / "legal" / "LICENSE-DOCS-CC-BY-SA-4.0.md",
    ROOT / "legal" / "NOTICE.md",
    ROOT / "legal" / "BRAND-AND-ATTRIBUTION.md",
    ROOT / "legal" / "THIRD_PARTY_NOTICES.md",
]

FORBIDDEN_STRINGS = [
    "About & FAQ",
    "About &amp; FAQ",
    UNFILLED_SENTINEL,
    "v0.1.0-beta.7",
    "v0.1.0-beta.8",
    "v0.1.0-beta.9",
    LOCAL_VOLUME_PATH,
    LOCAL_USER_PATH,
    "._",
    ".DS_Store",
    "Download + Learn",
]

REQUIRED_STRINGS = [
    "Not sure what to download?",
    "Claude Code / Cowork Plugin",
    "Claude Desktop Extension",
    "Download and Open Guide",
    "AI Basics",
    "https://jonathankhobson.github.io/shareables/s/understanding-ai-2026/",
    "MCP Basics",
    "Check Back for Public Package",
    "Download started. Guide opened.",
    "Codex can work with these local packages and source zips",
    "Codex can work with local Compass source packages when configured manually",
    "suite-footer",
    "Compass Suite is created and maintained by Jonathan Kyle Hobson.",
    "About the Author",
    "License &amp; Attribution",
    "AGPL-3.0-only",
    "CC BY-SA 4.0",
]

PRIVATE_HINTS = [
    "resume.pdf",
    "cover-letter",
    "phone",
    "gmail.com",
    "employer-specific",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_manifest() -> dict:
    try:
        return json.loads(read(ROOT / "suite-manifest.json"))
    except json.JSONDecodeError as exc:
        fail(f"suite-manifest.json is invalid JSON: {exc}")


def validate_static_text() -> None:
    combined = "\n".join(read(path) for path in PUBLIC_FILES)
    for forbidden in FORBIDDEN_STRINGS:
        if forbidden in combined:
            fail(f"forbidden string found in public files: {forbidden}")
    for required in REQUIRED_STRINGS:
        if required not in combined:
            fail(f"required storefront hardening string missing: {required}")

    styles = read(ROOT / "styles.css")
    if "compass-public-visual-system: uxhc-v1" not in styles:
        fail("shared Compass visual-system marker missing from styles.css")
    for required_css in [
        "overflow-x: hidden",
        ".site-nav-toggle",
        ".section-nav-toggle",
        ".js-enabled .site-nav-links",
        ".download-chooser",
        ".sr-only",
        ".suite-footer-grid",
    ]:
        if required_css not in styles:
            fail(f"mobile/accessibility containment CSS missing: {required_css}")

    for page in [ROOT / "index.html", ROOT / "404.html", ROOT / "about" / "index.html", ROOT / "license" / "index.html"]:
        text = read(page)
        for required_footer in [
            'class="site-nav-toggle"',
            'class="suite-footer"',
            'role="contentinfo"',
            'aria-label="Compass network footer"',
            "https://jonathankhobson.github.io/compass-suite/about/",
            "https://jonathankhobson.github.io/compass-suite/license/",
            "https://www.linkedin.com/in/jonathankylehobson/",
        ]:
            if required_footer not in text:
                fail(f"{page.relative_to(ROOT)} missing universal footer requirement: {required_footer}")

    html = read(ROOT / "index.html")
    expected_card_order = [
        "critical-compass",
        "prompt-compass",
        "ux-heuristics-compass",
        "ttrpg-compass",
        "research-compass",
        "job-application-compass",
    ]
    card_order = re.findall(r'data-product-id="([^"]+)"', html)
    if card_order != expected_card_order:
        fail(f"product card order mismatch: got {card_order}, expected {expected_card_order}")

    product_grid_pos = html.find('class="product-grid"')
    chooser_pos = html.find('class="download-chooser"')
    if chooser_pos == -1 or product_grid_pos == -1 or chooser_pos < product_grid_pos:
        fail("download chooser must appear after the product grid so available Compasses are seen first")

    for href in [
        "https://jonathankhobson.github.io/what-is-an-mcp/",
        "https://jonathankhobson.github.io/what-is-an-mcp/#mcp-risks",
    ]:
        if href in html and f'href="{href}" target="_blank" rel="noopener"' not in html:
            fail(f"MCP explainer link must open in a new tab: {href}")
    if 'href="https://jonathankhobson.github.io/shareables/s/understanding-ai-2026/" target="_blank"' in html:
        fail("AI Basics links should use same-tab Compass network navigation")

    job_section = re.search(
        r'data-product-id="job-application-compass".*?</article>',
        html,
        flags=re.DOTALL,
    )
    if not job_section:
        fail("Job Application Compass card missing")
    job_text = job_section.group(0).lower()
    for hint in PRIVATE_HINTS:
        if hint in job_text:
            fail(f"Job Application Compass card contains private-data hint: {hint}")

    error_page = read(ROOT / "404.html")
    for recovery_link in [
        "https://jonathankhobson.github.io/compass-suite/",
        "https://jonathankhobson.github.io/critical-compass/",
        "https://jonathankhobson.github.io/prompt-compass/",
        "https://jonathankhobson.github.io/ux-heuristic-compass/",
        "https://jonathankhobson.github.io/what-is-an-mcp/",
    ]:
        if recovery_link not in error_page:
            fail(f"404 recovery link missing: {recovery_link}")

    for sidecar in ROOT.rglob("*"):
        if ".git" in sidecar.parts or "__pycache__" in sidecar.parts:
            continue
        if sidecar.name == ".DS_Store" or sidecar.name.startswith("._"):
            fail(f"sidecar file found: {sidecar.relative_to(ROOT)}")


def validate_tabs() -> None:
    html = read(ROOT / "index.html")
    labels = re.findall(r'data-tab-target="[^"]+">([^<]+)</button>', html)
    expected = ["Get Started", "About", "Install Guide", "FAQ"]
    if labels != expected:
        fail(f"tab labels/order mismatch: got {labels}, expected {expected}")
    for disallowed in ["Example", "Advanced"]:
        if f">{disallowed}</button>" in html:
            fail(f"V1 suite site must not include {disallowed} tab")


def validate_manifest_parity(manifest: dict) -> None:
    html = read(ROOT / "index.html")
    products = manifest.get("products", [])
    if len(products) != 6:
        fail(f"expected 6 Compass products, found {len(products)}")

    manifest_order = [product.get("id") for product in products]
    expected_order = [
        "critical-compass",
        "prompt-compass",
        "ux-heuristics-compass",
        "ttrpg-compass",
        "research-compass",
        "job-application-compass",
    ]
    if manifest_order != expected_order:
        fail(f"manifest product order mismatch: got {manifest_order}, expected {expected_order}")

    ids = {product.get("id") for product in products}
    expected_ids = {
        "critical-compass",
        "prompt-compass",
        "ttrpg-compass",
        "research-compass",
        "job-application-compass",
        "ux-heuristics-compass",
    }
    if ids != expected_ids:
        fail(f"product ids mismatch: got {sorted(ids)}, expected {sorted(expected_ids)}")

    for product in products:
        product_id = product["id"]
        if f'data-product-id="{product_id}"' not in html:
            fail(f"product card missing from HTML: {product_id}")

        downloads = product.get("downloads", [])
        if product_id in {
            "ttrpg-compass",
            "research-compass",
            "job-application-compass",
        } and downloads:
            fail(f"{product_id} must not expose downloads before its public gate clears")

        if product_id == "job-application-compass":
            gate = product.get("safety_gate", "")
            if "privacy_scrub_required" not in gate:
                fail("Job Application Compass manifest must require privacy scrub")

        for download in downloads:
            url = download.get("url", "")
            checksum = download.get("checksum", "")
            filename = download.get("filename", "")
            if not url or not url.startswith("https://"):
                fail(f"{product_id} download has invalid URL: {filename}")
            if url not in html:
                fail(f"{product_id} download URL missing from HTML: {filename}")
            if not re.fullmatch(r"[a-f0-9]{64}", checksum):
                fail(f"{product_id} checksum is not a SHA-256 hex digest: {filename}")
            if download.get("availability") != "available":
                fail(f"{product_id} downloadable asset is not marked available: {filename}")

    download_links = re.findall(r'<a [^>]*data-download-url="([^"]+)"[^>]*data-learn-url="([^"]+)"', html)
    if len(download_links) != 15:
        fail(f"expected 15 enhanced download links, found {len(download_links)}")


def check_url(url: str) -> None:
    request = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "CompassSuiteValidator/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status >= 400:
                fail(f"URL returned HTTP {response.status}: {url}")
    except urllib.error.HTTPError as exc:
        if exc.code not in {403, 405}:
            fail(f"URL returned HTTP {exc.code}: {url}")
        fallback = urllib.request.Request(
            url,
            headers={
                "User-Agent": "CompassSuiteValidator/1.0",
                "Range": "bytes=0-0",
            },
        )
        with urllib.request.urlopen(fallback, timeout=20) as response:
            if response.status >= 400:
                fail(f"URL returned HTTP {response.status}: {url}")
    except urllib.error.URLError as exc:
        fail(f"URL check failed for {url}: {exc}")


def validate_links(manifest: dict) -> None:
    urls = {
        "https://jonathankhobson.github.io/critical-compass/",
        "https://jonathankhobson.github.io/prompt-compass/",
        "https://jonathankhobson.github.io/what-is-an-mcp/",
    }
    for product in manifest.get("products", []):
        for key in ("homepage_url", "repo_url", "learn_more_url"):
            value = product.get(key)
            if value and value.startswith("https://"):
                urls.add(value)
        for download in product.get("downloads", []):
            urls.add(download["url"])

    for url in sorted(urls):
        check_url(url)
        print(f"OK: {url}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-links", action="store_true", help="verify public URLs over the network")
    args = parser.parse_args()

    manifest = load_manifest()
    validate_static_text()
    validate_tabs()
    validate_manifest_parity(manifest)
    if args.check_links:
        validate_links(manifest)

    print("Compass Suite storefront validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
