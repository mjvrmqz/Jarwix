#!/usr/bin/env python3
import subprocess
import sys

TEXT_TO_TASK_SELECT = "/Users/mjvrmqz/Personal/Scripts/Notion/Jarwix/Text To Task/Select.py"
PYTHON = "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"

def ask(prompt, options):
    items = ", ".join(f'"{o}"' for o in options)
    script = f'choose from list {{{items}}} with title "Quick Schedule" with prompt "{prompt}" without multiple selections allowed and empty selection allowed'
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    output = result.stdout.strip()
    return None if output == "false" or not output else output

def main():
    choice = ask("How would you like to plan?", ["From Scratch", "Choose From Pre-Existing"])
    if not choice:
        sys.exit(0)

    if choice == "From Scratch":
        result = subprocess.run([PYTHON, TEXT_TO_TASK_SELECT], capture_output=True, text=True)
        if result.returncode != 0:
            sys.exit(1)
        output = result.stdout.strip()
        if output:
            print(output)

if __name__ == "__main__":
    main()
