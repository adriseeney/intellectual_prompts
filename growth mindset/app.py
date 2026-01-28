from flask import Flask, render_template
import random
import csv
from datetime import datetime
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "growth_prompts.csv")


def get_random_prompt():
    """Reads prompts from a CSV file and returns a random (concept, prompt) pair."""
    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)  # expects headers: concept,prompt
            rows = [row for row in reader if row.get("prompt")]

        if not rows:
            return ("", "No prompts found. Check your CSV contents.")

        row = random.choice(rows)
        topic = (row.get("topic") or "").strip()
        prompt = (row.get("prompt") or "").strip()
        return (topic, prompt)

    except FileNotFoundError:
        return ("", "Prompts file not found. Make sure prompts.csv is in the same folder as app.py.")
    except Exception as e:
        return ("", f"Error reading prompts: {e}")

@app.route("/")
def index():
    topic, prompt = get_random_prompt()
    return render_template("index.html", topic=topic, prompt=prompt)

@app.before_request
def log_visit():
    with open("visits.log", "a") as f:
        f.write(f"{datetime.utcnow()}\n")

if __name__ == "__main__":
    app.run(debug=True)
