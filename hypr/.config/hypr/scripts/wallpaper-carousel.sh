#!/usr/bin/env bash
WALLPAPER_DIR="/home/diego/Pictures/Wallpapers_rotation"
DELAY=1200

while true; do
    img=$(find "$WALLPAPER_DIR" -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.bmp' \) | shuf -n 1)
    if [[ -n "$img" ]]; then
        killall swaybg 2>/dev/null
        swaybg -i "$img" -m fill &
    fi
    sleep "$DELAY"
done
