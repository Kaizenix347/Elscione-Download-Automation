"""Command-line entry point for the ElSci downloader."""
import asyncio
from elsci_downloader.app import main

if __name__ == "__main__":
    asyncio.run(main())
