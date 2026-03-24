import os
import shutil
import stat
from pathlib import Path


def run_patcher():
    h = Path.home()
    options = {
        "1": h / ".config/discord",
        "2": h / ".config/discordcanary",
        "3": h / ".var/app/com.discordapp.Discord/config/discord",
        "4": h / ".var/app/com.discordapp.DiscordCanary/config/discordcanary",
    }

    print("Select target:")
    print("1. Discord (Standard)")
    print("2. Discord Canary (Standard)")
    print("3. Discord (Flatpak)")
    print("4. Discord Canary (Flatpak)")

    choice = input("> ")
    app_path = options.get(choice)

    if not app_path or not app_path.exists():
        print("Error: Directory not found.")
        return

    versions = [d for d in app_path.iterdir() if d.is_dir() and d.name[0].isdigit()]
    if not versions:
        print("Error: No version folder found.")
        return

    target_dir = max(versions, key=os.path.getmtime)
    voice_dir = target_dir / "modules" / "discord_voice"
    target_file = voice_dir / "index.js"
    source_file = Path(__file__).parent / "index.js"

    if not source_file.exists():
        print(f"Error: {source_file} not found.")
        return

    if not target_file.exists():
        print("Error: Target module file not found.")
        return

    try:
        shutil.copy2(source_file, target_file)

        for filename in [
            "gpu_encoder_helper",
            "discord_voice.node",
        ]:  # these mfs are responsible for detection
            filepath = voice_dir / filename
            if filepath.exists():
                st = os.stat(filepath)
                os.chmod(filepath, st.st_mode | stat.S_IEXEC)

        print(f"Successfully patched and set permissions: {target_dir.name}")
    except Exception as e:
        print(f"Failure: {e}")


if __name__ == "__main__":
    run_patcher()
