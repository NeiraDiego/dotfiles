vim.cmd("set expandtab")
vim.cmd("set tabstop=2")
vim.cmd("set softtabstop=2")
vim.cmd("set shiftwidth=2")
vim.g.mapleader = " "
vim.g.background = "light"

vim.opt.swapfile = false
vim.opt.number = true
vim.opt.relativenumber = true

-- Navigate vim panes better
vim.keymap.set('n', '<c-k>', ':wincmd k<CR>')
vim.keymap.set('n', '<c-j>', ':wincmd j<CR>')
vim.keymap.set('n', '<c-h>', ':wincmd h<CR>')
vim.keymap.set('n', '<c-l>', ':wincmd l<CR>')
vim.keymap.set('n', '<leader>pv', ':vs<CR>')
vim.keymap.set('n', '<leader>ph', ':sp<CR>')
vim.keymap.set('n', '<leader>conf', ':e ~/.config/nvim/lua/vim-options.lua<CR>')
vim.keymap.set('n', '<leader>bn', ':bn<CR>')
vim.keymap.set('n', '<leader>bp', ':bp<CR>')

vim.keymap.set('n', '<leader>h', ':nohlsearch<CR>')
vim.keymap.set('n', '<leader>ee', ':Neotree toggle<CR>')
vim.keymap.set('n', '<leader>ww', ':w<CR>')
vim.keymap.set('n', '<leader>qq', ':q!<CR>')
vim.keymap.set('n', '<leader>wq', ':wq<CR>')

-- lsp warnings hide or show
vim.keymap.set('n', '<leader>wh', ':lua vim.diagnostic.config({virtual_text=false})<CR>')
vim.keymap.set('n', '<leader>ws', ':lua vim.diagnostic.config({virtual_text=true})<CR>')

