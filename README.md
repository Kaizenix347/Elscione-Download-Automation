# Installation from Scratch

This requires Python **3.10 or newer**.

Make sure that your terminal is in the same folder level where elsci-4.py is located.

For a fresh install, follow these commands:

```sh
# Create a fresh virtual environment
py -m venv .venv

# Install Playwright and its browser
.\.venv\Scripts\python.exe -m pip install playwright
.\.venv\Scripts\python.exe -m playwright install chromium

# Run the downloader
.\.venv\Scripts\python.exe .\elsci-4.py
```

## How to Use the Downloader

When you run the code, you will be prompted in the terminal

```sh
Enter the ElSci One series URL:
```

Enter the URL.

The next step requires a manual step where you choose which file you want to download: EPUB or audiobook. For EPUB, you have 4 different options; follow the terminal prompt after inputting the ElSci URL. After a pop-up, a browser will appear, and it will automatically download all the files associated with the EPUB type or audiobook type you entered.

Lastly, the browser will close after all the downloads are complete.

## Where to Find the Download Folder

It should be located at the same folder level as elsci-4.py, in a folder called "download".

## Add a section

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

## Add a file type

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

Run the offline checks with:

```sh
python -m unittest discover -s ./tests
```
