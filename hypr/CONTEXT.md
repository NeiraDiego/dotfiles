# Hyprland Configuration Context

## Archivos activos
- **`hyprland.conf`** — Configuración tradicional (formato Hyprland nativo)
- **`hyprland.lua** — Configuración en Lua (más moderna, completa)
- **`scripts/`** — Scripts auxiliares (`show-keybinds.sh`, `toggle-edp.sh`)

**Ambos archivos se mantienen sincronizados.** Los cambios deben aplicarse en ambos.

## Monitores
- `DP-1` (externo, izquierda): preferred, 0x0, scale 1
- `eDP-1` (laptop, derecha): preferred, 1920x0, scale 1.175

## Autostart (orden)
1. `waybar`
2. `brave-browser` → workspace 1
3. `ghostty -e tmux` → workspace 2

## Keybindings principales
- `SUPER + A` → terminal (ghostty)
- `SUPER + B` → brave-browser
- `SUPER + D` → dolphin
- `SUPER + F` → wofi (drun)
- `SUPER + X` → gnome-calculator
- `SUPER + C` → cerrar ventana
- `SUPER + V` → toggle floating
- `SUPER + M` → salir
- `SUPER + Z` → mostrar keybinds
- `SUPER + ALT + P` → toggle eDP-1
- `SUPER + H/J/K/L` → mover foco (izq/abajo/arriba/der)
- `SUPER + Q/W/E/R/T/6-0` → workspaces 1-10
- `SUPER + SHIFT + Q/W/E/R/T/6-0` → mover ventana a workspace
- `SUPER + S` → scratchpad (special:magic)
- Multimedia keys: volumen (wpctl), brillo (brightnessctl), playback (playerctl)
- `SUPER + mouse:272` → mover ventana, `SUPER + mouse:273` → redimensionar

## Workspace rules
- `brave` / `brave-browser` (class: `^(brave|brave-browser)$`) → workspace 1
- `com.mitchellh.ghostty` → workspace 2

## Window rules
- PiP de Brave/Chromium (title: `^Picture in picture$`): `float`, `pin`, posición `4% 60%` (abajo-izquierda), tamaño `448x252` (~70% del original), `keepaspectratio`, `nodim`, `noborder`, `noshadow`
- `org.gnome.Calculator`: `float`

## Layout
- dwindle con pseudotile y preserve_split
- Border radius: 10px, blur activo
- Animaciones configurables por curva Bezier/spring (Lua)

## Cambios recientes
- **Zen Browser → Brave**: Se reemplazó Zen por Brave en:
  - Autostart (`exec-once` / `hl.exec_cmd`)
  - Keybinding `SUPER + B`
  - Window rule de workspace 1
  - Fecha: 2026-05-19
