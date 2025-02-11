#!/bin/bash
# Example: source helpme.sh

# Run your Python program and capture its output (sanitizing it slightly)
cmd=$(python3 /Users/masongill/Desktop/DB_friend/program.py | tr -d '\r' | awk '{$1=$1};1')

echo "Executing:"
echo "$cmd"

# Check for potentially destructive commands
if [[ "$cmd" == *"rm -rf"* ]]; then
    echo "⚠️  WARNING: You are about to execute a destructive command!"
    echo "This will permanently delete files. Do you really want to continue? (yes/no)"
    read -r confirm < /dev/tty
    if [[ "$confirm" != "yes" ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Wait for user confirmation before executing
echo "Press Enter to execute the command..."
read -r dummy < /dev/tty

# Execute the captured command in the current shell session
eval "$cmd"
