-- Reglas de ventanas y workspaces (migrado desde dotfiles)
-- Reglas exclusivas de CachyOS quedan comentadas (ver DECISIONS.md B)

-- Workspace assignments
hl.window_rule({
    name      = "ghostty-workspace",
    match     = { class = "^com.mitchellh.ghostty$" },
    workspace = 2,
    opacity   = 0.93,
})

hl.window_rule({
    name      = "brave-workspace",
    match     = { class = "^(brave|brave-browser)$" },
    workspace = 1,
})

-- Picture-in-Picture (Brave/Chromium)
hl.window_rule({
    name  = "brave-pip",
    match = { title = "^Picture in picture$" },

    float             = true,
    pin               = true,
    move              = "72% 60%",
    size              = "448 252",
    keep_aspect_ratio = true,
    no_dim            = true,
--    no_border         = true,
    no_shadow         = true,
})

-- Float rules
hl.window_rule({
    name  = "blueman-float",
    match = { class = "^blueman-manager$" },
    float = true,
})

hl.window_rule({
    name  = "gnome-calculator-float",
    match = { class = "^org%.gnome%.Calculator$" },
    float = true,
})

hl.window_rule({
    name    = "wofi-opacity",
    match   = { class = "^wofi$" },
    opacity = 0.90,
})

local suppressMaximizeRule = hl.window_rule({
    -- Ignore maximize requests from all apps. You'll probably like this.
    name  = "suppress-maximize-events",
    match = { class = ".*" },

    suppress_event = "maximize",
})
-- suppressMaximizeRule:set_enabled(false)

hl.window_rule({
    -- Fix some dragging issues with XWayland
    name  = "fix-xwayland-drags",
    match = {
        class      = "^$",
        title      = "^$",
        xwayland   = true,
        float      = true,
        fullscreen = false,
        pin        = false,
    },

    no_focus = true,
})

hl.window_rule({
    name  = "move-hyprland-run",
    match = { class = "hyprland-run" },

    move  = "20 monitor_h-120",
    float = true,
})

-- Reglas de CachyOS (decidir en DECISIONS.md B8/B13)
-- hl.window_rule({ match = { float = true }, center = true, persistent_size = true })
-- local terminals = "^(kitty|ghostty|[Kk]onsole|Alacritty|gnome-terminal|xfce[0-9]?-terminal)$"
-- hl.window_rule({ match = { class = "^(firefox|zen)$" }, opacity = "1.0 override" })
-- hl.window_rule({ match = { class = terminals }, opacity = "1.0 override" })
-- hl.window_rule({ match = { class = "^(mpv|org.kde.haruna|.*plex.*|org\\.kde\\.gwenview|.*vlc.*)$" }, opacity = "1.0 override" })
-- hl.window_rule({ match = { class = "^(.*[Ll]auncher.*)$" }, float = true, monitor = PRIMARY_MONITOR })
-- hl.window_rule({ match = { class = "^(.*\\.exe)$", float = true }, monitor = PRIMARY_MONITOR, center = true, fullscreen_state = 0 })
