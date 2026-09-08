#!/usr/bin/env bash
set -eu
skill_name="content-forecast"
target="${1:-codex}"
case "$target" in
  codex) destinations="$HOME/.codex/skills/$skill_name" ;;
  claude) destinations="$HOME/.claude/skills/$skill_name" ;;
  all) destinations="$HOME/.codex/skills/$skill_name $HOME/.claude/skills/$skill_name" ;;
  *) echo "Usage: bash uninstall.sh [codex|claude|all]"; exit 2 ;;
esac
for destination in $destinations; do
  if [ -d "$destination" ]; then
    rm -rf "$destination"
    echo "Removed: $destination"
  else
    echo "Not installed: $destination"
  fi
done
echo "Your content-forecast-data directory was not touched."
