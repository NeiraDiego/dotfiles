# Catálogo CachyOS: features en reasignación (qué se pierde y cómo recuperarlo)

Al conservar tus keybinds (DECISIONS.md, columna N) ciertas teclas de CachyOS
quedan reasignadas a tu flujo. Este archivo cataloga cada feature de CachyOS que
**se pierde** y sugiere una **tecla alternativa libre** para recuperarla más
adelante (basta con activar el bloque en `config/binds.lua` y cambiar la tecla).

Regla general para elegir alternativas: son combinaciones que ni tu config ni la
de CachyOS usan hoy (superpuestas con `SUPER+SHIFT+letra`, `SUPER+ALT+letra` o
`SUPER+CONTROL+letra`).

---

## 1. Features que COLISIONAN con tus keybinds (pierden la tecla original)

> Con columna N en DECISIONS.md ganas tú la tecla. Aquí está la acción de CachyOS
> que deja de tener atajo y una alternativa para recuperarla.

| Acción de CachyOS | Tecla original | Choca con tu | Sugerencia alternativa |
|---|---|---|---|
| Notificaciones (noctalia panel) | `SUPER+A` | kitty | `SUPER+SHIFT+N` |
| Clipboard (noctalia panel) | `SUPER+V` | toggle float | `SUPER+SHIFT+C` |
| Control-center (noctalia panel) | `SUPER+X` | calculadora | `SUPER+ALT+X` |
| Settings noctalia | `SUPER+Z` | show-keybinds | `SUPER+SHIFT+Z` |
| Fullscreen (mode 1) | `SUPER+D` | dolphin | `SUPER+SHIFT+F` |
| Fullscreen | `SUPER+F` | wofi | `SUPER+SHIFT+F` (o `SUPER+ALT+F`) |
| Session lock (noctalia) | `SUPER+L` | focus right | `SUPER+SHIFT+L` |
| Toggle float | `SUPER+ALT+SPACE` | quick-ask pro | ya tienes `SUPER+V` |
| Color picker (hyprpicker) | `SUPER+P` | pseudo-tile | `SUPER+SHIFT+P` |
| Editor default | `SUPER+T` | workspace 5 | `SUPER+ALT+T` |
| Cerrar ventana | `SUPER+Q` | workspace 1 | ya tienes `SUPER+C` |
| Togglesplit | `SUPER+J` | focus down | ya tienes `SUPER+N` |
| Navegador firefox | `SUPER+W` | workspace 2 | ya tienes `SUPER+B` (brave) |
| Calculadora | `SUPER+C` | cerrar ventana | ya tienes `SUPER+X` |
| Screenshot región (noctalia) | `Print` | grim+slurp | `SUPER+SHIFT+PRINT` |
| Screenshot fullscreen (noctalia) | `SUPER+Print` | grim fullscreen | `SUPER+ALT+S` |
| Scroll workspace por monitor (m±1) | `SUPER+wheel` | scroll e±1 | `SUPER+CONTROL+wheel` |
| Workspace special sin nombre | `SUPER+S` | special:magic | nada — tu scratchpad es superior |

---

## 2. Features de CachyOS con tecla LIBRE (no chocan, disponibles para activar)

> No se pierden: la tecla que usan no colisiona. Puedes activar el bloque
> comentado en `config/binds.lua` cuando quieras.

| Acción de CachyOS | Tecla | Nota |
|---|---|---|
| Terminal | `SUPER+Return` | tu terminal va en `SUPER+A`; útil tener ambos |
| File manager | `SUPER+E` | tú usas `SUPER+D` |
| Cerrar ventana forzado (`hyprctl kill`) | `SUPER+Escape` | |
| Mover ventana con flechas | `SUPER+SHIFT+↑↓←→` | tú mueves con `SUPER+SHIFT+Q/W/E/...` |
| Mover ventana a monitor ±1 | `SUPER+SHIFT+wheel` | |
| Mover ventana a monitor 1/2/3 | `SUPER+SHIFT+1/2/3` | |
| Mover ventana a workspace por monitor | `SUPER+CTRL+SHIFT+←/→` + `wheel` | |
| Mover a workspace m~i | `SUPER+SHIFT+CTRL+num` | |
| Ciclo de ventanas | `ALT+Tab` | |
| Window-switcher noctalia | `SUPER+Tab` | |
| Launcher noctalia | `SUPER+Space` | tú usas wofi con `SUPER+F` |
| Emoji launcher noctalia | `SUPER+.` | |
| Zoom cursor (−/+) | `SUPER+Minus` / `SUPER+Plus` | también `SUPER+code:82/86` (teclado numérico) |
| btop en terminal | `CTRL+SHIFT+Escape` | |
| Calculadora (tecla dedicada) | `XF86Calculator` | |
| Foco monitor 1/2/3 | `SUPER+1/2/3` | |
| Workspace absoluto | `SUPER+ALT+num` | |
| Workspace por monitor m~i | `SUPER+CTRL+num` | |
| Workspace m±1 / emptym | `SUPER+CTRL+←/→/↓` | |
| Wallpaper panel noctalia | `SUPER+SHIFT+W` | tienes wallpaper-carousel en autostart |
| Session panel noctalia | `SUPER+ALT+C` | |

---

## 3. Features de CachyOS sin tecla (solo si dices S en DECISIONS.md B)

| Feature | Cómo recuperarla después |
|---|---|
| Workspace `name:gaming` + reglas Steam/gamescope | Activar bloque B8 en `config/windowrules.lua` y `config/workspaces.lua` |
| Swallow de terminales + `vrr=3` + `force_zero_scaling` | Activar bloque B10 en `config/misc.lua` |
| Gestos touchpad (4/3 dedos) | Activar bloque B11 en `config/inputs.lua` (nota: `3 dedos izquierda=float` **no** se puede — Hyprland lo rechaza por solaparse con `3 dedos horizontal`; float ya está en `SUPER+V`) |
| Reglas float modales/dolphin/opacity overrides | Activar bloque B13 en `config/windowrules.lua` |
| Noctalia como barra/panel (vs waybar) | Decisión D1 en `config/autostart.lua` |
| Portal `xdph.conf` | Ya copiado y activo |

---

## 4. Comandos noctalia útiles (si decides reinstalar atajos)

Todos los `noctalia msg …` disponibles para enlazar a cualquier tecla:

```bash
noctalia msg panel-toggle launcher               # lanzador de apps
noctalia msg panel-toggle launcher /emo          # lanzador de emojis
noctalia msg panel-toggle control-center         # panel de control
noctalia msg panel-toggle control-center notifications
noctalia msg panel-toggle clipboard              # historial de portapapeles
noctalia msg panel-toggle session                # menú de sesión (salir/reiniciar)
noctalia msg session lock                        # bloquear pantalla
noctalia msg settings-toggle                     # ajustes noctalia
noctalia msg panel-toggle wallpaper              # selector de fondos
noctalia msg window-switcher                     # switcher de ventanas
noctalia msg screenshot-region                   # captura región
noctalia msg screenshot-fullscreen               # captura pantalla completa
noctalia msg volume-up / volume-down / volume-mute / mic-mute
noctalia msg media toggle / next / previous      # control multimedia
noctalia msg brightness-up / brightness-down     # brillo
```
