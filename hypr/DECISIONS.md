# Decisiones de migración: Hyprland CachyOS → dotfiles

> **ESTADO: APLICADO el 2026-08-07.** Los bloques S están activos en
> `config/*.lua`; los N quedan comentados (recuperables vía `CACHYOS_LOST.md`).
> Este archivo puede borrarse.

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
| A1 | `SUPER+A` | panel notificaciones (noctalia) | kitty (terminal) |N|
| A2 | `SUPER+C` | calculadora | cerrar ventana |N|
| A3 | `SUPER+D` | fullscreen (mode 1) | dolphin |N|
| A4 | `SUPER+F` | fullscreen | wofi (launcher) |N|
| A5 | `SUPER+V` | clipboard (noctalia) | toggle float |N|
| A6 | `SUPER+P` | hyprpicker (color picker) | pseudo-tile |N|
| A7 | `SUPER+X` | panel control-center (noctalia) | calculadora |N|
| A8 | `SUPER+Z` | settings (noctalia) | show-keybinds.sh |S|
| A9 | `SUPER+Q` | cerrar ventana | workspace 1 |N|
| A10 | `SUPER+W` | firefox | workspace 2 |N|
| A11 | `SUPER+T` | editor (gnome-text-editor) | workspace 5 |N|
| A12 | `SUPER+L` | session lock (noctalia) | focus right |N|
| A13 | `SUPER+J` | togglesplit | focus down |N|
| A14 | `SUPER+ALT+SPACE` | toggle float | quick-ask pro |N|
| A15 | `SUPER+S` / `SHIFT+S` | special (sin nombre) | special:magic |N|
| A16 | `SUPER+scroll` | workspace por monitor (m±1) | workspace global (e±1) |S|
| A17 | `Print` | screenshot región (noctalia) | grim+slurp → portapapeles |S|
| A18 | `SUPER+Print` | screenshot fullscreen (noctalia) | grim fullscreen → archivo |S|
| A19 | `XF86Audio*` (volumen/mute) | noctalia | wpctl |S|
| A20 | `XF86MonBrightness*` | noctalia | brightnessctl |S|
| A21 | `XF86AudioNext/Pause/Play/Prev` | noctalia (media) | playerctl |S|

---

## B. Features de CachyOS sin equivalente en tu dotfiles

> `S` = añadir a la config · `N` = omitir

| # | Feature | Descripción / ubicación | Decisión |
|---|---------|--------------------------|----------|
| B1 | `SUPER+Escape` → `hyprctl kill` | Cerrar ventana forzado. [binds.lua] |S|
| B2 | Mover ventana con `SUPER+SHIFT+↑↓←→` | Mover en dirección (flechas). [binds.lua] |N|
| B3 | `ALT+Tab` / `SUPER+Tab` | Ciclar ventanas / window-switcher (noctalia). [binds.lua] |N|
| B4 | Zoom de cursor `SUPER+−/+` (y teclado numérico) | Zoom del cursor hasta 3x. [binds.lua] |N|
| B5 | Workspaces por monitor (`SUPER+ALT/CONTROL+num`, `SUPER+1/2/3`, mover ventana a monitor) | Modelo multi-monitor de CachyOS; tu modelo es global 1-10. [binds.lua] |N|
| B6 | Noctalia: launcher `SUPER+SPACE`, panel `SUPER+X`, clipboard `SUPER+V`, notificaciones `SUPER+A`, lock `SUPER+L`, session `SUPER+ALT+C`, wallpaper `SUPER+SHIFT+W`, emoji `SUPER+.` | Suite CachyOS (requiere noctalia). Conflicto con A1/A5/A7/A8/A12. [binds.lua] |N|
| B7 | `SUPER+P` → hyprpicker (color picker) | Color picker. Conflicto con A6. [binds.lua] |N|
| B8 | Workspace `name:gaming` + reglas de juegos | Steam/gamescope en su propio workspace. [windowrules.lua] [workspaces.lua] |S|
| B9 | Scroll por workspace del monitor | `SUPER+scroll` y `SUPER+CTRL+scroll` en modo m±1. Conflicto con A16. [binds.lua] |N|
| B10 | Swallow de terminales + `vrr=3` + `force_zero_scaling` + `middle_click_paste=false` | Swallow (kitty/ghostty/konsole/alacritty…), VRR, escala. [misc.lua] |N|
| B11 | Gestos touchpad de CachyOS | 4 dedos horizontal = workspace; 3 dedos: abajo=cerrar, arriba=fullscreen, ~~izquierda=float~~. Tu gesto actual: 3 dedos horizontal = workspace. **Nota aplicada**: `3 dedos izquierda=float` se omite — en Hyprland `horizontal` ya captura left+right con 3 dedos → Hyprland rechaza el gesto "left" por solaparse (error en línea 31). Float sigue en `SUPER+V`. [inputs.lua] |S|
| B12 | Screenshot vía noctalia | `Print`/`SUPER+Print` por noctalia (sin grim). Conflicto con A17/A18. [binds.lua] |S|
| B13 | Reglas de ventana extra (float modales/diálogos, dolphin, opacity override firefox/terminales/video, apps `.exe` y launchers en monitor primario) | Ventanas flotantes y opacidades. [windowrules.lua] |S|
| B14 | `xdph.conf` (screencopy `allow_token_by_default`) | Portal de captura; útil para grim/slurp. Ya copiado. |S|

