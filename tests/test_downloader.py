import asyncio
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from elsci_downloader import downloader
from elsci_downloader.models import FileType, Section
from elsci_downloader.sections import SECTIONS


class ConfigurationTests(unittest.TestCase):
    def test_existing_sections(self):
        self.assertEqual(
            {s.key: (s.match_text, s.file_type.directory) for s in SECTIONS},
            {"k": ("[Kobo].epub", "epub"),
             "ki": ("[Kindle].epub", "epub"),
             "p": ("[Premium].epub", "epub"),
             "s": ("[Seven Seas].epub", "epub"),
             "a": (".m4b", "audiobooks")},
        )

    def test_new_format_uses_shared_filter_and_selector(self):
        section = Section("pdf", "PDF", FileType(".pdf", "pdf"))
        page = MagicMock()
        downloader.find_items(page, section)
        page.locator.return_value.filter.assert_called_once_with(has_text=".pdf")
        self.assertEqual(section.file_type.download_selector, 'a[download][href$=".pdf"]')


class DownloadTests(unittest.IsolatedAsyncioTestCase):
    async def test_page_closes_when_navigation_fails(self):
        page = AsyncMock()
        page.goto.side_effect = RuntimeError("navigation failed")
        context = AsyncMock()
        context.new_page.return_value = page
        with self.assertRaisesRegex(RuntimeError, "navigation failed"):
            await downloader.download_item(context, "url", 0, SECTIONS[0], Path("unused"))
        page.close.assert_awaited_once()

    async def test_batches_are_bounded_and_cover_all_items(self):
        active = peak = 0
        visited = []

        async def download(context, url, index, section, destination):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            visited.append(index)
            await asyncio.sleep(0)
            active -= 1

        with tempfile.TemporaryDirectory() as folder:
            with patch.object(downloader, "download_item", side_effect=download):
                await downloader.download_series(None, "url", 9, SECTIONS[0], Path(folder), 4)
        self.assertEqual(sorted(visited), list(range(9)))
        self.assertEqual(peak, 4)


if __name__ == "__main__":
    unittest.main()
