#!/usr/bin/env python3
"""Render cover.html / illustrations.html to PNG via Playwright.

Usage:
    python3 render_pngs.py content/<slug>
"""
import sys
import os
from pathlib import Path
from playwright.sync_api import sync_playwright


def render(slug_dir: Path):
    cover_html = slug_dir / "cover.html"
    illu_html = slug_dir / "illustrations.html"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(device_scale_factor=2, viewport={"width": 1200, "height": 900})

        if cover_html.exists():
            page = context.new_page()
            page.goto(cover_html.resolve().as_uri())
            page.wait_for_load_state("networkidle")
            el = page.locator("#cover-main")
            out = slug_dir / "cover.png"
            el.screenshot(path=str(out), omit_background=False)
            print(f"  ✓ {out}")
            page.close()

        if illu_html.exists():
            page = context.new_page()
            page.goto(illu_html.resolve().as_uri())
            page.wait_for_load_state("networkidle")
            slides = page.locator(".slide")
            count = slides.count()
            for i in range(count):
                out = slug_dir / f"配图-{i + 1}.png"
                slides.nth(i).screenshot(path=str(out), omit_background=False)
                print(f"  ✓ {out}")
            page.close()

        browser.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: render_pngs.py <content_dir>")
        sys.exit(1)
    render(Path(sys.argv[1]))
