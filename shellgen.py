#!/usr/bin/env python3
"""
shellgen.py

A CLI tool that uses Ollama + Code Llama to generate Bash or PowerShell commands from natural language.
"""

import argparse
import subprocess
import sys

PROMPT_TMPL = """\
You are an AI expert shell script assistant.  Follow these conversion templates:

1. Top‑N largest files → 
   find <path> -type f -exec du -h {{}} + 2>/dev/null \
     | sort -hr \
     | head -n <N>

2. Recursive grep with ignore → 
   find <path> -path "./<ignore_dir>" -prune -o \
        -type f -name "<pattern>" -exec grep "<pattern>" {{}} +

3. Line counts per file → 
   find <path> -type f -name "<ext>" -exec wc -l {{}} \\;

4. Archive recent logs → 
   find <path> -type f -name "<pattern>" -mtime -<days> -print0 \
     | tar --null -czvf <archive> --files-from=-
     
5. Combined size & time filters →
   find <path> -type f -name "<pattern>" -size +<N>M -mtime -<D> -print0 \
     | tar --null -czvf <archive> --files-from=-

### Examples

# Top‑5 in /home/user:
find /home/user -type f -exec du -h {{}} + 2>/dev/null | sort -hr | head -n 5

# Search TODO in .py except venv:
find . -path "./venv" -prune -o -type f -name "*.py" -exec grep "TODO" {{}} +

### User request:
{request}
"""

def make_prompt(request: str, shell: str = "bash") -> str:
    return PROMPT_TMPL.format(shell=shell, request=request)

def generate_script(prompt: str, model: str) -> str:
    try:
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

    user_req = " ".join(args.request)
    prompt = make_prompt(user_req, args.shell)
    snippet = generate_script(prompt, args.model)

    print(f"\n🔧 Generated {args.shell} snippet:\n")
    print(snippet)

if __name__ == "__main__":
    main()
