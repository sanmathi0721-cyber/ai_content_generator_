from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Simple local text generator (no API key needed)
responses = [
    "AI is changing the world by automating tasks and enhancing creativity.",
    "Machine learning enables computers to learn from data and improve over time.",
    "Artificial intelligence combines algorithms and data to make intelligent decisions.",
    "Future of AI lies in human collaboration and ethical development."
]

@app.route("/")
def home():
    return jsonify({"message": "AI Generator backend is running!"})

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    # Generate a random creative response
    content = f"{prompt} — {random.choice(responses)}"
    return jsonify({"result": content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
