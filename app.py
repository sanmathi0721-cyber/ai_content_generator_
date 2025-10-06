from flask import Flask, request, jsonify
from flask_cors import CORS
import os, requests

# Optional imports
try:
    import openai
except ImportError:
    openai = None

try:
    import cohere
except ImportError:
    cohere = None

app = Flask(__name__)
CORS(app)

# Load API keys
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
COHERE_KEY = os.getenv("COHERE_API_KEY")
HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Initialize clients if available
if openai and OPENAI_KEY:
    openai.api_key = OPENAI_KEY

co = None
if cohere and COHERE_KEY:
    co = cohere.Client(COHERE_KEY)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ Multi-AI Content Generator Backend is running!"}), 200


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

        # 1️⃣ Try OpenAI first
        if openai and OPENAI_KEY:
            try:
                print("🧠 Using OpenAI...")
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"Write a detailed creative article about {prompt}"}],
                    max_tokens=400,
                    temperature=0.8,
                )
                output = response["choices"][0]["message"]["content"].strip()
                return jsonify({"output": output}), 200
            except Exception as e:
                print("⚠️ OpenAI failed:", e)

        # 2️⃣ Then try Cohere
        if co:
            try:
                print("🧠 Using Cohere...")
                resp = co.generate(
                    model="command-xlarge-nightly",
                    prompt=f"Write a creative and professional article about {prompt}",
                    max_tokens=400,
                    temperature=0.8,
                )
                output = resp.generations[0].text.strip()
                return jsonify({"output": output}), 200
            except Exception as e:
                print("⚠️ Cohere failed:", e)

        # 3️⃣ Then try Hugging Face
        if HUGGINGFACE_KEY:
            try:
                print("🧠 Using Hugging Face...")
                headers = {"Authorization": f"Bearer {HUGGINGFACE_KEY}"}
                json_data = {"inputs": f"Write a detailed article about {prompt}"}
                hf_resp = requests.post(
                    "https://api-inference.huggingface.co/models/gpt2",
                    headers=headers,
                    json=json_data,
                    timeout=30
                )
                if hf_resp.status_code == 200:
                    output = hf_resp.json()[0]["generated_text"]
                    return jsonify({"output": output}), 200
                else:
                    print("⚠️ Hugging Face error:", hf_resp.text)
            except Exception as e:
                print("⚠️ Hugging Face failed:", e)

        # 4️⃣ Local fallback (never fails)
        print("💡 Using local fallback text.")
        fake_output = (
            f"Here’s a creative example article about **{prompt}**.\n\n"
            f"{prompt.capitalize()} is an inspiring topic that sparks curiosity, innovation, "
            f"and creativity. This text was generated locally for demonstration purposes."
        )
        return jsonify({"output": fake_output}), 200

    except Exception as e:
        print("❌ Backend Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
