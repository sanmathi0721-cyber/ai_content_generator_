from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ AI Content Generator Backend (Hugging Face) is running!"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # 🧠 Use Hugging Face's free inference model
        API_URL = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Authorization": "Bearer hf_NFcvHnWxaeqPGGzQhxZfSbEJbKDzFqjR"}  # public free demo token

        payload = {"inputs": f"Write a detailed and creative article about {prompt}. Include examples and a conclusion."}

        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                content = result[0]["generated_text"]
                return jsonify({"output": content}), 200
            else:
                return jsonify({"output": "⚠️ Model returned unexpected format, please retry."}), 200
        else:
            print("❌ Hugging Face API Error:", response.text)
            return jsonify({"output": "⚠️ Unable to generate content right now. Please try again."}), 200

    except Exception as e:
        print("❌ Backend Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
