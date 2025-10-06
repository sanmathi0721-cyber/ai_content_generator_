from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Model name (you can use gpt-3.5-turbo or gpt-4o-mini)
MODEL_NAME = "gpt-3.5-turbo"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        title = data.get("title", "Untitled")
        tone = data.get("tone", "professional")
        length = data.get("length", "medium")  # short, medium, long
        mode = data.get("mode", "blog")  # blog, tweet, story, paragraph

        prompt = f"""
        Write a {length} {mode} titled "{title}" in a {tone} tone.
        Include an intro, 2-3 key points, and a conclusion.
        Make it engaging and well-structured.
        """

        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a creative AI content generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85,
            max_tokens=600,
        )

        content = response.choices[0].message["content"].strip()
        return jsonify({"status": "ok", "output": content})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok", "model": MODEL_NAME})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
