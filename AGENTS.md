# AGENTS.md

## Deployment

Dotfiles managed via [GNU Stow](https://www.gnu.org/software/stow/). Clone to `~/dotfiles`, then:

```bash
git submodule update --init   # kitty catppuccin themes (themes/mocha.conf)
stow bash      # ~/.bashrc
stow hypr      # ~/.config/hypr/
stow kitty     # ~/.config/kitty/
stow nvim      # ~/.config/nvim/
stow tmux      # ~/.tmux.conf
stow waybar    # ~/.config/waybar/
stow wofi      # ~/.config/wofi/
```

Run `stow -D <pkg>` to unlink, `stow -R <pkg>` to relink.

## Key files

| File | Role |
|---|---|
| `hypr/.config/hypr/hyprland.lua` | Hyprland Lua entrypoint (**active**), requires `config/*.lua` |
| `hypr/.config/hypr/config/` | 12 modules: binds, monitors, autostart, variables, inputs, decorations, animations, colors, misc, environment, windowrules, workspaces |
| `hypr/.config/hypr/hyprland.conf.bak` | Decommissioned native config (backup) |
| `hypr/.config/hypr/hyprland.lua.monolithic.bak` | Old single-file config (backup) |
| `hypr/.config/hypr/xdph.conf` | Portal screencopy `allow_token_by_default` |
| `hypr/.config/hypr/scripts/` | `show-keybinds.sh`, `wallpaper-carousel.sh`, `quick-ask.sh`, `quick-ask.env.example` |
| `hypr/DECISIONS.md`, `hypr/CACHYOS_LOST.md` | Migration S/N decisions + recoverable CachyOS features (excluded from stow via `.stow-local-ignore`) |
| `hypr/CONTEXT.md` | Redirect stub (content migrated here) |
| `bash/.bashrc` | oh-my-bash, custom `dotcommit` (git add+commit+push), `gitdot` alias |
| `nvim/.config/nvim/init.lua` | lazy.nvim entrypoint, modules in `lua/config/` and `lua/plugins/` |
| `tmux/.tmux.conf` | TPM plugins (catppuccin, vim-tmux-navigator) |
| `waybar/.config/waybar/` | `config` (JSON), `style.css`, `scripts/powermenu.sh` |
| `kitty/.config/kitty/` | `kitty.conf` (`shell tmux new-session -A -s main` → kitty abre con tmux) + `catppuccin/` subtheme |
| `wofi/.config/wofi/` | `config`, `style.css` (Catppuccin Mocha theme) |

## Hyprland

**Active config**: `hyprland.lua` entrypoint + `config/*.lua` modules (CachyOS-style modular Lua). Native `.conf` decommissioned as `.conf.bak`.

Host detection: `IS_SERVER = (hostname == "DiegoArchSV")` (headless Sunshine streaming host). On the server only `HEADLESS-1` virtual monitor + `sunshine` autostart.

### Monitors
- `DP-3` (external, left): preferred, -1920x0, scale 1
- `eDP-1` (laptop, right): preferred, 0x0, scale **1.57** (re-enable vía `SUPER+ALT+P` también 1.57)
- `DP-4` / `DP-9` (alternate externals): preferred, -1920x0, scale 1
- Server: `HEADLESS-1` 1920x1080@60

### Autostart (`hl.on("hyprland.start")`, UWSM session)
1. `dbus-update-activation-environment --systemd --all`, `noctalia`, `xhost +SI:localuser:root`
2. `wallpaper-carousel.sh`
3. `nm-applet`
4. `brave` → workspace 1 (laptop)
5. `kitty` → workspace 2 (laptop)
6. `sunshine` (server only)

Bar/panel: **noctalia** (D1 = S). `waybar/` and `wofi/` packages remain stowable but are not the active bar/launcher on this setup.

### Keybindings
- `SUPER + A/B/D/F/X/M/G` → kitty / brave / dolphin / wofi / calculator / obsidian / quick-ask mini
- `SUPER + ALT + SPACE` → quick-ask (pro); `SUPER + ALT + M` → exit; `SUPER + ALT + P` → toggle eDP-1
- `SUPER + Z` → noctalia settings (A8 = S)
- `SUPER + C` → close window; `SUPER + Escape` → `hyprctl kill` (B1 = S)
- `SUPER + V` → toggle float; `SUPER + P` → pseudo; `SUPER + N` → togglesplit
- `SUPER + H/J/K/L` → move focus (left/down/up/right)
- `SUPER + Q/W/E/R/T/6-0` → workspaces 1-10; `SUPER + SHIFT + …` → move window to workspace
- `SUPER + S` → scratchpad (special:magic); `SUPER + SHIFT + S` → move to scratchpad
- `SUPER + wheel` → cycle workspaces (e±1)
- `SUPER + mouse:272` → move window, `SUPER + mouse:273` → resize
- `Print` → noctalia screenshot-region (A17 = S); `SUPER + Print` → noctalia screenshot-fullscreen (A18 = S); `SUPER + ALT + Print` → grim fullscreen to file
- Multimedia keys (XF86Audio / XF86MonBrightness) → noctalia (A19/A20/A21 = S)
- Gestures: 3-finger horizontal = workspace (yours); CachyOS (B11 = S): 4-finger horizontal = workspace, 3-finger down = close / up = fullscreen / left = float

### Workspace rules
- `brave` / `brave-browser` (class: `^(brave|brave-browser)$`) → workspace 1
- `kitty` (class `^kitty$`) → workspace 2 (opacity 0.93), abre con tmux (sesión `main`)
- `name:gaming` (B8 = S) → default on primary monitor
- default_names `q/w/e/r/t` for workspaces 1-5

### Window rules
- Brave/Chromium PiP (`^Picture in picture$`): float, pin, move `72% 60%`, size `448x252`, keep_aspect_ratio, no_dim, no_shadow
- `org.gnome.Calculator`, `blueman-manager`: float; `wofi`: opacity 0.90
- suppress-maximize, fix-xwayland-drags, hyprland-run float
- CachyOS extras (B13 = S): generic float centering, gaming/Steam rules, dolphin modals, float utilities (pavucontrol, nm-applet, …), opacity overrides, `.exe`/launcher floats on primary monitor

### Layout
- dwindle + `preserve_split` (no global pseudotile; `SUPER + P` toggles pseudo per-window)
- Border radius: 10px, blur active
- Colors: gradient border `rgba(33ccffee)` → `rgba(00ff99ee)`, inactive `rgba(595959aa)`

## Neovim

- Plugin manager: lazy.nvim (auto-installs on first launch)
- Config modules: `lua/config/options.lua`, `lua/config/keymaps.lua`
- Plugins: `lua/plugins/*.lua` (13 plugins)
- OpenCode integration via `opencode.nvim` with `<leader>a*` keymaps

## Git

```bash
gitdot    # alias: cd ~/dotfiles && git add .
dotcommit # interactive: git add . → git commit → git push
```

## Fonts

- Sans-serif fallback `FreeSans` has poor kerning causing wide number spacing in web apps (e.g., Odoo in Brave).
- Fix: installed `noto-fonts`, `ttf-dejavu`, `ttf-liberation` and set Noto Sans as preferred sans-serif in `~/.config/fontconfig/fonts.conf`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <alias>
    <family>sans-serif</family>
    <prefer>
      <family>Noto Sans</family>
      <family>DejaVu Sans</family>
      <family>Liberation Sans</family>
    </prefer>
  </alias>
</fontconfig>
```

After changes, run `fc-cache -fv` and restart Brave.

## Gotchas

- `lazy-lock.json` is **tracked** despite the `.gitignore` entry (gitignore doesn't apply to tracked files)
- `kitty/kitty.conf.back` is a manual backup
- `hyprland.conf.bak` and `hyprland.lua.monolithic.bak` are decommissioned backups — active config = `hyprland.lua` + `config/*.lua`
- `~/.config/hypr.cachyos-backup-*` on the system holds the original CachyOS config (migration 2026-08)
- NVIDIA env vars live in `~/.config/uwsm/env` (moved from `.bashrc`, D6 = S)
- No CI, tests, linting, or type checking — purely config management
- After cloning tmux config, manually install TPM plugins with `Prefix + I`
- Shell por defecto: **bash** (vía `chsh`). El `.bashrc` es bash-only; `source .bashrc` desde fish falla en la línea 1 (`case` vs `switch`) — si una terminal abre fish, es porque heredó `$SHELL=/bin/fish` de una sesión vieja; fix: logout/login completo. `kitty.conf` lanza `tmux new-session -A -s main` (tmux usa el shell de `/etc/passwd`, bash)
