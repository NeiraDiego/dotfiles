#!/bin/bash

chosen=$(printf " Lock\n Suspend\n Reboot\n Shutdown\n Logout" | \
    wofi --dmenu --prompt "Power Menu")

case "$chosen" in
    " Lock")     hyprctl dispatch exit ;;   # aquí puedes poner tu locker preferido
    " Suspend")  systemctl suspend ;;
    " Reboot")   systemctl reboot ;;
    " Shutdown") systemctl poweroff ;;
    " Logout")   hyprctl dispatch exit ;;
esac

