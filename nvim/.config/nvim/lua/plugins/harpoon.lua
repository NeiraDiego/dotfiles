return {
    "ThePrimeagen/harpoon",
    branch = "harpoon2",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function ()
    local builtin = require("harpoon")
      vim.keymap.set("n", "<leader>a", function() harpoon:list():add() end)
      vim.keymap.set("n", "<C-e>", function() harpoon.ui:toggle_quick_menu(harpoon:list()) end)

--      vim.keymap.set("n", "<C-h>", function() harpoon:list():select(1) end)
      vim.keymap.set("n", "<C-t>", function() harpoon:list():select(2) end)
      vim.keymap.set("n", "<C-n>", function() harpoon:list():select(3) end)
      vim.keymap.set("n", "<C-s>", function() harpoon:list():select(4) end)

      -- Toggle previous & next buffers stored within Harpoon list
      vim.keymap.set("n", "<C-S-P>", function() harpoon:list():prev() end)
      vim.keymap.set("n", "<C-S-N>", function() harpoon:list():next() end)
  end,
}
      -- vim.keymap.set('n', '<C-n>', ':Neotree filesystem reveal left<CR>', {})
-- -- List of favorite files/marks per project
--return {
  -- https://github.com/ThePrimeagen/harpoon
--  'ThePrimeagen/harpoon',
--  branch = 'master',
--  event = 'VeryLazy',
--  dependencies = {
    -- https://github.com/nvim-lua/plenary.nvim
--    'nvim-lua/plenary.nvim',
--  },
--  opts = {
--    menu = {
--      width = 120
--    }
--  },
--}
