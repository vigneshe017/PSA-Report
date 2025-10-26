# password_tool.py
import getpass
from zxcvbn import zxcvbn
from itertools import permutations, product
import os

print("==== Password Strength Analyzer ====")

# Step 1: Take password input
password = getpass.getpass("Enter your password: ")

# Step 2: Analyze password using zxcvbn
result = zxcvbn(password)
score = result['score']
feedback = result['feedback']

labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
print(f"\nPassword Strength: {labels[score]} (Score: {score}/4)")

if feedback['warning']:
    print("⚠️ Warning:", feedback['warning'])
if feedback['suggestions']:
    print("💡 Suggestions:")
    for s in feedback['suggestions']:
        print("-", s)

# Step 3: Ask if user wants to create a custom wordlist
choice = input("\nDo you want to create a custom wordlist? (y/n): ").lower()

if choice == 'y':
    keywords = input("Enter keywords separated by commas (e.g. name, year, pet): ").split(',')
    keywords = [k.strip() for k in keywords if k.strip()]

    # Step 4: Create folder to save file
    os.makedirs("generated_wordlists", exist_ok=True)
    filename = input("Enter a file name for the wordlist (default: custom.txt): ").strip() or "custom.txt"
    path = os.path.join("generated_wordlists", filename)

    # Step 5: Generate combinations
    combos = set()
    for r in range(1, len(keywords) + 1):
        for combo in product(keywords, repeat=r):
            combos.add(''.join(combo))
        for perm in permutations(keywords, r):
            combos.add(''.join(perm))

    # Step 6: Save to file
    with open(path, "w", encoding="utf-8") as f:
        for c in sorted(combos):
            f.write(c + "\n")

    print(f"\n✅ Wordlist generated successfully! Saved as: {path}")
    print(f"Total combinations: {len(combos)}")
else:
    print("\nNo wordlist generated. Program finished.")
