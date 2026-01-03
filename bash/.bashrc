case $- in
  *i*) ;;
    *) return;;
esac
export OSH='/home/diego/.oh-my-bash'

# hace add, commit y push de los archivos dot
dotcommit() {
    local prev_dir=$(pwd)
    cd ~/dotfiles || return 1
    
    # Agregar todos los cambios
    git add .
    
    # Mostrar el estado
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Archivos modificados:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    git status --short
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Pedir el mensaje de commit
    echo -n "Mensaje del commit: "
    read commit_message
    
    # Verificar que no esté vacío
    if [ -z "$commit_message" ]; then
        echo "❌ Commit cancelado: mensaje vacío"
        cd "$prev_dir"
        return 1
    fi
    
    # Hacer commit y push
    git commit -m "$commit_message"
    
    if [ $? -eq 0 ]; then
        echo "Haciendo push..."
        git push
        echo "✅ Dotfiles actualizados!"
    else
        echo "❌ Error en el commit"
    fi
    
    cd "$prev_dir"
}


case $(hostname) in
  "diegoUbuntuL")
    MACHINE_ICON="🏠"
    ;;
  "orangepi5")
    MACHINE_ICON="🍊"
    ;;
  "DNS-NB")
    MACHINE_ICON="💻"
    ;;
  *)
    MACHINE_ICON="🖳"
    ;;
esac

# Activar mostrar ambientes de Python/Conda
OMB_PROMPT_SHOW_PYTHON_VENV=true

OSH_THEME="rr"
OMB_USE_SUDO=true
completions=(
  git
  composer
  ssh
)
aliases=(
  general
)
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias gitdot='cd ~/dotfiles && git add .'
alias n='nvim .'
alias cda='source ~/conda/bin/activate'
plugins=(
  git
  bashmarks
)

source "$OSH"/oh-my-bash.sh

# Sobrescribir el tema para agregar el icono
function _omb_theme_PROMPT_COMMAND() {
  local arrow="${_omb_prompt_bold_purple}➜${_omb_prompt_reset_color}"
  local user_name="${_omb_prompt_white}\u${_omb_prompt_reset_color}"
  local base_directory="${_omb_prompt_bold_blue}\W${_omb_prompt_reset_color}"
  local GIT_THEME_PROMPT_PREFIX="${_omb_prompt_bold_purple}git:(${_omb_prompt_reset_color}"
  local SVN_THEME_PROMPT_PREFIX="${_omb_prompt_bold_purple}svn:(${_omb_prompt_reset_color}"
  local HG_THEME_PROMPT_PREFIX="${_omb_prompt_bold_purple}hg:(${_omb_prompt_reset_color}"
  local SCM_THEME_PROMPT_SUFFIX="${_omb_prompt_bold_purple})${_omb_prompt_reset_color}"
  local SCM_THEME_PROMPT_CLEAN="${_omb_prompt_bold_green} ✓${_omb_prompt_reset_color}"
  local SCM_THEME_PROMPT_DIRTY="${_omb_prompt_bold_red} ✗${_omb_prompt_reset_color}"
  
  PS1="${arrow} ${user_name} ${MACHINE_ICON} ${base_directory} "
  
  local python_venv
  _omb_prompt_get_python_venv
  PS1+=$python_venv
  local scm_info=$(scm_prompt_info)
  PS1+=${scm_info:+$scm_info }
  PS1+=$_omb_prompt_normal
}
export PATH="$HOME/.local/bin:$PATH"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# opencode
export PATH=/home/diego/.opencode/bin:$PATH
