from pathlib import Path

from playwright.async_api import async_playwright

from .downloader import download_series, find_items
from .models import Section
from .sections import SECTIONS

CONCURRENCY = 4
DOWNLOAD_ROOT = Path(__file__).resolve().parents[1] / "download"


def choose_section() -> Section:
    choices = {section.key: section for section in SECTIONS}
    menu = ", ".join(f"{section.label} ({section.key})" for section in SECTIONS)
    while True:
        key = input(f"Download which items? {menu}: ").strip().lower()
        if key in choices:
            return choices[key]
        print(f"Choose one of: {', '.join(choices)}")


def print_banner(message: str):
    print("=" * len(message))
    print(message)
    print("=" * len(message))


async def main():
    url = input("Enter the ElSci One series URL: ").strip()
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False, slow_mo=50)
        try:
            context = await browser.new_context(accept_downloads=True)
            page = await context.new_page()
            await page.goto(url)
            series = (await page.locator("a.crumb.active span.label").inner_text()).strip()
            print_banner(f"Series: {series}")
            section = choose_section()
            count = await find_items(page, section).count()
            print(f"Found {count} {section.label} items.")
            await page.close()
            destination = DOWNLOAD_ROOT / section.file_type.directory / series
            await download_series(context, url, count, section, destination, CONCURRENCY)
            print_banner("All downloads completed.")
        finally:
            await browser.close()
