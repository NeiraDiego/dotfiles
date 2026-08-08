# Decisiones de migración: Hyprland CachyOS → dotfiles

Rellena cada ítem con `S` (aceptar/incorporar) o `N` (eliminar/omitir).
El bloque a la derecha de cada línea es donde escribes tu decisión.

La config ya está reestructurada en `config/*.lua` (estructura de CachyOS) con
tu workflow activo y las features de CachyOS **comentadas** (referenciadas por
cada ítem B). Al terminar, aplico tus respuestas: activo/elimino cada bloque y
hago `stow`.

---

## A. Conflictos de tecla — mismo keybind, distinta acción

> `S` = gana la de CachyOS (reemplaza la tuya) · `N` = conservas la tuya (se elimina la de CachyOS)

| # | Tecla | CachyOS | Tú (dotfiles) | Decisión |
|---|-------|---------|----------------|----------|
| A1 | `SUPER+A` | panel notificaciones (noctalia) | kitty (terminal) | |
| A2 | `SUPER+C` | calculadora | cerrar ventana | |
| A3 | `SUPER+D` | fullscreen (mode 1) | dolphin | |
| A4 | `SUPER+F` | fullscreen | wofi (launcher) | |
| A5 | `SUPER+V` | clipboard (noctalia) | toggle float | |
| A6 | `SUPER+P` | hyprpicker (color picker) | pseudo-tile | |
| A7 | `SUPER+X` | panel control-center (noctalia) | calculadora | |
| A8 | `SUPER+Z` | settings (noctalia) | show-keybinds.sh | |
| A9 | `SUPER+Q` | cerrar ventana | workspace 1 | |
| A10 | `SUPER+W` | firefox | workspace 2 | |
| A11 | `SUPER+T` | editor (gnome-text-editor) | workspace 5 | |
| A12 | `SUPER+L` | session lock (noctalia) | focus right | |
| A13 | `SUPER+J` | togglesplit | focus down | |
| A14 | `SUPER+ALT+SPACE` | toggle float | quick-ask pro | |
| A15 | `SUPER+S` / `SHIFT+S` | special (sin nombre) | special:magic | |
| A16 | `SUPER+scroll` | workspace por monitor (m±1) | workspace global (e±1) | |
| A17 | `Print` | screenshot región (noctalia) | grim+slurp → portapapeles | |
| A18 | `SUPER+Print` | screenshot fullscreen (noctalia) | grim fullscreen → archivo | |
| A19 | `XF86Audio*` (volumen/mute) | noctalia | wpctl | |
| A20 | `XF86MonBrightness*` | noctalia | brightnessctl | |
| A21 | `XF86AudioNext/Pause/Play/Prev` | noctalia (media) | playerctl | |

---

## B. Features de CachyOS sin equivalente en tu dotfiles

> `S` = añadir a la config · `N` = omitir

| # | Feature | Descripción / ubicación | Decisión |
|---|---------|--------------------------|----------|
| B1 | `SUPER+Escape` → `hyprctl kill` | Cerrar ventana forzado. [binds.lua] | |
| B2 | Mover ventana con `SUPER+SHIFT+↑↓←→` | Mover en dirección (flechas). [binds.lua] | |
| B3 | `ALT+Tab` / `SUPER+Tab` | Ciclar ventanas / window-switcher (noctalia). [binds.lua] | |
| B4 | Zoom de cursor `SUPER+−/+` (y teclado numérico) | Zoom del cursor hasta 3x. [binds.lua] | |
| B5 | Workspaces por monitor (`SUPER+ALT/CONTROL+num`, `SUPER+1/2/3`, mover ventana a monitor) | Modelo multi-monitor de CachyOS; tu modelo es global 1-10. [binds.lua] | |
| B6 | Noctalia: launcher `SUPER+SPACE`, panel `SUPER+X`, clipboard `SUPER+V`, notificaciones `SUPER+A`, lock `SUPER+L`, session `SUPER+ALT+C`, wallpaper `SUPER+SHIFT+W`, emoji `SUPER+.` | Suite CachyOS (requiere noctalia). Conflicto con A1/A5/A7/A8/A12. [binds.lua] | |
| B7 | `SUPER+P` → hyprpicker (color picker) | Color picker. Conflicto con A6. [binds.lua] | |
| B8 | Workspace `name:gaming` + reglas de juegos | Steam/gamescope en su propio workspace. [windowrules.lua] [workspaces.lua] | |
| B9 | Scroll por workspace del monitor | `SUPER+scroll` y `SUPER+CTRL+scroll` en modo m±1. Conflicto con A16. [binds.lua] | |
| B10 | Swallow de terminales + `vrr=3` + `force_zero_scaling` + `middle_click_paste=false` | Swallow (kitty/ghostty/konsole/alacritty…), VRR, escala. [misc.lua] | |
| B11 | Gestos touchpad de CachyOS | 4 dedos horizontal = workspace; 3 dedos: abajo=cerrar, arriba=fullscreen, izquierda=float. Tu gesto actual: 3 dedos horizontal = workspace. [inputs.lua] | |
| B12 | Screenshot vía noctalia | `Print`/`SUPER+Print` por noctalia (sin grim). Conflicto con A17/A18. [binds.lua] | |
| B13 | Reglas de ventana extra (float modales/diálogos, dolphin, opacity override firefox/terminales/video, apps `.exe` y launchers en monitor primario) | Ventanas flotantes y opacidades. [windowrules.lua] | |
| B14 | `xdph.conf` (screencopy `allow_token_by_default`) | Portal de captura; útil para grim/slurp. Ya copiado. | |

