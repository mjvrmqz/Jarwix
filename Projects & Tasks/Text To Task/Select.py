import tkinter as tk
import sys

def show_method_dialog():
    result = {"choice": None}
    root = tk.Tk()
    root.title("")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()
    tk.Label(frame, text="How would you like to add your task?", font=("Helvetica", 14, "bold")).pack(pady=(0, 15))
    def choose(option):
        result["choice"] = option
        root.destroy()
    tk.Button(frame, text="Manual", width=20, command=lambda: choose("Manual")).pack(pady=5)
    tk.Button(frame, text="Audio", width=20, command=lambda: choose("Audio")).pack(pady=5)
    root.mainloop()
    return result["choice"]

def show_text_input():
    result = {"text": None, "hours": None}
    root = tk.Tk()
    root.title("")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()
    tk.Label(frame, text="What's on your mind?", font=("Helvetica", 14, "bold")).pack(pady=(0, 10))
    text_box = tk.Text(frame, width=40, height=5, font=("Helvetica", 12))
    text_box.pack(pady=(0, 15))
    text_box.focus()
    tk.Label(frame, text="How many hours?", font=("Helvetica", 12)).pack(pady=(0, 5))
    hours_var = tk.StringVar(value="1")
    spinbox = tk.Spinbox(frame, from_=0.5, to=24, increment=0.5, textvariable=hours_var, width=10, font=("Helvetica", 12), format="%.1f")
    spinbox.pack(pady=(0, 15))
    def submit(event=None):
        text = text_box.get("1.0", tk.END).strip()
        try:
            hours = float(hours_var.get())
            hours = int(hours) if hours == int(hours) else hours
        except ValueError:
            hours = 1
        result["text"] = text
        result["hours"] = hours
        root.destroy()
    tk.Button(frame, text="Continue", width=20, command=submit).pack()
    root.bind("<Return>", submit)
    root.mainloop()
    return result["text"], result["hours"]

def show_tag_selector():
    tags = ["#ActionableSteps", "#NotionCalendar", "#EndOfDay", "#macOS"]
    result = {"selected": None}
    root = tk.Tk()
    root.title("")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()
    tk.Label(frame, text="Would you like to add any tags?", font=("Helvetica", 14, "bold")).pack(pady=(0, 15))
    vars = []
    for tag in tags:
        var = tk.BooleanVar(value=True)
        tk.Checkbutton(frame, text=tag, variable=var, font=("Helvetica", 12)).pack(anchor="w")
        vars.append(var)
    def submit():
        result["selected"] = [tags[i] for i, v in enumerate(vars) if v.get()]
        root.destroy()
    tk.Button(frame, text="Done", width=20, command=submit).pack(pady=(15, 0))
    root.mainloop()
    return result["selected"]

def main():
    method = show_method_dialog()
    if method is None:
        sys.exit(0)
    if method == "Manual":
        task_text, hours = show_text_input()
        if not task_text:
            sys.exit(0)
        selected_tags = show_tag_selector()
        if selected_tags is None:
            sys.exit(0)
        tags_line = " ".join(selected_tags)
        print(f"{task_text}. {hours} hours\n{tags_line}")
    elif method == "Audio":
        print("AUDIO_SELECTED")

if __name__ == "__main__":
    main()
