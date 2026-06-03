#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PREFERRED_TARGET_DIRS=(
  "$HOME/.local/bin"
  "$HOME/bin"
)
SHARE_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/chronora"
TEMPLATE_DIR="$SHARE_DIR/templates"
SOURCE_SCRIPT="$SCRIPT_DIR/bin/cclaude"
SOURCE_CURRENT_TEMPLATE="$SCRIPT_DIR/templates/current.md"
SOURCE_LOCAL_TEMPLATE="$SCRIPT_DIR/templates/CLAUDE.local.md"

abort() {
  printf 'chronora install: %s\n' "$1" >&2
  exit 1
}

path_contains() {
  local dir=$1
  [[ ":$PATH:" == *":$dir:"* ]]
}

path_export_line() {
  local dir=$1

  case "$dir" in
    "$HOME/.local/bin")
      printf '%s\n' 'export PATH="$HOME/.local/bin:$PATH"'
      ;;
    "$HOME/bin")
      printf '%s\n' 'export PATH="$HOME/bin:$PATH"'
      ;;
    *)
      printf 'export PATH="%s:$PATH"\n' "$dir"
      ;;
  esac
}

python_user_bin_dir() {
  python3 - <<'PY'
import site
import sys
from pathlib import Path

candidates = []
user_base = getattr(site, "USER_BASE", None)
if user_base:
    candidates.append(Path(user_base) / "bin")

scripts_dir = Path(sys.executable).resolve().parent
candidates.append(scripts_dir)

seen = set()
for path in candidates:
    if path in seen:
        continue
    seen.add(path)
    print(path)
    break
PY
}

choose_target_dir() {
  local dir
  local python_bin

  python_bin=$(python_user_bin_dir)
  if [[ -n "$python_bin" ]]; then
    printf '%s\n' "$python_bin"
    return
  fi

  for dir in "${PREFERRED_TARGET_DIRS[@]}"; do
    if path_contains "$dir"; then
      printf '%s\n' "$dir"
      return
    fi
  done

  printf '%s\n' "${PREFERRED_TARGET_DIRS[0]}"
}

ensure_python_and_pip() {
  if ! command -v python3 >/dev/null 2>&1; then
    abort "python3 was not found in PATH. Install Python 3.10+ and rerun ./install.sh."
  fi

  if ! python3 -m pip --version >/dev/null 2>&1; then
    abort "python3 -m pip is unavailable. Install pip for your Python 3 environment and rerun ./install.sh."
  fi
}

install_python_cli() {
  if python3 -m pip install --user .; then
    return
  fi

  if python3 -m pip install --user --break-system-packages .; then
    printf 'chronora install: pip required --break-system-packages in this environment; used it with --user\n'
    return
  fi

  abort "failed to install the Python CLI with pip --user. If your Python is externally managed, install pipx or use a virtual environment, then rerun ./install.sh."
}

TARGET_DIR=$(choose_target_dir)
TARGET_SCRIPT="$TARGET_DIR/cclaude"

if [[ ! -f "$SOURCE_SCRIPT" ]]; then
  abort "missing source script: $SOURCE_SCRIPT"
fi

if [[ ! -f "$SOURCE_CURRENT_TEMPLATE" ]]; then
  abort "missing template: $SOURCE_CURRENT_TEMPLATE"
fi

if [[ ! -f "$SOURCE_LOCAL_TEMPLATE" ]]; then
  abort "missing template: $SOURCE_LOCAL_TEMPLATE"
fi

ensure_python_and_pip

case "$(uname -s)" in
  Darwin|Linux)
    ;;
  *)
    printf 'chronora install: warning: Chronora is currently validated primarily on macOS and Linux.\n' >&2
    ;;
esac

mkdir -p "$TARGET_DIR" "$TEMPLATE_DIR"
cp "$SOURCE_SCRIPT" "$TARGET_SCRIPT"
chmod +x "$TARGET_SCRIPT"
cp "$SOURCE_CURRENT_TEMPLATE" "$TEMPLATE_DIR/current.md"
cp "$SOURCE_LOCAL_TEMPLATE" "$TEMPLATE_DIR/CLAUDE.local.md"

printf 'chronora install: installing Python CLI with pip --user\n'
install_python_cli

printf 'chronora install: installed cclaude to %s\n' "$TARGET_SCRIPT"
printf 'chronora install: installed templates to %s\n' "$TEMPLATE_DIR"
printf 'chronora install: installed chronora CLI into %s\n' "$TARGET_DIR"

if command -v claude >/dev/null 2>&1; then
  printf 'chronora install: Claude Code CLI found at %s\n' "$(command -v claude)"
else
  printf 'chronora install: warning: Claude Code CLI was not found in PATH.\n' >&2
  printf 'chronora install: install it from https://claude.ai/code before running cclaude.\n' >&2
fi

if path_contains "$TARGET_DIR"; then
  printf 'chronora install: %s is already in PATH.\n' "$TARGET_DIR"
else
  printf '\n'
  printf 'chronora install: %s is not in PATH.\n' "$TARGET_DIR"
  printf 'Add this line to ~/.zprofile, ~/.zshrc, or ~/.bashrc, then reload your shell:\n'
  path_export_line "$TARGET_DIR"
fi

printf '\n'
printf 'chronora install: next steps\n'
printf '  1. cd ~/work/your-project\n'
if path_contains "$TARGET_DIR"; then
  printf '  2. cclaude\n'
  printf '  3. chronora restore\n'
else
  printf '  2. reload your shell\n'
  printf '  3. cclaude\n'
  printf '  4. chronora restore\n'
fi
printf '\n'
printf 'On first run, Chronora creates .claude/current.md, .claude/CLAUDE.local.md,\n'
printf 'a root CLAUDE.local.md symlink, and a session archive under .claude/sessions/.\n'
printf 'The chronora CLI can then compute a restore plan from discovered project state.\n'
