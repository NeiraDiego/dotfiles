-- Hyprland Lua configuration (estructura CachyOS)
-- Módulos migrados desde hyprland.lua.monolithic.bak
-- Decisiones pendientes en DECISIONS.md


-------------------------------
---- HOST DETECTION ----
-------------------------------

local function get_hostname()
    local handle = io.popen("hostname")
    if handle then
        local hostname = handle:read("*a"):gsub("%s+", "")
        handle:close()
        return hostname
    end
    return ""
end

local HOST = get_hostname()
local IS_SERVER = (HOST == "DiegoArchSV")


-----------------
---- MODULES ----
-----------------

require("config.animations")
require("config.autostart")
require("config.colors")
require("config.decorations")
require("config.variables")
require("config.environment")
require("config.inputs")
require("config.binds")
require("config.misc")
require("config.monitors")
require("config.windowrules")
require("config.workspaces")
