import subprocess
from dotenv import load_dotenv
from openai import OpenAI
import sys
import os
load_dotenv()


api_key = os.environ.get("API_KEY")
if not api_key:
    raise ValueError("No API key found. Please set the OPENAI_API_KEY environment variable.")

OpenAI.api_key = api_key

client = OpenAI()



# Print prompt to stderr so it doesn't get captured by command substitution
sys.stderr.write("How Can I Help You? ")
initial_prompt = input()  

# Call the OpenAI API
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": (
                "You only return a single-line Bash command that executes the user's request. If you can not safely execute the command in a single line, return an error message."
                "Do not include Markdown formatting, code block markers, or any extra text."
                "Program for Zsh NOT BASH."
            )
        },
        {"role": "user", "content": initial_prompt}
    ]
)

raw_output = completion.choices[0].message.content.strip()

def clean_command(text):
    # Remove any markdown code fences
    lines = text.splitlines()
    filtered_lines = [line for line in lines if not line.strip().startswith("```")]
    cleaned = "\n".join(filtered_lines).strip()
    
    if cleaned.startswith("#!/bin/bash"):
        cleaned = "\n".join(cleaned.splitlines()[1:]).strip()
    
    return cleaned

command = clean_command(raw_output)

print(command)