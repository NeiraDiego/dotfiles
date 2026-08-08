-- Misc (migrado desde dotfiles)

hl.config({
    dwindle = {
        preserve_split = true, -- You probably want this
    },
})

-- Layouts (valores por defecto)
hl.config({
    master = {
        new_status = "master",
    },
})

hl.config({
    scrolling = {
        fullscreen_on_one_column = true,
    },
})

hl.config({
    misc = {
        force_default_wallpaper = -1,    -- Set to 0 or 1 to disable the anime mascot wallpapers
        disable_hyprland_logo   = false, -- If true disables the random hyprland logo / anime girl background. :(
    },
})

-- Features CachyOS (decidir en DECISIONS.md B10/B13)
-- hl.config({
--     misc = {
--         middle_click_paste = false,
--         enable_swallow     = true,
--         swallow_regex      = "(kitty|ghostty|[Kk]onsole|Alacritty|gnome-terminal|xfce[0-9]?-terminal)",
--         vrr                = 3,
--     },
--     xwayland = {
--         force_zero_scaling = true,
--     },
--     ecosystem = {
--         no_update_news   = true,
--         no_donation_nag  = true,
--     },
-- })
