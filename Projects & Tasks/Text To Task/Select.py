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

def main():
    method = show_method_dialog()
    if method is None:
        sys.exit(0)
    if method == "Manual":
        print("MANUAL_SELECTED")
    elif method == "Audio":
        print("AUDIO_SELECTED")

if __name__ == "__main__":
    main()
