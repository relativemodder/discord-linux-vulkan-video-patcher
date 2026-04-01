#!/bin/bash
set -e

TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

curl -L https://github.com/relativemodder/discord-linux-vulkan-video-patcher/archive/refs/heads/main.tar.gz | tar xz --strip-components=1

if command -v python3 &>/dev/null; then
    python3 main.py
elif command -v python &>/dev/null; then
    python main.py
else
    echo "Error: Python is not installed."
    exit 1
fi

rm -rf "$TMP_DIR"