---

## C. Tu workflow (se conserva — informativo, sin acción)

- Workspaces globales 1-10 con `Q/W/E/R/T/6-0`, mover ventana con `SHIFT+…`
- Focus `H/J/K/L`, `SUPER+M` obsidian, `SUPER+G` quick-ask mini, `SUPER+ALT+M` salir
- `SUPER+ALT+P` toggle eDP-1, `SUPER+ALT+PRINT` fullscreen a archivo
- Scratchpad `special:magic`, scroll `SUPER+wheel` (e±1)
- Autostart: wallpaper-carousel.sh, nm-applet, brave, kitty (abre con tmux, sesión `main`); sunshine en servidor
- Detección de host: `DiegoArchSV` = servidor headless (Sunshine)
- Layout teclado `us, latam` + `grp:win_space_toggle`
- Monitores: DP-3/eDP-1 (scale 1.57)/DP-4/DP-9
- Nombres de workspaces q/w/e/r/t (para waybar)
- Reglas: kitty→2 (opacity 0.93), brave→1, PiP, calculadora float, blueman, wofi, fix-xwayland

---

## D. Decisiones estructurales

> `S` = aceptar la sugerencia · `N` = rechazarla/otra opción

| # | Tema | Sugerencia | Decisión |
|---|------|------------|----------|
| D1 | Barra / panel | **noctalia** (integrado, ya instalado) vs **waybar** (tu config en dotfiles/waybar, hay que `pacman -S waybar`; excluye noctalia como barra). [autostart.lua] |S|
| D2 | Launcher | **wofi** (tu config en dotfiles/wofi, hay que instalar) vs **noctalia launcher** (`SUPER+SPACE`). Hoy `SUPER+F` lanza wofi. |S|
| D3 | Control de media | **playerctl** (tu config, hay que `pacman -S playerctl`) vs **noctalia** (ya instalado). [binds.lua A21] |S|
| D4 | Navegador | **brave** (tuyo, ya instalado) vs **firefox** (default CachyOS). [variables.lua] |N|
| D5 | Editor default | `gnome-text-editor` (CachyOS) vs `nvim` (el tuyo). [variables.lua] |N|
| D6 | Env vars NVIDIA | Mover `GBM_BACKEND=nvidia-drm`, `__GLX_VENDOR_LIBRARY_NAME=nvidia`, `WLR_NO_HARDWARE_CURSORS=1` (hoy en `~/.bashrc`) a **`~/.config/uwsm/env`** para que apliquen a la sesión Wayland. |S|
| D7 | Colores | **Tu paleta** (gradiente cyan→verde, gris) vs verde/azul CachyOS. La config usa tu paleta. |S|

---

## Notas

- Para cada feature que "pierdes" al marcar `N`, hay una **tecla alternativa
  libre** en [`CACHYOS_LOST.md`](./CACHYOS_LOST.md) para recuperarla después.
- Números `B#`/`D#` referencian bloques comentados en los archivos `config/*.lua`.
- Tras llenar esto: **no hagas `stow` ni reinicies**; avísame y aplico las
  respuestas, hago backup de `~/.config/hypr` actual y `stow hypr`.
- `hyprland.lua.monolithic.bak` conserva tu config anterior de un solo archivo.
- Este archivo se puede borrar al terminar la migración.

---

## Adenda 2026-10: quick-ask → cerebro

- `quick-ask.sh` (mini/pro con wofi + Ollama remoto 192.168.30.110) quedó
  **DEPRECADO**: wofi no está instalado y el Ollama remoto está caído.
- Reemplazo: **`cerebro ui`** (lanzador GTK4; router Qwen3-1.7B + chat
  Qwen3-14B local + retrieval sobre `~/Notas` + voz). Binds: `SUPER+G` y
  `SUPER+ALT+G` → `cerebro ui` (se movió de `SUPER+ALT+SPACE` para no pisar
  `grp:win_space_toggle`). Ventana flotante centrada 860x600
  (`windowrules.lua`). Dentro de la UI: `Ctrl+C` copiar, `Ctrl+K` snippet,
  `Ctrl+S` nota, `Ctrl+L` voz, `Ctrl+P` nube; prefijo `!` → buscar en web.
- Definición técnica completa en `AGENTS.md` → `## Cerebro`.
