#!/usr/bin/env python3
import subprocess
import sys

def ask(prompt, options):
    items = ", ".join(f'"{o}"' for o in options)
    script = f'choose from list {{{items}}} with title "Quick Schedule" with prompt "{prompt}" without multiple selections allowed and empty selection allowed'
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    output = result.stdout.strip()
    return None if output == "false" or not output else output

def get_taken_groups():
    script = '''
    tell application "Calendar"
        set groupNames to {}
        set todays_date to current date
        set start_of_day to todays_date
        set hours of start_of_day to 0
        set minutes of start_of_day to 0
        set seconds of start_of_day to 0
        set end_of_day to start_of_day + (23 * hours + 59 * minutes + 59)
        repeat with c in every calendar
            try
                set dayEvents to (every event of c whose start date >= start_of_day and start date <= end_of_day)
                repeat with e in dayEvents
                    try
                        set evName to summary of e
                        repeat with i from 1 to 5
                            if evName contains ("Group " & i) then
                                set end of groupNames to i
                            end if
                        end repeat
                    end try
                end repeat
            end try
        end repeat
        return groupNames
    end tell
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    taken = set()
    for token in result.stdout.replace(",", " ").split():
        try:
            taken.add(int(token))
        except ValueError:
            pass
    return taken

def find_next_group():
    taken = get_taken_groups()
    if not taken:
        return "Group 1"
    highest = max(taken)
    if highest >= 5:
        return None
    return f"Group {highest + 1}"

def main():
    choice = ask("What would you like to do?", ["Group Tasks", "Edit Tasks", "Remove Tasks"])
    if not choice:
        sys.exit(0)

    if choice == "Group Tasks":
        next_group = find_next_group()
        if next_group is None:
            print("All groups taken", flush=True)
        else:
            print(next_group, flush=True)
    elif choice == "Edit Tasks":
        print("EDIT_SELECTED", flush=True)
    elif choice == "Remove Tasks":
        print("REMOVE_SELECTED", flush=True)

    sys.exit(0)

if __name__ == "__main__":
    main()
