#!/bin/bash

# Map modifier masks to human-readable names
modmask_to_str() {
    local mask=$1
    local parts=""
    (( mask & 64 )) && parts+="SUPER "
    (( mask & 8 ))  && parts+="ALT "
    (( mask & 4 ))  && parts+="CTRL "
    (( mask & 1 ))  && parts+="SHIFT "
    echo "$parts" | sed 's/ $//'
}

hyprctl -j binds | jq -r '.[] | select(.submap == null or .submap == "") | {modmask, key, dispatcher, arg} | [.modmask, .key, .dispatcher, (.arg // "")] | @tsv' |
while IFS=$'\t' read -r modmask key dispatcher arg; do
    modstr=$(modmask_to_str "$modmask")
    [[ -n $modstr ]] && combo="${modstr} + $key" || combo="$key"
    action="$dispatcher${arg:+ $arg}"
    printf "%-35s %s\n" "$combo" "$action"
done | wofi --show dmenu -p "Keybinds" -W 800 -H 600
