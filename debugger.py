from dotenv import load_dotenv
from openai import OpenAI
import sys
import os


if len(sys.argv) < 3:
    print("Usage: debugger.py <output_file> <command> <prompt_file>")
    sys.exit(1)


output_file = sys.argv[1]
command = str(sys.argv[2])
prompt_file = "/Users/masongill/Desktop/DB_friend/prompt.txt"

with open(output_file, "r") as f:
    output_contents = f.read()

with open(prompt_file, "r") as f:
    prompt_contents = f.read()


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


completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": (
                "There is an error in the following command: " + command + "\n"
                "The output of the command is: " + output_contents + "\n"
                "The intended use for the command is: " + prompt_contents + "\n"
                "You Return Commands to fix the problem and forfill the intended use. If you cannot safely execute the command in a single line, return an error message. Offer a new solution to the problem different from the original command. "
                + shell_instruction
            )
        },
        {"role": "user", "content": prompt_contents}
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
