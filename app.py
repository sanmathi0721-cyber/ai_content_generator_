from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can call backend

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Health check route
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": "gpt-3.5-turbo"}), 200

# Main AI content generator route
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Generate text using OpenAI
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Write a creative and engaging article about {prompt}. Keep it concise and clear."
                }
            ],
            max_tokens=250,
            temperature=0.8,
        )

        output = completion["choices"][0]["message"]["content"].strip()
        return jsonify({"output": output}), 200

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500


# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ AI Content Generator Backend is running!"}), 200


# Run app locally or on Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
