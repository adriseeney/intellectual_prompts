from flask import Flask, render_template
import random
import csv

app = Flask(__name__)

def get_random_prompt():
    """Reads prompts from a CSV file and returns a random (concept, prompt) pair."""
    try:
        with open("prompts.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)  # expects headers: concept,prompt
            rows = [row for row in reader if row.get("prompt")]

        if not rows:
            return ("", "No prompts found. Check your CSV contents.")

        row = random.choice(rows)
        concept = (row.get("concept") or "").strip()
        prompt = (row.get("prompt") or "").strip()
        return (concept, prompt)

    except FileNotFoundError:
        return ("", "Prompts file not found. Make sure prompts.csv is in the same folder as app.py.")
    except Exception as e:
        return ("", f"Error reading prompts: {e}")

@app.route("/")
def index():
    concept, prompt = get_random_prompt()
    return render_template("index.html", concept=concept, prompt=prompt)

if __name__ == "__main__":
    app.run(debug=True)
