#DICTIONARY APP USING PYTHON AND TKINTER

import tkinter as tk
import ttkbootstrap as tb
import requests

# function to call api and get meaning
def get_meaning(word):
    if word == "":
        return "Please type a word."

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        r = requests.get(url, timeout=5)
    except:
        return "Error: check your internet connection."

    if r.status_code != 200:
        return f"No meaning found for '{word}'."

    data = r.json()

    try:
        meanings = data[0]["meanings"]
    except (IndexError, KeyError):
        return f"No meaning found for '{word}'."

    lines = []
    count = 1
    for m in meanings:
        part = m.get("partOfSpeech", "unknown")
        defs = m.get("definitions", [])
        if not defs:
            continue
        d_text = defs[0].get("definition", "")
        example = defs[0].get("example", "")

        lines.append(f"{count}. ({part}) {d_text}")
        if example:
            lines.append(f"   eg: {example}")
        lines.append("")
        count += 1
        
    if not lines:
        return f"No meaning found for '{word}'."

    return "\n".join(lines)

def search():
    word = word_entry.get().strip()
    result = get_meaning(word)

    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)
    output_box.config(state="disabled")

def clear():
    word_entry.delete(0, tk.END)
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")
    word_entry.focus()

# main window
app = tb.Window(themename="flatly")
app.title("Dictionary App")
app.geometry("650x400")

title_label = tb.Label(app, text="Mini Dictionary", font=("Segoe UI", 18, "bold"))
title_label.pack(pady=10)

top_frame = tb.Frame(app)
top_frame.pack(pady=5, padx=10, fill="x")

word_label = tb.Label(top_frame, text="Word :", font=("Segoe UI", 11, "bold"))
word_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

word_entry = tb.Entry(top_frame, width=25, font=("Segoe UI", 11))
word_entry.grid(row=0, column=1, padx=5, pady=5)
word_entry.focus()

search_btn = tb.Button(top_frame, text="Search", bootstyle="primary", command=search)
search_btn.grid(row=0, column=2, padx=5, pady=5)

clear_btn = tb.Button(top_frame, text="Clear", bootstyle="secondary", command=clear)
clear_btn.grid(row=0, column=3, padx=5, pady=5)

bottom_frame = tb.Frame(app)
bottom_frame.pack(padx=10, pady=10, fill="both", expand=True)

scroll = tb.Scrollbar(bottom_frame, orient="vertical")
scroll.pack(side="right", fill="y")

output_box = tk.Text(
    bottom_frame,
    wrap="word",
    height=12,
    font=("Segoe UI", 11),
    state="disabled",
)
output_box.pack(fill="both", expand=True)

output_box.config(yscrollcommand=scroll.set)
scroll.config(command=output_box.yview)

app.bind("<Return>", lambda event: search())

app.mainloop()