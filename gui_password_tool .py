# gui_password_tool.py
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from zxcvbn import zxcvbn
from itertools import permutations, product
import os

# Function to check password strength
def analyze_password():
    pw = pw_entry.get()
    if not pw:
        messagebox.showwarning("Error", "Please enter a password.")
        return

    result = zxcvbn(pw)
    score = result['score']
    feedback = result['feedback']

    levels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    strength_label.config(text=f"Strength: {levels[score]}", fg="blue")

    # Show feedback
    warn = feedback.get("warning", "")
    sugg = feedback.get("suggestions", [])
    feedback_text = ""
    if warn:
        feedback_text += f"⚠️ {warn}\n"
    if sugg:
        feedback_text += "💡 " + "\n💡 ".join(sugg)
    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, feedback_text)
    result_box.config(state="disabled")

# Function to generate custom wordlist
def generate_wordlist():
    kws = simpledialog.askstring("Keywords", "Enter keywords separated by commas (e.g. name,year,pet):")
    if not kws:
        return

    keywords = [k.strip() for k in kws.split(",") if k.strip()]
    os.makedirs("generated_wordlists", exist_ok=True)
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialdir="generated_wordlists",
        title="Save Wordlist As",
        filetypes=[("Text files", "*.txt")]
    )
    if not filename:
        return

    combos = set()
    for r in range(1, len(keywords) + 1):
        for combo in product(keywords, repeat=r):
            combos.add("".join(combo))
        for perm in permutations(keywords, r):
            combos.add("".join(perm))

    with open(filename, "w", encoding="utf-8") as f:
        for c in sorted(combos):
            f.write(c + "\n")

    messagebox.showinfo("Success", f"✅ Wordlist generated!\nSaved to:\n{filename}\nTotal: {len(combos)} combinations.")

# GUI setup
root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("400x350")
root.resizable(False, False)

tk.Label(root, text="Enter Password:", font=("Arial", 11)).pack(pady=10)
pw_entry = tk.Entry(root, show="*", width=30)
pw_entry.pack(pady=5)

tk.Button(root, text="Check Strength", command=analyze_password, bg="lightblue").pack(pady=5)
tk.Button(root, text="Generate Wordlist", command=generate_wordlist, bg="lightgreen").pack(pady=5)

strength_label = tk.Label(root, text="Strength: ", font=("Arial", 11, "bold"))
strength_label.pack(pady=10)

result_box = tk.Text(root, height=6, width=45, state="disabled", wrap="word")
result_box.pack(pady=10)

tk.Label(root, text="Developed by Vignesh E", font=("Arial", 9, "italic"), fg="gray").pack(side="bottom", pady=5)

root.mainloop()