---

## C. Tu workflow (se conserva — informativo, sin acción)

- Workspaces globales 1-10 con `Q/W/E/R/T/6-0`, mover ventana con `SHIFT+…`
- Focus `H/J/K/L`, `SUPER+M` obsidian, `SUPER+G` quick-ask mini, `SUPER+ALT+M` salir
- `SUPER+ALT+P` toggle eDP-1, `SUPER+ALT+PRINT` fullscreen a archivo
- Scratchpad `special:magic`, scroll `SUPER+wheel` (e±1)
- Autostart: wallpaper-carousel.sh, nm-applet, brave, kitty -e tmux (sunshine en servidor)
- Detección de host: `DiegoArchSV` = servidor headless (Sunshine)
- Layout teclado `us, latam` + `grp:win_space_toggle`
- Monitores: DP-3/eDP-1 (scale 1.57)/DP-4/DP-9
- Nombres de workspaces q/w/e/r/t (para waybar)
- Reglas: ghostty→2 (opacity 0.93), brave→1, PiP, calculadora float, blueman, wofi, fix-xwayland

---

## D. Decisiones estructurales

> `S` = aceptar la sugerencia · `N` = rechazarla/otra opción

| # | Tema | Sugerencia | Decisión |
|---|------|------------|----------|
| D1 | Barra / panel | **noctalia** (integrado, ya instalado) vs **waybar** (tu config en dotfiles/waybar, hay que `pacman -S waybar`; excluye noctalia como barra). [autostart.lua] | |
| D2 | Launcher | **wofi** (tu config en dotfiles/wofi, hay que instalar) vs **noctalia launcher** (`SUPER+SPACE`). Hoy `SUPER+F` lanza wofi. | |
| D3 | Control de media | **playerctl** (tu config, hay que `pacman -S playerctl`) vs **noctalia** (ya instalado). [binds.lua A21] | |
| D4 | Navegador | **brave** (tuyo, ya instalado) vs **firefox** (default CachyOS). [variables.lua] | |
| D5 | Editor default | `gnome-text-editor` (CachyOS) vs `nvim` (el tuyo). [variables.lua] | |
| D6 | Env vars NVIDIA | Mover `GBM_BACKEND=nvidia-drm`, `__GLX_VENDOR_LIBRARY_NAME=nvidia`, `WLR_NO_HARDWARE_CURSORS=1` (hoy en `~/.bashrc`) a **`~/.config/uwsm/env`** para que apliquen a la sesión Wayland. | |
| D7 | Colores | **Tu paleta** (gradiente cyan→verde, gris) vs verde/azul CachyOS. La config usa tu paleta. | |

---

## Notas

- Números `B#`/`D#` referencian bloques comentados en los archivos `config/*.lua`.
- Tras llenar esto: **no hagas `stow` ni reinicies**; avísame y aplico las
  respuestas, hago backup de `~/.config/hypr` actual y `stow hypr`.
- `hyprland.lua.monolithic.bak` conserva tu config anterior de un solo archivo.
- Este archivo se puede borrar al terminar la migración.
