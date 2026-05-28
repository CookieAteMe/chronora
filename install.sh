#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
TARGET_DIR="$HOME/bin"
TARGET_SCRIPT="$TARGET_DIR/cclaude"
SHARE_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/chronora"
TEMPLATE_DIR="$SHARE_DIR/templates"
SOURCE_SCRIPT="$SCRIPT_DIR/bin/cclaude"
SOURCE_CURRENT_TEMPLATE="$SCRIPT_DIR/templates/current.md"
SOURCE_LOCAL_TEMPLATE="$SCRIPT_DIR/templates/CLAUDE.local.md"

abort() {
  print "chronora install: $1" >&2
  exit 1
}

if [[ ! -f "$SOURCE_SCRIPT" ]]; then
  abort "missing source script: $SOURCE_SCRIPT"
fi

if [[ ! -f "$SOURCE_CURRENT_TEMPLATE" ]]; then
  abort "missing template: $SOURCE_CURRENT_TEMPLATE"
fi

if [[ ! -f "$SOURCE_LOCAL_TEMPLATE" ]]; then
  abort "missing template: $SOURCE_LOCAL_TEMPLATE"
fi

if [[ "$(uname -s)" != "Darwin" ]]; then
  print "chronora install: warning: Chronora v0.1 is tested primarily on macOS with zsh."
fi

mkdir -p "$TARGET_DIR" "$TEMPLATE_DIR"
cp "$SOURCE_SCRIPT" "$TARGET_SCRIPT"
chmod +x "$TARGET_SCRIPT"
cp "$SOURCE_CURRENT_TEMPLATE" "$TEMPLATE_DIR/current.md"
cp "$SOURCE_LOCAL_TEMPLATE" "$TEMPLATE_DIR/CLAUDE.local.md"

print "chronora install: installed cclaude to $TARGET_SCRIPT"
print "chronora install: installed templates to $TEMPLATE_DIR"

if command -v claude >/dev/null 2>&1; then
  print "chronora install: Claude Code CLI found at $(command -v claude)"
else
  print "chronora install: warning: Claude Code CLI was not found in PATH." >&2
  print "chronora install: install it from https://claude.ai/code before running cclaude." >&2
fi

if [[ ":$PATH:" == *":$TARGET_DIR:"* ]]; then
  print "chronora install: $TARGET_DIR is already in PATH."
else
  print ""
  print "chronora install: $TARGET_DIR is not in PATH."
  print "Add this line to ~/.zshrc, then run 'source ~/.zshrc' or open a new shell:"
  print 'export PATH="$HOME/bin:$PATH"'
fi

print ""
print "chronora install: next steps"
print "  1. cd ~/work/your-project"
print "  2. cclaude"
print ""
print "On first run, Chronora creates .claude/current.md, .claude/CLAUDE.local.md,"
print "a root CLAUDE.local.md symlink, and a session archive under .claude/sessions/."
