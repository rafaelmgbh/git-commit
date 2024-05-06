#!/bin/bash

changed_files=$(git diff --cached --name-only)

if [ -n "$changed_files" ]; then
  commit_message=$(python3 main.py "$changed_files")

  if [ -n "$commit_message" ]; then
    echo "Suggested commit message: $commit_message"
    read -p "Press ENTER to use the suggested commit message, or type a custom one and press ENTER. Press 0 to cancel: " user_input

    if [ "$user_input" = "0" ]; then
      echo "Commit canceled."
    elif [ -z "$user_input" ]; then
      user_input="$commit_message"
      git commit -m "$user_input"
    else
      git commit -m "$user_input"
    fi
  else
    echo "Error: Could not generate commit message."
  fi
else
  echo "No files changed, nothing to commit."
fi
