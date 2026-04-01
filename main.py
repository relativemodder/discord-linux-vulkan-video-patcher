import sys
from pathlib import Path

from src.detect import resolve_installations
from src.patcher import patch
from src.ui import clear, print_error, print_header, print_installations, prompt_choice


def main():
    source_file = Path(__file__).parent / "index.js"

    clear()
    print_header()

    if not source_file.exists():
        print_error(
            "index.js not found next to this script.",
            hint=f"Expected: {source_file}",
        )
        sys.exit(1)

    installations = resolve_installations()
    print_installations(installations)

    target = prompt_choice(installations)
    if target is None:
        sys.exit(0)

    patch(target, source_file)


if __name__ == "__main__":
    main()
