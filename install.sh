#!/usr/bin/env bash
set -eu
skill_name="content-forecast"
source_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
target="${1:-codex}"
case "$target" in
  codex) destinations="$HOME/.codex/skills/$skill_name" ;;
  claude) destinations="$HOME/.claude/skills/$skill_name" ;;
  all) destinations="$HOME/.codex/skills/$skill_name $HOME/.claude/skills/$skill_name" ;;
  *) echo "Usage: bash install.sh [codex|claude|all]"; exit 2 ;;
esac
for destination in $destinations; do
  mkdir -p "$(dirname "$destination")"
  if [ -e "$destination" ]; then
    echo "Already installed: $destination"
    echo "Remove it first with: bash uninstall.sh $target"
    exit 1
  fi
  cp -R "$source_dir" "$destination"
  rm -f "$destination/.DS_Store"
  echo "Installed: $destination"
done
echo "Start a new Agent session and say: Initialize Content Forecast"
