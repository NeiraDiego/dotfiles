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
| `hypr/CONTEXT.md` | **Primary reference** for Hyprland config — monitors, keybinds, window rules, autostart |
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
- See `hypr/CONTEXT.md` for current monitor layout, keybindings, autostart order, and window rules

## Neovim

- Plugin manager: lazy.nvim (auto-installs on first launch)
- Config modules: `lua/config/options.lua`, `lua/config/keymaps.lua`
- Plugins: `lua/plugins/*.lua` (13 plugins)
- OpenCode integration via `opencode.nvim` with `<leader>a*` keymaps

## Pre-existing instruction files

### `hypr/CONTEXT.md`
Hyprland-specific context (monitors, keybinds, autostart, window rules, layout). Agents editing hyprland config should read this first.

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
