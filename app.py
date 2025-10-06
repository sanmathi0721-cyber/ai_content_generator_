from flask import Flask, request, jsonify
from flask_cors import CORS
import openai, os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": "gpt-3.5-turbo"}), 200

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Write a creative short article about {prompt}"}],
            max_tokens=250,
            temperature=0.8,
        )

        output = completion.choices[0].message.content.strip()
        return jsonify({"output": output}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend running successfully!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
