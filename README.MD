# 🐚 ShellGen — Natural Language to Shell Commands

A simple CLI tool that uses [Ollama](https://ollama.com) with Code Llama to generate `bash` or 
`powershell` commands from plain English descriptions.

---

## ✅ Requirements

- Python 3.7+
- [Ollama](https://ollama.com) installed and running locally
- A pulled model like `codellama:latest`

---

## 🚀 Setup

```bash
git clone <your-repo-url>
cd shellgen
chmod +x shellgen.py

🧠 Example Usage

Bash example:
./shellgen.py --shell bash "find all files larger than 100MB in /var/log"

Output:
find /var/log -type f -size +100M

‼️ Powershell is not accurate as of now, go with the bash, I will update here once it's 
good to go ‼️

PowerShell example:
./shellgen.py --shell powershell "list all running processes sorted by CPU usage"

Output:
Get-Process | Sort-Object CPU


⚙️ Options
--model (optional): Specify which Ollama model to use (default: codellama:latest)

--shell (required): Choose between bash or powershell

🆘 Help
./shellgen.py --help

📦 How It Works
ShellGen constructs a structured few-shot prompt and sends it to your local LLM using:
ollama run codellama:latest "<prompt>"
It extracts and prints only the command output, suitable for immediate use.

## ⚠️ Limitations

This tool generates accurate Bash commands for most simple and moderately complex natural language 
inputs. While it can handle complex scenarios as well, in rare cases the generated commands may 
require manual verification or correction.