-- Keybinds (migrados desde dotfiles)
-- Binds exclusivos de CachyOS quedan comentados con referencia a DECISIONS.md

local mainMod = "SUPER"


---------------------------
---- MONITORS TOGGLE ------
---------------------------

-- Toggle eDP-1 laptop monitor (solo en PC con laptop)
if not IS_SERVER then
    function toggleEDP()
        local mon = hl.get_monitor("eDP-1")
        if mon ~= nil and not mon.disabled then
            hl.monitor({ output = "eDP-1", disabled = true })
        else
            hl.monitor({ output = "eDP-1", disabled = false, mode = "preferred", position = "0x0", scale = 1.175 })
        end
    end
end


-------------------
---- PROGRAMS -----
-------------------

hl.bind(mainMod .. " + A",          hl.dsp.exec_cmd(TERMINAL))
hl.bind(mainMod .. " + B",          hl.dsp.exec_cmd(BROWSER))
hl.bind(mainMod .. " + D",          hl.dsp.exec_cmd(FILE_MANAGER))
hl.bind(mainMod .. " + F",          hl.dsp.exec_cmd("wofi --show drun"))   -- launcher, ver DECISIONS.md D2
hl.bind(mainMod .. " + X",          hl.dsp.exec_cmd(CALCULATOR))
hl.bind(mainMod .. " + M",          hl.dsp.exec_cmd("obsidian"))
hl.bind(mainMod .. " + G",          hl.dsp.exec_cmd("~/.config/hypr/scripts/quick-ask.sh mini"))
hl.bind(mainMod .. " + ALT + SPACE", hl.dsp.exec_cmd("~/.config/hypr/scripts/quick-ask.sh pro"))
hl.bind(mainMod .. " + Z",          hl.dsp.exec_cmd("~/.config/hypr/scripts/show-keybinds.sh"))
hl.bind(mainMod .. " + ALT + M",    hl.dsp.exec_cmd("command -v hyprshutdown >/dev/null 2>&1 && hyprshutdown || hyprctl dispatch 'hl.dsp.exit()'"))


------------------------
---- WINDOW MANAGEMENT --
------------------------

hl.bind(mainMod .. " + C", hl.dsp.window.close())
hl.bind(mainMod .. " + V", hl.dsp.window.float({ action = "toggle" }))
hl.bind(mainMod .. " + P", hl.dsp.window.pseudo())
hl.bind(mainMod .. " + N", hl.dsp.layout("togglesplit"))    -- dwindle only

-- Move focus con HJKL
hl.bind(mainMod .. " + H", hl.dsp.focus({ direction = "left" }))
hl.bind(mainMod .. " + L", hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + K", hl.dsp.focus({ direction = "up" }))
hl.bind(mainMod .. " + J", hl.dsp.focus({ direction = "down" }))

-- Mover/redimensionar con mouse (SUPER + LMB/RMB)
hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag(),   { mouse = true })
hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })


-----------------------
---- WORKSPACES ------
-----------------------

-- Q/W/E/R/T/6-0 = workspaces 1-10; SHIFT mueve la ventana al workspace
local workspaceKeys = { "Q", "W", "E", "R", "T", "6", "7", "8", "9", "0" }
for i, key in ipairs(workspaceKeys) do
    hl.bind(mainMod .. " + " .. key,         hl.dsp.focus({ workspace = i }))
    hl.bind(mainMod .. " + SHIFT + " .. key, hl.dsp.window.move({ workspace = i }))
end

-- Scroll por los workspaces existentes
hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mainMod .. " + mouse_up",   hl.dsp.focus({ workspace = "e-1" }))

-- Scratchpad (special:magic)
hl.bind(mainMod .. " + S",         hl.dsp.workspace.toggle_special("magic"))
hl.bind(mainMod .. " + SHIFT + S", hl.dsp.window.move({ workspace = "special:magic" }))


