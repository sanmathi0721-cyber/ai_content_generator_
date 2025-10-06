from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# Hugging Face free model
generator = pipeline("text-generation", model="gpt2")

@app.route("/")
def home():
    return jsonify({"message": "AI Text Generator is running!"})

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is empty"}), 400

    result = generator(prompt, max_length=100, num_return_sequences=1)
    return jsonify({"result": result[0]['generated_text']})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
