import os
import json
import hashlib
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Load API key from Render environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

client = openai.OpenAI()

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

    try:
        data = request.json
        prompt = data.get("prompt", "")

        request_hash = hashlib.md5(prompt.encode()).hexdigest()

        db = load_db()

        # Return cached item if exists
        if request_hash in db:
            return jsonify(db[request_hash])

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a horror survival item generator. Output JSON only."
                },
                {
                    "role": "user",
                    "content": f"""
Generate a strange horror survival item.

Rules:
- Return valid JSON only.
- Fields required:
name
description
ability
cooldown (8-30)
duration (1-6)
risk

Prompt: {prompt}
"""
                }
            ]
        )

        item_text = response.choices[0].message.content

        item_data = json.loads(item_text)

        db[request_hash] = item_data
        save_db(db)

        return jsonify(item_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
