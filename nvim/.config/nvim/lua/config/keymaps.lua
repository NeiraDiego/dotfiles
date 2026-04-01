vim.keymap.set("n", "<C-k>", "<cmd>wincmd k<CR>", { desc = "Move to upper window" })
vim.keymap.set("n", "<C-j>", "<cmd>wincmd j<CR>", { desc = "Move to lower window" })
vim.keymap.set("n", "<C-h>", "<cmd>wincmd h<CR>", { desc = "Move to left window" })
vim.keymap.set("n", "<C-l>", "<cmd>wincmd l<CR>", { desc = "Move to right window" })
vim.keymap.set("n", "<leader>pv", "<cmd>vsplit<CR>", { desc = "Vertical split" })
vim.keymap.set("n", "<leader>ph", "<cmd>split<CR>", { desc = "Horizontal split" })

vim.keymap.set("n", "<leader>bn", "<cmd>bnext<CR>", { desc = "Next buffer" })
vim.keymap.set("n", "<leader>bp", "<cmd>bprevious<CR>", { desc = "Previous buffer" })

vim.keymap.set("n", "<leader>conf", "<cmd>e ~/.config/nvim/lua/config/options.lua<CR>", { desc = "Edit Neovim options" })
vim.keymap.set("n", "<leader>ww", "<cmd>w<CR>", { desc = "Save" })
vim.keymap.set("n", "<leader>qq", "<cmd>q!<CR>", { desc = "Quit without saving" })
vim.keymap.set("n", "<leader>wq", "<cmd>wq<CR>", { desc = "Save and quit" })

vim.keymap.set("n", "<leader>h", "<cmd>nohlsearch<CR>", { desc = "Clear search highlight" })
vim.keymap.set("n", "<leader>ee", "<cmd>Neotree toggle<CR>", { desc = "Toggle file explorer" })

vim.keymap.set("n", "<leader>ff", function()
  require("telescope.builtin").find_files()
end, { desc = "Find files" })

vim.keymap.set("n", "<leader>fg", function()
  require("telescope.builtin").live_grep()
end, { desc = "Live grep" })

vim.keymap.set("n", "K", vim.lsp.buf.hover, { desc = "LSP hover" })
vim.keymap.set("n", "gd", vim.lsp.buf.definition, { desc = "LSP go to definition" })
vim.keymap.set({ "n", "v" }, "<leader>ca", vim.lsp.buf.code_action, { desc = "LSP code action" })
vim.keymap.set("n", "<leader>gf", vim.lsp.buf.format, { desc = "Format code" })

vim.keymap.set("n", "<leader>wh", function()
  vim.diagnostic.config({ virtual_text = false })
end, { desc = "Hide diagnostics" })

vim.keymap.set("n", "<leader>ws", function()
  vim.diagnostic.config({ virtual_text = true })
end, { desc = "Show diagnostics" })

vim.keymap.set("n", "<Leader>dt", function()
  require("dap").toggle_breakpoint()
end, { desc = "Toggle breakpoint" })

vim.keymap.set("n", "<Leader>dc", function()
  require("dap").continue()
end, { desc = "Debug continue" })
