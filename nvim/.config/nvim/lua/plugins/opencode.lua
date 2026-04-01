return {
  {
    "nickjvandyke/opencode.nvim",
    version = "*",
    init = function()
      vim.g.opencode_opts = vim.tbl_deep_extend("force", vim.g.opencode_opts or {}, {
        server = {
          start = function()
            require("opencode.terminal").open("opencode --port", {
              split = "right",
              width = math.floor(vim.o.columns * 0.35),
            })
          end,
          stop = function()
            require("opencode.terminal").close()
          end,
          toggle = function()
            require("opencode.terminal").toggle("opencode --port", {
              split = "right",
              width = math.floor(vim.o.columns * 0.35),
            })
          end,
        },
      })
    end,
    keys = {
      {
        "<leader>aa",
        function()
          require("opencode").ask("@this: ", { submit = true })
        end,
        mode = { "n", "x" },
        desc = "Ask OpenCode",
      },
      {
        "<leader>as",
        function()
          require("opencode").select()
        end,
        mode = { "n", "x" },
        desc = "Select OpenCode action",
      },
      {
        "<leader>at",
        function()
          require("opencode").toggle()
        end,
        mode = { "n", "t" },
        desc = "Toggle OpenCode",
      },
      {
        "<leader>ar",
        function()
          require("opencode").prompt("review")
        end,
        mode = { "n", "x" },
        desc = "Review with OpenCode",
      },
      {
        "<leader>af",
        function()
          require("opencode").prompt("fix")
        end,
        mode = { "n", "x" },
        desc = "Fix with OpenCode",
      },
    },
  },
}
