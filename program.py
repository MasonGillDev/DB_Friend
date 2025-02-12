import subprocess
from dotenv import load_dotenv
from openai import OpenAI
import sys
import os
load_dotenv()

api_key = os.environ.get("API_KEY")
if not api_key:
    raise ValueError("No API key found. Please set the API_KEY environment variable.")

OpenAI.api_key = api_key

client = OpenAI()

# Detect the current shell
shell_name = os.path.basename(os.environ.get("SHELL", "unknown"))


if shell_name == "zsh":
    shell_instruction = "Program for Zsh NOT BASH."
elif shell_name == "bash":
    shell_instruction = "Program for Bash."
else:
    shell_instruction = f"Program for {shell_name}, behavior may be different."

sys.stderr.write("How Can I Help You? ")
initial_prompt = input()

with open("/Users/masongill/Desktop/DB_friend/prompt.txt", "w") as f:
    f.write(initial_prompt)

# Call the OpenAI API
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": (
                "You only return commands that executes the user's request. If you cannot safely execute the command, return an error message. You are to return all the necessary commands to fulfill the user's request. "
                "Do not include Markdown formatting, code block markers, or any extra text. "
                + shell_instruction
            )
        },
        {"role": "user", "content": initial_prompt}
    ]
)

raw_output = completion.choices[0].message.content.strip()

def clean_command(text):
    lines = text.splitlines()
    filtered_lines = [line for line in lines if not line.strip().startswith("```")]
    cleaned = "\n".join(filtered_lines).strip()

    if cleaned.startswith("#!/bin/bash"):
        cleaned = "\n".join(cleaned.splitlines()[1:]).strip()
    
    return cleaned

command = clean_command(raw_output)

print(command)
