case $- in
  *i*) ;;
    *) return;;
esac
export OSH='/home/diego/.oh-my-bash'

case $(hostname) in
  "diegoUbuntuL")
    MACHINE_ICON="🏠"
    ;;
  "orangepi5")
    MACHINE_ICON="🍊"
    ;;
  "DiegoNB")
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
