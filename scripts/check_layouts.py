#!/usr/bin/env python3
"""Browser-based checks/screenshots for CROSSGLINT GitHub Pages responsive layout.

Runs locally on CI's Google Chrome. It does not require downloading browser
binaries or contacting any external website.
"""
import argparse
from pathlib import Path
import shutil

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BROWSER = (
    shutil.which("google-chrome")
    or shutil.which("chromium")
    or shutil.which("chromium-browser")
)

def bounds(page, selector):
    result = page.locator(selector).bounding_box()
    if result is None:
        raise AssertionError(f"Element not laid out: {selector}")
    return result

def validate(page, label, is_home, wide):
    overflow = page.evaluate(
        "document.documentElement.scrollWidth > window.innerWidth + 2"
    )
    assert not overflow, f"{label}: page overflows horizontally"
    assert page.locator("main").count() == 1, f"{label}: main missing"
    assert page.locator(".brand-lockup").is_visible(), f"{label}: header missing"

    if not is_home:
        assert page.locator(".policy-sheet").count() == 2
        assert page.locator("#english").count() == 1
        return

    copy = bounds(page, ".hero-copy")
    art = bounds(page, ".hero-art")
    product = bounds(page, ".product-card")
    contact = bounds(page, ".contact-panel")
    banner = page.locator(".hero-banner")
    symbol = page.locator(".hero-symbol")
    desktop_wordmark = page.locator(".hero-desktop-wordmark")
    if wide:
        assert copy["x"] + copy["width"] <= art["x"] + 3, (
            f"{label}: hero must put introduction to left of brand art"
        )
        assert abs(copy["y"] - art["y"]) < 10
        assert product["x"] + product["width"] <= contact["x"] + 4, (
            f"{label}: cards are not side by side"
        )
        assert symbol.is_visible() and not banner.is_visible()
        assert desktop_wordmark.is_visible(), f"{label}: brand wordmark missing"
    else:
        assert art["y"] + art["height"] <= copy["y"] + 3, (
            f"{label}: original mobile banner order changed"
        )
        assert product["y"] + product["height"] < contact["y"] + 4, (
            f"{label}: phone cards must be stacked"
        )
        assert banner.is_visible() and not symbol.is_visible()
        assert not desktop_wordmark.is_visible()
    assert page.locator("a[href^='mailto:']").count() >= 2
    assert page.locator(".product-actions a[href='privacy.html']").count() == 1

def run(output):
    assert BROWSER, "Google Chrome/Chromium required for browser layout checks"
    output.mkdir(parents=True, exist_ok=True)
    cases = [
        ("phone", 390, 844, False),
        ("tablet", 820, 1000, False),
        ("desktop", 1440, 900, True),
        ("desktop-900", 900, 900, True),
    ]
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True, executable_path=BROWSER,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        for name, width, height, wide in cases:
            page = browser.new_page(
                viewport={"width": width, "height": height},
                device_scale_factor=1,
                is_mobile=name == "phone",
                has_touch=name == "phone",
            )
            for suffix, filename in (("", "index.html"), ("-privacy", "privacy.html")):
                page.goto((ROOT / filename).as_uri(), wait_until="load")
                page.locator("img").first.wait_for(state="visible")
                errors = page.evaluate(
                    """() => Array.from(document.images)
                      .filter(img => img.offsetWidth > 0 && !img.complete)
                      .map(img => img.src)"""
                )
                assert not errors, f"{name}{suffix}: unloaded images: {errors}"
                validate(page, name + suffix, filename == "index.html", wide)
                if name in ("phone", "desktop"):
                    page.screenshot(
                        path=str(output / f"{name}{suffix}.png"),
                        full_page=True,
                        animations="disabled"
                    )
            page.close()
        browser.close()
    print("Responsive checks passed at 390px, 820px, 900px, 1440px.")
    print("Saved phone/desktop screenshots for PR review in", output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    run(args.output)
