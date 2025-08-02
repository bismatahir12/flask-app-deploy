from flask import Flask, request, jsonify, render_template, send_from_directory
from textblob import TextBlob
from dotenv import load_dotenv
import logging, os
from datetime import datetime

app = Flask(__name__)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/favicon.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/png')

@app.route("/", methods=["GET", "POST"])
def home():
    keywords = None
    if request.method == "POST":
        text = request.form.get("text", "")
        if text:
            blob = TextBlob(text)
            keywords = list(set(blob.noun_phrases))
    return render_template("form.html", keywords=keywords)

@app.route('/api/v1/keywords', methods=['POST'])
def extract_keywords():
    timestamp = datetime.now().isoformat()
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            return jsonify({'error': 'Missing text field'}), 400

        blob = TextBlob(text)
        keywords = list(set(blob.noun_phrases))
        return jsonify({'keywords': keywords}), 200
    except Exception as e:
        logging.error(f"{timestamp} - ERROR: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
