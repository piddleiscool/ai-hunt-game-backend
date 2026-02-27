import os
import json
import hashlib
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Load API key from Render environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

CACHE_FILE = "database.json"

def load_db():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(CACHE_FILE, "w") as f:
        json.dump(db, f)

@app.route("/generate_item", methods=["POST"])
def generate_item():

    data = request.json
    prompt = data.get("prompt", "")

    # Hash request so duplicate requests return cached item
    request_hash = hashlib.md5(prompt.encode()).hexdigest()

    db = load_db()

    if request_hash in db:
        return jsonify(db[request_hash])

    # Call AI once
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a balanced horror survival item generator. Output JSON only."
            },
            {
                "role": "user",
                "content": f"""
Generate a unique strange horror survival item.

Rules:
- Cooldown must be between 8 and 30
- Duration must be between 1 and 6
- Include name, description, ability, cooldown, duration, and risk
- Output JSON only

Prompt: {prompt}
"""
            }
        ]
    )

    item_text = response["choices"][0]["message"]["content"]

    item_data = json.loads(item_text)

    db[request_hash] = item_data
    save_db(db)

    return jsonify(item_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
