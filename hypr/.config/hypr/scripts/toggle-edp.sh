#!/bin/bash
MONITOR="eDP-1"

hyprctl monitors -j | jq -e ".[] | select(.name == \"$MONITOR\") | select(.disabled == false)" > /dev/null
if [[ $? -eq 0 ]]; then
    hyprctl keyword monitor "$MONITOR, disable"
else
    hyprctl keyword monitor "$MONITOR, preferred, 1920x0, 1.175"
fi
