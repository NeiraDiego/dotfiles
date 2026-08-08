-- Input (migrado desde dotfiles)

hl.config({
    input = {
        kb_layout  = "us, latam",
        kb_variant = "",
        kb_model   = "",
        kb_options = "grp:win_space_toggle",
        kb_rules   = "",

        follow_mouse = 1,

        sensitivity = 0, -- -1.0 - 1.0, 0 significa sin modificación

        touchpad = {
            natural_scroll = false,
        },
    },
})

hl.gesture({
    fingers   = 3,
    direction = "horizontal",
    action    = "workspace",
})

-- Gestos de CachyOS (decidir en DECISIONS.md B11)
-- hl.gesture({ fingers = 4, direction = "horizontal", action = "workspace" })
-- hl.gesture({ fingers = 3, direction = "down",       action = "close" })
-- hl.gesture({ fingers = 3, direction = "up",         action = "fullscreen" })
-- hl.gesture({ fingers = 3, direction = "left",       action = "float" })
