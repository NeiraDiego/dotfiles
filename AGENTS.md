# AGENTS.md

## Deployment

Dotfiles managed via [GNU Stow](https://www.gnu.org/software/stow/). Clone to `~/dotfiles`, then:

```bash
stow bash      # ~/.bashrc
stow hypr      # ~/.config/hypr/
stow kitty     # ~/.config/kitty/
stow nvim      # ~/.config/nvim/
stow tmux      # ~/.tmux.conf
stow waybar    # ~/.config/waybar/
```

Run `stow -D <pkg>` to unlink, `stow -R <pkg>` to relink.

## Key files

| File | Role |
|---|---|
| `AGENTS.md` | **Primary reference** for Hyprland config — monitors, keybinds, window rules, autostart, waybar |
| `hypr/.config/hypr/hyprland.conf` | Hyprland native config |
| `hypr/.config/hypr/hyprland.lua` | Hyprland Lua config — must be kept in sync with `.conf` |
| `hypr/.config/hypr/scripts/` | `show-keybinds.sh`, `toggle-edp.sh` |
| `bash/.bashrc` | oh-my-bash, custom `dotcommit` (git add+commit+push), `gitdot` alias |
| `nvim/.config/nvim/init.lua` | lazy.nvim entrypoint, modules in `lua/config/` and `lua/plugins/` |
| `tmux/.tmux.conf` | TPM plugins (catppuccin, vim-tmux-navigator), run `Prefix + I` after fresh clone |
| `waybar/.config/waybar/` | `config` (JSON), `style.css`, `scripts/powermenu.sh` |
| `kitty/.config/kitty/` | `kitty.conf` + `catppuccin/` subtheme |

## Hyprland

- **Keep both config files in sync** — changes to keybinds, monitors, window rules must go in both `hyprland.conf` and `hyprland.lua`

### Archivos activos
- **`hyprland.conf`** — Configuración tradicional (formato Hyprland nativo)
- **`hyprland.lua`** — Configuración en Lua (más moderna, completa)
- **`scripts/`** — Scripts auxiliares (`show-keybinds.sh`, `toggle-edp.sh`)

### Monitores
- `DP-1` (externo, izquierda): preferred, 0x0, scale 1
- `eDP-1` (laptop, derecha): preferred, 1920x0, scale 1.175

### Autostart (orden)
1. `waybar`
2. `brave-browser` → workspace 1
3. `ghostty -e tmux` → workspace 2

### Keybindings principales
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

### Workspace rules
- `brave` / `brave-browser` (class: `^(brave|brave-browser)$`) → workspace 1
- `com.mitchellh.ghostty` → workspace 2

### Window rules
- PiP de Brave/Chromium (title: `^Picture in picture$`): `float`, `pin`, posición `4% 60%` (abajo-izquierda), tamaño `448x252` (~70% del original), `keepaspectratio`, `nodim`, `noborder`, `noshadow`
- `org.gnome.Calculator`: `float`

### Layout
- dwindle con pseudotile y preserve_split
- Border radius: 10px, blur activo
- Animaciones configurables por curva Bezier/spring (Lua)

### Waybar
- **Config**: `waybar/.config/waybar/config` — Barra con workspaces (izq), clock/idle_inhibitor (centro), y system-tray/pulseaudio/botón power (der)
- **Style**: `waybar/.config/waybar/style.css` — Tema Catppuccin Mocha:
  - Fondo: `rgba(30, 30, 46, 0.85)` (base)
  - Texto: `#cdd6f4`
  - Workspace activo: azul `#89b4fa` con overlay
  - Power button: lila `#cba6f7` con overlay
  - Estados: verde (battery charging, idle activado), amarillo (battery warning), rojo (battery critical, pulseaudio muted, temperature critical)
  - Tooltips: fondo base 95% con borde surface0
- **Módulos**: workspaces se sincroniza vía IPC de Hyprland

### Cambios recientes
- **Waybar CSS → Catppuccin Mocha**: Se reemplazó el tema anterior (verde oscuro/azul) por Catppuccin Mocha para coincidir con wofi. Se eliminó `hyprland/mode` de modules-left (no existe en waybar v0.12) y `sway/mode` del config. Fecha: 2026-06-01
- **Zen Browser → Brave**: Se reemplazó Zen por Brave en:
  - Autostart (`exec-once` / `hl.exec_cmd`)
  - Keybinding `SUPER + B`
  - Window rule de workspace 1
  - Fecha: 2026-05-19

## Neovim

- Plugin manager: lazy.nvim (auto-installs on first launch)
- Config modules: `lua/config/options.lua`, `lua/config/keymaps.lua`
- Plugins: `lua/plugins/*.lua` (13 plugins)
- OpenCode integration via `opencode.nvim` with `<leader>a*` keymaps

## Pre-existing instruction files

### `AGENTS.md` (this file)
Hyprland-specific context under the ## Hyprland section (monitors, keybinds, autostart, window rules, layout, waybar). Agents editing hyprland config should read this first.

## Git

```bash
gitdot    # alias: cd ~/dotfiles && git add .
dotcommit # interactive: git add . → git commit → git push
```

## Gotchas

- `lazy-lock.json` is gitignored (nvim lazy.nvim lockfile, intentionally untracked)
- `bashrc-omb-bk` in `bash/` is a manual backup, not deployed by stow
- `kitty/kitty.conf.back` in the kitty config dir is a manual backup
- No CI, tests, linting, or type checking — purely config management
- After cloning tmux config, manually install TPM plugins with `Prefix + I`
