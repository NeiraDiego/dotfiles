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
| `hypr/.config/hypr/hyprland.lua` | Hyprland Lua config (**active**) |
| `hypr/.config/hypr/hyprland.conf.bak` | Decommissioned native config (backup) |
| `hypr/.config/hypr/scripts/` | `show-keybinds.sh`, `wallpaper-carousel.sh`, `quick-ask.sh` |
| `hypr/CONTEXT.md` | Redirect stub (content migrated here) |
| `bash/.bashrc` | oh-my-bash, custom `dotcommit` (git add+commit+push), `gitdot` alias |
| `nvim/.config/nvim/init.lua` | lazy.nvim entrypoint, modules in `lua/config/` and `lua/plugins/` |
| `tmux/.tmux.conf` | TPM plugins (catppuccin, vim-tmux-navigator) |
| `waybar/.config/waybar/` | `config` (JSON), `style.css`, `scripts/powermenu.sh` |
| `kitty/.config/kitty/` | `kitty.conf` + `catppuccin/` subtheme |
| `wofi/.config/wofi/` | `config`, `style.css` (Catppuccin Mocha theme) |

## Hyprland

**Active config**: `hyprland.lua` (native `.conf` decommissioned as `.conf.bak`)

### Monitors
- `DP-3` (external, left): preferred, -1920x0, scale 1
- `eDP-1` (laptop, right): preferred, 0x0, scale 1.175

### Autostart (order)
1. `waybar`
2. `wallpaper-carousel.sh`
3. `brave` → workspace 1
4. `kitty -e tmux` → workspace 2

### Keybindings
- `SUPER + A` → terminal (kitty)
- `SUPER + B` → brave
- `SUPER + D` → dolphin
- `SUPER + F` → wofi (drun)
- `SUPER + X` → gnome-calculator
- `SUPER + C` → close window
- `SUPER + V` → toggle floating
- `SUPER + M` → obsidian
- `SUPER + ALT + M` → exit
- `SUPER + G` → quick-ask (mini)
- `SUPER + ALT + SPACE` → quick-ask (pro)
- `SUPER + Z` → show keybinds
- `SUPER + ALT + P` → toggle eDP-1
- `SUPER + H/J/K/L` → move focus (left/down/up/right)
- `SUPER + Q/W/E/R/T/6-0` → workspaces 1-10
- `SUPER + SHIFT + Q/W/E/R/T/6-0` → move window to workspace
- `SUPER + S` → scratchpad (special:magic)
- `Print` → screenshot selection to clipboard
- `SUPER + Print` → screenshot selection to file
- `SUPER + ALT + Print` → screenshot fullscreen to file
- Multimedia: volume (wpctl), brightness (brightnessctl), playback (playerctl)
- `SUPER + mouse:272` → move window, `SUPER + mouse:273` → resize

### Workspace rules
- `brave` / `brave-browser` (class: `^(brave|brave-browser)$`) → workspace 1
- `com.mitchellh.ghostty` → workspace 2

### Window rules
- Brave/Chromium PiP (title: `^Picture in picture$`): float, pin, position `4% 60%`, size `448x252`, keepaspectratio, nodim, noborder, noshadow
- `org.gnome.Calculator`: float

### Layout
- dwindle with pseudotile and preserve_split
- Border radius: 10px, blur active

### Waybar
- **Config**: `waybar/.config/waybar/config` — workspaces (left), clock/idle_inhibitor (center), system-tray/pulseaudio/power button (right)
- **Style**: `waybar/.config/waybar/style.css` — Catppuccin Mocha theme, workspaces synced via Hyprland IPC

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

- `lazy-lock.json` is gitignored (nvim lazy.nvim lockfile, intentionally untracked)
- `bashrc-omb-bk` in `bash/` is a manual backup, not deployed by stow
- `kitty/kitty.conf.back` is a manual backup
- `hyprland.conf.bak` is decommissioned — `hyprland.lua` is the sole active config
- No CI, tests, linting, or type checking — purely config management
- After cloning tmux config, manually install TPM plugins with `Prefix + I`
