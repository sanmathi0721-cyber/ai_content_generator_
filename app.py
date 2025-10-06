from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Optional: only import openai if key exists
try:
    import openai
except ImportError:
    openai = None

app = Flask(__name__)
CORS(app)

# Load OpenAI API key
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if openai and OPENAI_KEY:
    openai.api_key = OPENAI_KEY


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ AI Content Generator Backend is running!"}), 200


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

        # ✅ If OpenAI API key is valid, use it
        if openai and OPENAI_KEY:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"Write a creative paragraph about {prompt}"}
                    ],
                    max_tokens=200,
                    temperature=0.8,
                )
                output = response["choices"][0]["message"]["content"].strip()
                return jsonify({"output": output}), 200

            except Exception as e:
                print("⚠️ OpenAI error:", e)

        # 🔄 Offline fallback mode (if no key or quota issue)
        fake_output = f"Here’s a creative sample text about **{prompt}**.\n\n{prompt.capitalize()} is an interesting topic that inspires imagination, creativity, and innovation. This text is auto-generated locally for demo purposes."
        return jsonify({"output": fake_output}), 200

    except Exception as e:
        print("❌ Backend error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
