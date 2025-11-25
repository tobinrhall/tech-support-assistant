import tkinter as tk
from tkinter import scrolledtext, ttk

import tech_assistant  # uses your existing logic


def send_message(event=None):
    """Send the user's message to the assistant and display the reply."""
    user_text = entry.get().strip()
    if not user_text:
        return

    # Show user message
    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"You: {user_text}\n")
    chat_box.config(state="disabled")
    entry.delete(0, tk.END)

    # Get assistant reply
    try:
        reply = tech_assistant.get_assistant_reply(user_text, docs)
    except Exception as e:
        reply = f"[An error emerges from the burning depths of the network]: {e}"

    # Show assistant reply
    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"Assistant: {reply}\n\n")
    chat_box.see(tk.END)
    chat_box.config(state="disabled")


def on_mode_change(event=None):
    """Handle changes to Normal/Diablo mode from the dropdown."""
    mode = mode_var.get()
    if mode == "Normal":
        tech_assistant.current_system_prompt = tech_assistant.NORMAL_MODE_PROMPT
        tech_assistant.current_mode_name = "Normal"
    elif mode == "Diablo":
        tech_assistant.current_system_prompt = tech_assistant.DIABLO_MODE_PROMPT
        tech_assistant.current_mode_name = "Diablo"

    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"* Mode set to {mode} *\n")
    chat_box.config(state="disabled")
    chat_box.see(tk.END)


def on_level_change(event=None):
    """Handle changes to explanation level (ELI5 / Normal / Advanced)."""
    level = level_var.get()
    tech_assistant.current_level = level

    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"* Level set to {level} *\n")
    chat_box.config(state="disabled")
    chat_box.see(tk.END)


def main():
    global chat_box, entry, mode_var, level_var, docs

    # Load knowledge base once for the GUI
    docs = tech_assistant.load_knowledge_base()

    root = tk.Tk()
    root.title("Tobys Tech Support Assistant of Sanctuary")

    # Top frame for controls
    controls_frame = tk.Frame(root)
    controls_frame.pack(fill="x", padx=8, pady=4)

    # Mode dropdown
    tk.Label(controls_frame, text="Mode:").pack(side="left")
    mode_var = tk.StringVar(value=tech_assistant.current_mode_name)
    mode_combo = ttk.Combobox(
        controls_frame,
        textvariable=mode_var,
        values=["Normal", "Diablo"],
        state="readonly",
        width=10,
    )
    mode_combo.pack(side="left", padx=(2, 10))
    mode_combo.bind("<<ComboboxSelected>>", on_mode_change)

    # Level dropdown
    tk.Label(controls_frame, text="Level:").pack(side="left")
    level_var = tk.StringVar(value=tech_assistant.current_level)
    level_combo = ttk.Combobox(
        controls_frame,
        textvariable=level_var,
        values=["ELI5", "Normal", "Advanced"],
        state="readonly",
        width=10,
    )
    level_combo.pack(side="left", padx=(2, 10))
    level_combo.bind("<<ComboboxSelected>>", on_level_change)

    # Chat display
    chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=24)
    chat_box.pack(fill="both", expand=True, padx=8, pady=(0, 8))
    chat_box.config(state="disabled")

    # Input frame
    input_frame = tk.Frame(root)
    input_frame.pack(fill="x", padx=8, pady=(0, 8))

    entry = tk.Entry(input_frame)
    entry.pack(side="left", fill="x", expand=True)
    entry.bind("<Return>", send_message)

    send_button = tk.Button(input_frame, text="Send", command=send_message)
    send_button.pack(side="left", padx=(4, 0))

    # Intro text
    chat_box.config(state="normal")
    chat_box.insert(
        tk.END,
        "Welcome to the Tech Support Assistant of Sanctuary.\n"
        "Choose Mode and Level above, then type your issue below and press Enter or click Send.\n\n"
    )
    chat_box.config(state="disabled")

    entry.focus()
    root.mainloop()


if __name__ == "__main__":
    main()
