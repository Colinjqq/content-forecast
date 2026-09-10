#!/usr/bin/env bash
set -eu

skill_name="content-forecast"
source_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
target="${1:-codex}"

case "$target" in
  codex) destinations="$HOME/.codex/skills/$skill_name" ;;
  claude) destinations="$HOME/.claude/skills/$skill_name" ;;
  all) destinations="$HOME/.codex/skills/$skill_name $HOME/.claude/skills/$skill_name" ;;
  *) echo "Usage: bash update.sh [codex|claude|all]"; exit 2 ;;
esac

if [ -d "$source_dir/.git" ]; then
  echo "Fetching the latest version from GitHub..."
  git -C "$source_dir" pull --ff-only
else
  echo "This folder is not a Git clone, so it cannot fetch updates automatically."
  echo "Download the latest release or clone the repository, then run update.sh again."
  exit 1
fi

version="$(cat "$source_dir/VERSION" 2>/dev/null || echo unknown)"

for destination in $destinations; do
  if [ ! -d "$destination" ]; then
    echo "Not installed: $destination"
    echo "Install first with: bash install.sh $target"
    exit 1
  fi

  parent="$(dirname "$destination")"
  staging="$(mktemp -d "$parent/.content-forecast-update.XXXXXX")"
  backup="$destination.previous"

  tar -C "$source_dir" --exclude='.git' --exclude='.DS_Store' -cf - . | tar -C "$staging" -xf -
  rm -rf "$backup"
  mv "$destination" "$backup"
  if mv "$staging" "$destination"; then
    rm -rf "$backup"
    echo "Updated to v$version: $destination"
  else
    mv "$backup" "$destination"
    echo "Update failed; the previous installation was restored."
    exit 1
  fi
done

echo "Your separate content-forecast-data directory was not touched."
echo "Start a new Agent session to use the updated Skill."
