#!/usr/bin/env python3

"""
shellgen.py

A CLI tool that uses Ollama + Code Llama to generate Bash or PowerShell commands from natural language.
"""

import argparse
import subprocess
import sys

# Few‑shot prompt template with Python str.format()
PROMPT_TMPL = """\
    You are an AI expert shell script assistant.
    Generate *only* the {shell} command(s) (no explanations, no comments) to accomplish the user’s request.

    ### Examples
    # List all files modified in the last 24 hours
    find . -type f -mtime -1

    # Show disk usage in human‑readable form
    du -sh /*

    # Create a directory if it does not exist
    [ -d /opt/mydir ] || mkdir -p /opt/mydir

    ### User request:
    {request}
"""

def make_prompt(request: str, shell: str = "bash") -> str:
    # Fill in the placeholders
    return PROMPT_TMPL.format(shell=shell, request=request)

def generate_script(prompt: str, model: str) -> str:
    try:
        # Pass the prompt as a positional argument instead of --prompt
        proc = subprocess.run(
            ["ollama", "run", model, prompt],
            text=True, capture_output=True, check=True
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"❌ Ollama error: {e.stderr.strip()}")
    return proc.stdout.strip()

def main():
    parser = argparse.ArgumentParser(
        description="Generate bash or PowerShell snippets via Ollama + Code Llama"
    )
    parser.add_argument(
        "-m", "--model",
        default="codellama:latest",
        help="Ollama model name (default: %(default)s)"
    )
    parser.add_argument(
        "-s", "--shell",
        choices=["bash", "powershell"],
        default="bash",
        help="Target shell (bash or powershell)"
    )
    parser.add_argument(
        "request",
        nargs="+",
        help="Natural-language description of what you want the script to do"
    )
    args = parser.parse_args()

    # Rebuild the request string from CLI words
    user_req = " ".join(args.request)
    # Build the prompt and call Ollama
    prompt = make_prompt(user_req, args.shell)
    snippet = generate_script(prompt, args.model)

    # Print out the raw commands
    print(f"\n🔧 Generated {args.shell} snippet:\n")
    print(snippet)

if __name__ == "__main__":
    main()
