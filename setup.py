#!/usr/bin/env python3
import subprocess
import os
import sys

def install_dependencies():
    print("Installing dependencies...")
    try:
        # Install required Python packages
        subprocess.run(["pip3", "install", "python-dotenv", "openai"], check=True)
    except subprocess.CalledProcessError as e:
        print("Failed to install dependencies:", e)
        sys.exit(1)

def setup_env():
    api_key = input("Enter your OpenAI API key: ").strip()
    if not api_key:
        print("API key cannot be empty!")
        sys.exit(1)
    # Write the API key to the .env file
    with open(".env", "w") as f:
        f.write("API_KEY=" + api_key + "\n")
    print(".env file created.")

def create_alias():
    # Determine absolute path to helpme.sh
    current_dir = os.getcwd()
    helpme_path = os.path.join(current_dir, "helpme.sh")
    # Determine which shell configuration file to update
    shell = os.environ.get("SHELL", "")
    if "bash" in shell:
        rc_file = os.path.expanduser("~/.bashrc")
    elif "zsh" in shell:
        rc_file = os.path.expanduser("~/.zshrc")
    else:
        print("Shell not recognized. Please add the alias manually.")
        return
    alias_command = f"alias helpme='bash {helpme_path}'\n"
    # Append the alias to the appropriate shell configuration file
    with open(rc_file, "a") as f:
        f.write("\n# Alias for helpme command added by setup script\n")
        f.write(alias_command)
    print(f"Alias added to {rc_file}. To use it immediately, run: source {rc_file}")

if __name__ == "__main__":
    install_dependencies()
    setup_env()
    create_alias()
    print("Setup completed successfully.")
