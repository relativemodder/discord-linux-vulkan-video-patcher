import os
from pathlib import Path
from typing import Callable

from .models import Installation

CANDIDATES: list[tuple[str, Callable[[Path], Path]]] = [
    ("Discord (Standard)", lambda h: h / ".config/discord"),
    ("Discord Canary (Standard)", lambda h: h / ".config/discordcanary"),
    (
        "Discord (Flatpak)",
        lambda h: h / ".var/app/com.discordapp.Discord/config/discord",
    ),
    (
        "Discord Canary (Flatpak)",
        lambda h: h / ".var/app/com.discordapp.DiscordCanary/config/discordcanary",
    ),
    (
        "Discord (Snap)",
        lambda h: h / "snap/discord/current/.config/discord",
    ),
    (
        "Discord Canary (Snap)",
        lambda h: h / "snap/discord-canary/current/.config/discordcanary",
    ),
]


def find_version_dir(app_path: Path) -> Path | None:
    versions = [d for d in app_path.iterdir() if d.is_dir() and d.name[0].isdigit()]
    if not versions:
        return None
    return max(versions, key=os.path.getmtime)


def resolve_installations(home: Path | None = None) -> list[Installation]:
    home = home or Path.home()
    results: list[Installation] = []

    for label, path_fn in CANDIDATES:
        path = path_fn(home)

        if not path.exists():
            results.append(
                Installation(
                    label=label, path=path, ver_dir=None, patchable=False, found=False
                )
            )
            continue

        ver_dir = find_version_dir(path)
        voice_dir = ver_dir / "modules" / "discord_voice" if ver_dir else None
        target_file = voice_dir / "index.js" if voice_dir else None

        results.append(
            Installation(
                label=label,
                path=path,
                ver_dir=ver_dir,
                patchable=bool(target_file and target_file.exists()),
                found=True,
            )
        )

    return results
