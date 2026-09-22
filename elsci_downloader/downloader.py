import asyncio
from pathlib import Path
from urllib.parse import urljoin

from playwright.async_api import BrowserContext, Locator, Page, TimeoutError as PlaywrightTimeoutError

from .models import Section


def find_items(page: Page, section: Section):
    return page.locator(".item.file:visible").filter(has_text=section.match_text)


async def get_item_id(item: Locator, page_url: str) -> str:
    """Identify a file by its full source URL, independent of list position."""

    href = await item.locator("a").get_attribute("href")

    if not href or href.startswith("#"):
        raise ValueError("Download item has no usable file link")
    
    return urljoin(page_url, href)


async def download_item(context: BrowserContext, url: str, index: int, section: Section, destination: Path):
    page = await context.new_page()

    try:
        await page.goto(url)
        item = find_items(page, section).nth(index)
        item_id = await get_item_id(item, page.url)

        print(f"File ID: {item_id}")

        await item.scroll_into_view_if_needed()
        button = page.locator(section.file_type.download_selector).first

        # Listen before clicking so direct downloads are captured too.
        async with page.expect_download() as download_info:
            await item.click()
            try:
                await button.wait_for(state="visible", timeout=10000)
            except PlaywrightTimeoutError:
                # A direct download may already have started on the first click.
                pass
            else:
                await button.click()

        download = await download_info.value
        await download.save_as(destination / download.suggested_filename)
        print(f"Downloaded {download.suggested_filename}")
        
    finally:
        await page.close()


async def download_series(context: BrowserContext, url: str, count: int,
                          section: Section, destination: Path, concurrency: int):
    if concurrency < 1:
        raise ValueError("Concurrency must be at least 1")

    destination.mkdir(parents=True, exist_ok=True)

    for start in range(0, count, concurrency):
        # Allow every page in a batch to close before propagating failures.
        results = await asyncio.gather(
            *(download_item(context, url, index, section, destination)
              for index in range(start, min(start + concurrency, count))),
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, BaseException):
                raise result