--------------------
---- MULTIMEDIA ----
--------------------

-- Volumen (wpctl)
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"), { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"),      { locked = true, repeating = true })
hl.bind("XF86AudioMute",        hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"),     { locked = true, repeating = true })
hl.bind("XF86AudioMicMute",     hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"),   { locked = true, repeating = true })

-- Brillo (brightnessctl)
hl.bind("XF86MonBrightnessUp",   hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%+"), { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%-"), { locked = true, repeating = true })

-- Reproducción (playerctl, ver DECISIONS.md D3)
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd("playerctl next"),       { locked = true })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPlay",  hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd("playerctl previous"),   { locked = true })


----------------------
---- SCREENSHOTS ----
----------------------

hl.bind("Print",                   hl.dsp.exec_cmd('grim -g "$(slurp)" - | wl-copy'))
hl.bind(mainMod .. " + Print",     hl.dsp.exec_cmd('grim -g "$(slurp)" ~/Pictures/screenshots/$(date +%Y%m%d_%H%M%S).png'))
hl.bind(mainMod .. " + ALT + Print", hl.dsp.exec_cmd('grim ~/Pictures/screenshots/$(date +%Y%m%d_%H%M%S).png'))


-----------------------------
---- CACHYOS (COMENTADOS) ---
-----------------------------

-- Binds exclusivos de CachyOS. Activa/borra según DECISIONS.md B.

-- B1: Cerrar con SUPER+Escape / mover ventana con flechas
-- hl.bind(mainMod .. " + Escape", hl.dsp.exec_cmd("hyprctl kill"))
-- hl.bind(mainMod .. " + SHIFT + Up",    hl.dsp.window.move({ direction = "u" }))
-- hl.bind(mainMod .. " + SHIFT + Right", hl.dsp.window.move({ direction = "r" }))
-- hl.bind(mainMod .. " + SHIFT + Left",  hl.dsp.window.move({ direction = "l" }))
-- hl.bind(mainMod .. " + SHIFT + Down",  hl.dsp.window.move({ direction = "d" }))

-- B3: ALT+Tab ciclo de ventanas / SUPER+Tab window-switcher (noctalia)
-- hl.bind("ALT + Tab",       hl.dsp.window.cycle_next())
-- hl.bind(mainMod .. " + Tab", hl.dsp.exec_cmd("noctalia msg window-switcher"))

-- B4: Cursor zoom
-- local function zoomfunction(value)
--     local zoomvalue = hl.get_config("cursor:zoom_factor")
--     if (zoomvalue + value) > 3.0 then
--         hl.config({ cursor = { zoom_factor = 3.0 } })
--     elseif (zoomvalue + value) < 1.0 then
--         hl.config({ cursor = { zoom_factor = 1.0 } })
--     else
--         hl.config({ cursor = { zoom_factor = zoomvalue + value } })
--     end
-- end
-- hl.bind(mainMod .. " + Minus", function() zoomfunction(-0.3) end, { repeating = true })
-- hl.bind(mainMod .. " + Plus",  function() zoomfunction( 0.3) end, { repeating = true })
-- hl.bind(mainMod .. " + code:82", function() zoomfunction(-0.3) end, { repeating = true })
-- hl.bind(mainMod .. " + code:86", function() zoomfunction( 0.3) end, { repeating = true })

