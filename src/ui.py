import os
import sys

from .models import Installation

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"


def supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def c(code: str, text: str) -> str:
    if supports_color():
        return f"{code}{text}{RESET}"
    return text


def clear() -> None:
    os.system("clear")


def rule(char: str = "ᚑ", width: int = 52) -> str:
    return c(DIM, char * width)


def print_header() -> None:
    print()
    print(rule())
    print(c(BOLD, "  Discord Voice Patcher").center(60))
    print(rule())
    print()


def print_installations(installations: list[Installation]) -> None:
    print(c(BOLD, "  Detected installations:"))
    print()
    for i, inst in enumerate(installations, 1):
        idx = f"  [{i}]"
        if not inst.found:
            continue

        elif not inst.patchable:
            print(
                f"{c(YELLOW, idx)} {c(YELLOW, inst.label)}  {c(YELLOW, 'found, module missing')}"
            )
        else:
            ver = inst.ver_dir.name if inst.ver_dir else "?"
            print(
                f"{c(GREEN, idx)} {c(BOLD, inst.label)}  {c(GREEN, f'ready  ({ver})')}"
            )
    print()


def prompt_choice(installations: list[Installation]) -> Installation | None:
    patchable = [i for i, inst in enumerate(installations, 1) if inst.patchable]

    if not patchable:
        print(c(RED, "  No patchable Discord installation found."))
        print(c(DIM, "  Make sure Discord has been launched at least once."))
        print()
        return None

    valid = {str(i) for i in patchable} | {"q"}
    print(c(DIM, "  Select a target to patch, or [q] to quit."))
    print()

    while True:
        try:
            choice = input(c(BOLD, "  > ")).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return None

        if choice == "q":
            return None
        if choice in valid:
            return installations[int(choice) - 1]

        print(c(YELLOW, f"  Invalid choice. Enter one of: {', '.join(sorted(valid))}"))


def print_patch_header(inst: Installation) -> None:
    print()
    print(rule())
    print(c(BOLD, f"  Patching: {inst.label}"))
    print(c(DIM, f"  Version:  {inst.ver_dir.name if inst.ver_dir else 'N/A'}"))
    print(rule())
    print()


def print_patch_result(
    ok: bool, filename: str | None = None, message: str | None = None
) -> None:
    if ok:
        print(f"  {c(GREEN, 'OK')}  {filename}")
    else:
        print(c(RED, f"  {message}"))


def print_patch_skip(filename: str) -> None:
    print(f"  {c(DIM, '--')}  {filename} not present, skipping")


def print_success() -> None:
    print()
    print(c(GREEN, c(BOLD, "  Patch applied successfully. Happy streaming!")))
    print()


def print_error(message: str, hint: str | None = None) -> None:
    print(c(RED, f"  Failed: {message}"))
    if hint:
        print(c(DIM, f"  {hint}"))
    print()
