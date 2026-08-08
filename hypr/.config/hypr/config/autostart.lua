-- Autostart (UWSM)
-- Con UWSM las apps también pueden ir en ~/.config/autostart/ (XDG)
-- y las env vars del sistema en ~/.config/uwsm/env

hl.on("hyprland.start", function ()
    -- Compatible con UWSM (CachyOS)
    hl.exec_cmd("dbus-update-activation-environment --systemd --all")
    hl.exec_cmd("noctalia")
    hl.exec_cmd("xhost +SI:localuser:root")

    -- Tu workflow
    hl.exec_cmd("~/.config/hypr/scripts/wallpaper-carousel.sh")
    hl.exec_cmd("nm-applet")
    if IS_SERVER then
        hl.exec_cmd("sunshine")
    else
        hl.exec_cmd("brave")
        hl.exec_cmd("kitty -e tmux")
    end

    -- Barra/panel: noctalia (actual) o waybar, ver DECISIONS.md D1
    -- hl.exec_cmd("waybar")
end)
