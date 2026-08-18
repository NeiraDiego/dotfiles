-- Monitores (migrado desde dotfiles)
-- Ver tus outputs reales con: hyprctl monitors

if IS_SERVER then
    -- Servidor headless: pantalla virtual para Sunshine
    hl.monitor({
        output   = "HEADLESS-1",
        mode     = "1920x1080@60",
        position = "0x0",
        scale    = 1,
    })
else
    -- PC de escritorio/laptop (DiegoNB)
    hl.monitor({
        output   = "DP-2",
        mode     = "preferred",
        position = "0x-1080",
        scale    = 1,
    })
    hl.monitor({
        output   = "DP-3",
        mode     = "preferred",
        position = "-1920x0",
        scale    = 1,
    })
    hl.monitor({
        output   = "eDP-1",
        mode     = "preferred",
        position = "0x0",
        scale    = 1.57,
    })
    hl.monitor({
        output   = "DP-4",
        mode     = "preferred",
        position = "-1920x0",
        scale    = 1,
    })
    hl.monitor({
        output   = "DP-9",
        mode     = "preferred",
        position = "-1920x0",
        scale    = 1,
    })
end
