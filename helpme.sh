#!/bin/bash
# helpme.sh: Execute AI-generated commands with safeguards

# Run your Python program and capture its output (sanitizing it slightly)
cmd=$(python3 ~/DB_Friend/program.py | tr -d '\r' | awk '{$1=$1};1')

echo "Executing:"
echo "$cmd"

# Define an array of destructive command patterns
destructive_patterns=(
    "rm"
    "rm -rf"
    "rm -rf /"
    "rm -rf ~"
    "dd if=/dev/zero"
    "mkfs"
    ":(){ :|:& };:"  # Fork bomb pattern
    "shutdown"
    "reboot"
    "chmod -R 000"
    "chown -R"
)

# Check if any destructive pattern is found in the command
destructive_found=0
for pattern in "${destructive_patterns[@]}"; do
    if [[ "$cmd" == *"$pattern"* ]]; then
        echo "⚠️  WARNING: Destructive command pattern detected: '$pattern'"
        destructive_found=1
    fi
done
# If a destructive pattern is detected, ask for extra confirmation
if [[ $destructive_found -eq 1 ]]; then
    echo "This command may be destructive. Do you really want to continue? (yes/no)"
    read -r confirm < /dev/tty
    if [[ "$confirm" != "yes" ]]; then
        echo "Aborted."
        exit 1
    fi
    exit 1
fi

# Wait for user confirmation before executing
echo "Press Enter to execute the command..."
read -r dummy < /dev/tty



echo "Executing: $cmd"
eval "$cmd" 2>&1 | tee ~/DB_Friend/output.txt | grep --color=always -i "error\|failed\|no such file\|not found"
eval "$cmd"



output="~/DB_Friend/output.txt"
command="$cmd"


if grep -qi "error\|failed\|no such file\|not found" ~/DB_Friend/output.txt; then
    while
        echo "Error detected. Re-running the Python program..."
        cmd=$(python3 ~/DB_Friend/debugger.py "$output" "$command" | tr -d '\r' | awk '{$1=$1};1')

        echo "Executing:"
        echo "$cmd"

        # Define an array of destructive command patterns
        destructive_patterns=(
            "rm"
            "rm -rf"
            "rm -rf /"
            "rm -rf ~"
            "dd if=/dev/zero"
            "mkfs"
            ":(){ :|:& };:"  # Fork bomb pattern
            "shutdown"
            "reboot"
            "chmod -R 000"
            "chown -R"
        )

        # Check if any destructive pattern is found in the command
        destructive_found=0
        for pattern in "${destructive_patterns[@]}"; do
            if [[ "$cmd" == *"$pattern"* ]]; then
                echo "⚠️  WARNING: Destructive command pattern detected: '$pattern'"
                destructive_found=1
            fi
        done
        # If a destructive pattern is detected, ask for extra confirmation
        if [[ $destructive_found -eq 1 ]]; then
            echo "This command may be destructive. Do you really want to continue? (yes/no)"
            read -r confirm < /dev/tty
            if [[ "$confirm" != "yes" ]]; then
                echo "Aborted."
                exit 1
            fi
        fi

        # Wait for user confirmation before executing
        echo "Press Enter to execute the command..."
        read -r dummy < /dev/tty



        echo "Executing: $cmd"
        eval "$cmd" 2>&1 | tee ~/DB_Friend/output.txt | grep --color=always -i "error\|failed\|no such file\|not found"

        output="~/DB_Friend/output.txt"
        command="$cmd"
fi
