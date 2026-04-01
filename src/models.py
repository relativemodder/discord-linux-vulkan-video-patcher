from dataclasses import dataclass
from pathlib import Path


@dataclass
class Installation:
    label: str
    path: Path
    ver_dir: Path | None
    patchable: bool
    found: bool
