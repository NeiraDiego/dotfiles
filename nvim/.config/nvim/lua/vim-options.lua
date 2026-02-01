-- ============================================================================
-- CONFIGURACIÓN GENERAL
-- ============================================================================
vim.cmd("set expandtab")
vim.cmd("set tabstop=2")
vim.cmd("set softtabstop=2")
vim.cmd("set shiftwidth=2")
vim.g.mapleader = " "
vim.g.background = "light"

vim.opt.swapfile = false
vim.opt.number = true
vim.opt.relativenumber = true

-- ============================================================================
-- ATAJOS DE TECLADO (KEYMAPS)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- NAVEGACIÓN DE VENTANAS Y SPLITS
-- ----------------------------------------------------------------------------
vim.keymap.set('n', '<c-k>', ':wincmd k<CR>')
vim.keymap.set('n', '<c-j>', ':wincmd j<CR>')
vim.keymap.set('n', '<c-h>', ':wincmd h<CR>')
vim.keymap.set('n', '<c-l>', ':wincmd l<CR>')
vim.keymap.set('n', '<leader>pv', ':vs<CR>')  -- Split vertical
vim.keymap.set('n', '<leader>ph', ':sp<CR>')  -- Split horizontal

-- ----------------------------------------------------------------------------
-- VIM-TMUX-NAVIGATOR
-- ----------------------------------------------------------------------------
-- Nota: Estos atajos están configurados directamente en el archivo del plugin
-- para aprovechar el lazy-loading de lazy.nvim

-- ----------------------------------------------------------------------------
-- GESTIÓN DE BUFFERS
-- ----------------------------------------------------------------------------
vim.keymap.set('n', '<leader>bn', ':bn<CR>')  -- Buffer next
vim.keymap.set('n', '<leader>bp', ':bp<CR>')  -- Buffer previous

-- ----------------------------------------------------------------------------
-- ARCHIVOS Y CONFIGURACIÓN
-- ----------------------------------------------------------------------------
vim.keymap.set('n', '<leader>conf', ':e ~/.config/nvim/lua/vim-options.lua<CR>')
vim.keymap.set('n', '<leader>ww', ':w<CR>')    -- Save
vim.keymap.set('n', '<leader>qq', ':q!<CR>')   -- Quit without saving
vim.keymap.set('n', '<leader>wq', ':wq<CR>')   -- Save and quit

-- ----------------------------------------------------------------------------
-- BÚSQUEDA Y UI
-- ----------------------------------------------------------------------------
vim.keymap.set('n', '<leader>h', ':nohlsearch<CR>')      -- Clear search highlight
vim.keymap.set('n', '<leader>ee', ':Neotree toggle<CR>') -- Toggle file explorer

-- ----------------------------------------------------------------------------
-- TELESCOPE (Fuzzy Finder)
-- ----------------------------------------------------------------------------
vim.keymap.set('n', '<leader>ff', function()
  require('telescope.builtin').find_files()
end, { desc = 'Telescope find files' })

vim.keymap.set('n', '<leader>fg', function()
  require('telescope.builtin').live_grep()
end, { desc = 'Telescope live grep' })

-- ----------------------------------------------------------------------------
-- HARPOON (File Marks)
-- ----------------------------------------------------------------------------
vim.keymap.set("n", "<leader>a", function()
  require("harpoon"):list():add()
end, { desc = 'Harpoon add file' })

vim.keymap.set("n", "<C-e>", function()
  require("harpoon").ui:toggle_quick_menu(require("harpoon"):list())
end, { desc = 'Harpoon toggle menu' })

vim.keymap.set("n", "<C-t>", function()
  require("harpoon"):list():select(2)
end, { desc = 'Harpoon select 2' })

vim.keymap.set("n", "<C-n>", function()
  require("harpoon"):list():select(3)
end, { desc = 'Harpoon select 3' })

vim.keymap.set("n", "<C-s>", function()
  require("harpoon"):list():select(4)
end, { desc = 'Harpoon select 4' })

vim.keymap.set("n", "<C-S-P>", function()
  require("harpoon"):list():prev()
end, { desc = 'Harpoon previous' })

vim.keymap.set("n", "<C-S-N>", function()
  require("harpoon"):list():next()
end, { desc = 'Harpoon next' })

-- ----------------------------------------------------------------------------
-- LSP (Language Server Protocol)
-- ----------------------------------------------------------------------------
vim.keymap.set('n', 'K', vim.lsp.buf.hover, { desc = 'LSP hover' })
vim.keymap.set('n', 'gd', vim.lsp.buf.definition, { desc = 'LSP go to definition' })
vim.keymap.set({'n', 'v'}, '<leader>ca', vim.lsp.buf.code_action, { desc = 'LSP code action' })

-- Formateo de código
vim.keymap.set("n", "<leader>gf", vim.lsp.buf.format, { desc = 'Format code' })

-- LSP diagnostics (warnings/errors)
vim.keymap.set('n', '<leader>wh', ':lua vim.diagnostic.config({virtual_text=false})<CR>', { desc = 'Hide diagnostics' })
vim.keymap.set('n', '<leader>ws', ':lua vim.diagnostic.config({virtual_text=true})<CR>', { desc = 'Show diagnostics' })

-- ----------------------------------------------------------------------------
-- DEBUGGING (nvim-dap)
-- ----------------------------------------------------------------------------
vim.keymap.set("n", "<Leader>dt", function()
  require("dap").toggle_breakpoint()
end, { desc = 'Toggle breakpoint' })

vim.keymap.set("n", "<Leader>dc", function()
  require("dap").continue()
end, { desc = 'Debug continue' })
