#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
TARGET_DIR="$HOME/bin"
TARGET_SCRIPT="$TARGET_DIR/cclaude"
SHARE_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/chronora"
TEMPLATE_DIR="$SHARE_DIR/templates"

mkdir -p "$TARGET_DIR" "$TEMPLATE_DIR"
cp "$SCRIPT_DIR/bin/cclaude" "$TARGET_SCRIPT"
chmod +x "$TARGET_SCRIPT"
cp "$SCRIPT_DIR/templates/current.md" "$TEMPLATE_DIR/current.md"
cp "$SCRIPT_DIR/templates/CLAUDE.local.md" "$TEMPLATE_DIR/CLAUDE.local.md"

print "Installed cclaude to $TARGET_SCRIPT"
print "Installed templates to $TEMPLATE_DIR"

if [[ ":$PATH:" == *":$TARGET_DIR:"* ]]; then
  print "$TARGET_DIR is already in PATH."
else
  print ""
  print "$TARGET_DIR is not in PATH."
  print "Add this line to ~/.zshrc:"
  print 'export PATH="$HOME/bin:$PATH"'
fi

print ""
print "Installation complete."
print "Run 'cclaude' from a project root to start a Chronora session."
