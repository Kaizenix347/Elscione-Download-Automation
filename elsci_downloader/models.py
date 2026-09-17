from dataclasses import dataclass

@dataclass(frozen=True)
class FileType:
    extension: str
    directory: str
    modal_selectors: tuple[str, ...] = ()

    @property
    def download_selector(self) -> str:
        return ", ".join((*self.modal_selectors, f'a[download][href$="{self.extension}"]'))

@dataclass(frozen=True)
class Section:
    key: str
    label: str
    file_type: FileType
    tag: str = ""

    @property
    def match_text(self) -> str:
        return f"{self.tag}{self.file_type.extension}"
