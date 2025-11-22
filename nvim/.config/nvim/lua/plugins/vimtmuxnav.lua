return {
  "christoomey/vim-tmux-navigator",
  lazy = false,
  cmd = {
    "TmuxNavigateLeft",
    "TmuxNavigateDown",
    "TmuxNavigateUp",
    "TmuxNavigateRight",
    "TmuxNavigatePrevious",
    "TmuxNavigatorProcessList",
  },
  keys = {
    { "<c-h>", "<cmd><C-b>TmuxNavigateLeft<cr>" },
    { "<c-j>", "<cmd><C-b>TmuxNavigateDown<cr>" },
    { "<c-k>", "<cmd><C-b>TmuxNavigateUp<cr>" },
    { "<c-l>", "<cmd><C-b>TmuxNavigateRight<cr>" },
    { "<c-\\>", "<cmd><C-b>TmuxNavigatePrevious<cr>" },
  },
}
