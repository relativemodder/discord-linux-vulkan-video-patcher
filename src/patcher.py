import os
import shutil
import stat
from pathlib import Path

from .models import Installation
from .ui import (
    print_error,
    print_patch_header,
    print_patch_result,
    print_patch_skip,
    print_success,
)

PERMISSION_TARGETS = ("gpu_encoder_helper", "discord_voice.node")


def patch(inst: Installation, source_file: Path) -> None:
    if inst.ver_dir is None:
        print_error(f"Version directory not found for {inst.label}")
        return

    voice_dir = inst.ver_dir / "modules" / "discord_voice"
    target = voice_dir / "index.js"

    print_patch_header(inst)

    try:
        shutil.copy2(source_file, target)
        print_patch_result(ok=True, filename="Copied index.js")

        for filename in PERMISSION_TARGETS:
            filepath = voice_dir / filename
            if filepath.exists():
                st = os.stat(filepath)
                os.chmod(filepath, st.st_mode | stat.S_IEXEC)
                print_patch_result(
                    ok=True, filename=f"Set executable bit on {filename}"
                )
            else:
                print_patch_skip(filename)

        print_success()

    except Exception as e:
        print_error(str(e))
