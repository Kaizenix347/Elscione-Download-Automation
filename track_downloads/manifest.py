import json
from pathlib import Path
from typing import Any, cast


def load_manifest(path: str) -> dict[str, Any]:
    """Load a manifest, returning an empty dictionary if the file is missing."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            loaded_manifest = json.load(f)
    except FileNotFoundError:
        return {}

    if not isinstance(loaded_manifest, dict):
        raise ValueError(f"Manifest file at {path} must contain a JSON object.")
    return cast(dict[str, Any], loaded_manifest)


def save_manifest(path: str, records: dict[str, Any]) -> None:
    """Save records through a temporary file; propagate write failures.

    The parent directory must exist. Use one writer at a time.
    """
    manifest_path = Path(path)
    temporary = manifest_path.with_name(manifest_path.name + '.tmp')
    temporary.write_text(
        json.dumps(records, indent=4),
        encoding='utf-8',
    )
    temporary.replace(manifest_path)


def ensure_record(records: dict[str, Any], item_id: str, url: str) -> None:
    """Add a pending record without resetting existing progress."""
    if item_id not in records:
        records[item_id] = {
            "url": url,
            "path": None,
            "status": "pending",
            "attempts": 0,
            "size_bytes": None,
            "last_error": None,
        }
