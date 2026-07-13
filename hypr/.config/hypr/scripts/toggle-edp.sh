#!/bin/bash
MONITOR="eDP-1"

hyprctl monitors -j | jq -e ".[] | select(.name == \"$MONITOR\") | select(.disabled == false)" > /dev/null
if [[ $? -eq 0 ]]; then
    hyprctl eval "hl.monitor({ output = \"$MONITOR\", disabled = true })"
else
    hyprctl eval "hl.monitor({ output = \"$MONITOR\", disabled = false, mode = \"preferred\", position = \"0x0\", scale = 1.175 })"
fi