-- B5: Workspaces por monitor (SUPER+num focus monitor, SUPER+ALT/CONTROL+num workspace)
-- for i = 1, NUM_WPM do
--     local key = i % 10
--     hl.bind(mainMod .. " + ALT + " .. key,     hl.dsp.focus({ workspace = i }))
--     hl.bind(mainMod .. " + CONTROL + " .. key, hl.dsp.focus({ workspace = "m~" .. i }))
-- end
-- hl.bind(mainMod .. " + 1", hl.dsp.focus({ monitor = MONITOR1 }))
-- hl.bind(mainMod .. " + 2", hl.dsp.focus({ monitor = MONITOR2 }))
-- hl.bind(mainMod .. " + 3", hl.dsp.focus({ monitor = MONITOR3 }))
-- hl.bind(mainMod .. " + CONTROL + Right", hl.dsp.focus({ workspace = "m+1" }))
-- hl.bind(mainMod .. " + CONTROL + Left",  hl.dsp.focus({ workspace = "m-1" }))
-- hl.bind(mainMod .. " + CONTROL + Down",  hl.dsp.focus({ workspace = "emptym" }))
-- hl.bind(mainMod .. " + SHIFT + 1", hl.dsp.window.move({ monitor = MONITOR1 }))
-- hl.bind(mainMod .. " + SHIFT + 2", hl.dsp.window.move({ monitor = MONITOR2 }))
-- hl.bind(mainMod .. " + SHIFT + 3", hl.dsp.window.move({ monitor = MONITOR3 }))
-- hl.bind(mainMod .. " + SHIFT + mouse_up",   hl.dsp.window.move({ monitor = "-1" }))
-- hl.bind(mainMod .. " + SHIFT + mouse_down", hl.dsp.window.move({ monitor = "+1" }))
-- hl.bind(mainMod .. " + CONTROL + SHIFT + Right", hl.dsp.window.move({ workspace = "m+1" }))
-- hl.bind(mainMod .. " + CONTROL + SHIFT + Left",  hl.dsp.window.move({ workspace = "m-1" }))

-- B6: Noctalia (launcher, control center, clipboard, notificaciones, lock, wallpaper)
-- hl.bind(mainMod .. " + Space", hl.dsp.exec_cmd("noctalia msg panel-toggle launcher"))
-- hl.bind(mainMod .. " + X",     hl.dsp.exec_cmd("noctalia msg panel-toggle control-center"))
-- hl.bind(mainMod .. " + V",     hl.dsp.exec_cmd("noctalia msg panel-toggle clipboard"))
-- hl.bind(mainMod .. " + A",     hl.dsp.exec_cmd("noctalia msg panel-toggle control-center notifications"))
-- hl.bind(mainMod .. " + L",     hl.dsp.exec_cmd("noctalia msg session lock"))
-- hl.bind(mainMod .. " + ALT + C", hl.dsp.exec_cmd("noctalia msg panel-toggle session"))
-- hl.bind(mainMod .. " + SHIFT + W", hl.dsp.exec_cmd("noctalia msg panel-toggle wallpaper"))
-- hl.bind(mainMod .. " + Z",     hl.dsp.exec_cmd("noctalia msg settings-toggle"))
-- hl.bind(mainMod .. " + period", hl.dsp.exec_cmd("noctalia msg panel-toggle launcher /emo"))

-- B7: Utilidades
-- hl.bind(mainMod .. " + P", hl.dsp.exec_cmd("hyprpicker -a -n")) -- color picker
-- hl.bind("CONTROL + SHIFT + Escape", hl.dsp.exec_cmd(TERMINAL .. " -e btop"))
-- hl.bind("XF86Calculator",           hl.dsp.exec_cmd(CALCULATOR))

-- B9: Scroll por workspaces por monitor (vs e±1)
-- hl.bind(mainMod .. " + mouse_up",   hl.dsp.focus({ workspace = "m+1" }))
-- hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "m-1" }))
-- hl.bind(mainMod .. " + CONTROL + mouse_up",   hl.dsp.focus({ workspace = "m-1" }))
-- hl.bind(mainMod .. " + CONTROL + mouse_down", hl.dsp.focus({ workspace = "m+1" }))

-- B12: Screenshot vía noctalia (reemplaza grim/slurp)
-- hl.bind("Print",               hl.dsp.exec_cmd("noctalia msg screenshot-region"))
-- hl.bind(mainMod .. " + Print", hl.dsp.exec_cmd("noctalia msg screenshot-fullscreen"))
