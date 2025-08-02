import os
from flask import Flask, request, jsonify, send_from_directory, render_template
from textblob import TextBlob
from dotenv import load_dotenv
import logging
from datetime import datetime

app = Flask(__name__)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Home route to serve the HTML form
@app.route('/')
def home():
    return render_template('form.html')

# Keyword extraction route for JavaScript fetch request
@app.route('/api/v1/keywords', methods=['POST'])
def extract_keywords():
    timestamp = datetime.now().isoformat()
    route = "/api/v1/keywords"

    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            logging.warning(f"{timestamp} - {route} - Missing text field")
            return jsonify({'error': 'Missing text field'}), 400

        blob = TextBlob(text)
        keywords = list(set(blob.noun_phrases))

        logging.info(f"{timestamp} - {route} - Success")
        return jsonify({'keywords': keywords}), 200

    except Exception as e:
        logging.error(f"{timestamp} - {route} - ERROR: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Optional favicon route
@app.route('/favicon.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
