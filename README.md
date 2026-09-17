# ElSci Downloader

A Python command-line tool that uses Playwright to download matching EPUB or
M4B audiobook files from an ElSci One series page. Choose a section in the
terminal, and the tool opens Chromium to download its files in batches of up to
four. Downloads are organized by format and series name.

## Installation

Requires **Python 3.10 or newer**. The commands below use Windows PowerShell.

Download or clone this repository, then open a terminal in the project folder
containing `elsci-4.py`.

```powershell
# Create a fresh virtual environment
py -m venv .venv

# Install Playwright and its browser
.\.venv\Scripts\python.exe -m pip install playwright
.\.venv\Scripts\python.exe -m playwright install chromium

# Run the downloader
.\.venv\Scripts\python.exe .\elsci-4.py
```

## How to Use the Downloader

1. Run the downloader using the command above.
2. At the following prompt, paste the URL of an ElSci One series page:

```text
Enter the ElSci One series URL:
```

3. Chromium opens and loads the series page. Return to the terminal to choose a
   section:

| Choice | Files |
| --- | --- |
| `k` | Kobo EPUBs |
| `ki` | Kindle EPUBs |
| `p` | Premium EPUBs |
| `s` | Seven Seas EPUBs |
| `a` | M4B audiobooks |

4. Leave the browser open while the tool downloads the matching files. Progress
   appears in the terminal, and the browser closes when the run ends.

## Where to Find the Download Folder

Files are saved inside the project's `download` folder:

```text
download/
  epub/<series name>/
  audiobooks/<series name>/
```

## Known limitations

- The tool depends on the site's current page layout and download controls.
  Site changes may require updates to the selectors.
- Failed downloads are not retried automatically. An error stops the run after
  the current batch finishes; files already saved remain in the download folder.
- Existing files are not skipped. Downloading a file with the same name into
  the same folder can overwrite it.
- Series names are used directly as folder names. Names containing characters
  that are invalid in file paths may cause a run to fail.

## Development

### Add a section

Create `elsci_downloader/sections/yen_press.py`:

```python
from ..file_types.epub import EPUB
from ..models import Section

YEN_PRESS = Section("y", "Yen Press", EPUB, "[Yen Press]")
```

In `sections/__init__.py`, import `YEN_PRESS` and append it to `SECTIONS`.
The menu, item filtering, and destination follow automatically. Keys must be
unique. Filtering matches the tag immediately followed by the extension;
an empty tag matches all items containing that extension.

### Add a file type

Create `elsci_downloader/file_types/pdf.py`:

```python
from ..models import FileType

PDF = FileType(".pdf", "pdf", ("#pdf-btn-download",))
```

Create and register a section using `PDF`, as above. Use the site's actual modal
button selectors, or omit the tuple for direct downloads. A download link
selector for the extension is generated automatically. Formats requiring a
different interaction than a direct download or preview modal need corresponding
handling in `downloader.py`.

`app.py` owns prompts and browser startup; `downloader.py` owns page interaction
and bounded batches; `models.py` defines the configuration objects.

### Run tests

Run the offline unit tests from the project folder:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s ./tests
```

These tests cover configuration, bounded download batches, and page cleanup on
navigation failure. They do not verify downloads against the live site.

## License

This project's source code is available under the [MIT License](LICENSE).
