from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from flask_cors import CORS
CORS(app)
import os

app = Flask(__name__)

# ✅ Read OpenAI key from environment (Render will set it)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    topic = data.get('topic')
    content_type = data.get('type')
    tone = data.get('tone')
    word_count = data.get('word_count')

    if not topic:
        return jsonify({'error': 'Please enter a topic.'})

    prompt = f"Write a {tone.lower()} {content_type.lower()} about '{topic}' in around {word_count} words."

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        result = response.output[0].content[0].text
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
