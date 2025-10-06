from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# Initialize Flask
app = Flask(__name__)
CORS(app)  # ✅ Allow frontend to access this backend

# ✅ Load your OpenAI API key from Render Environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🩵 Health check route (optional but useful)
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": "gpt-3.5-turbo"}), 200

# 🚀 Main generate route
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # 🧠 OpenAI ChatCompletion request
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
