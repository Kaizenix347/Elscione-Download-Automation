"""Register sections here to add them to the menu and downloader."""
from .kobo import KOBO
from .kindle import KINDLE
from .premium import PREMIUM
from .seven_seas import SEVEN_SEAS
from .audiobook import AUDIOBOOK

SECTIONS = (KOBO, KINDLE, PREMIUM, SEVEN_SEAS, AUDIOBOOK)

if len({section.key for section in SECTIONS}) != len(SECTIONS):
    raise ValueError("Section keys must be unique")
