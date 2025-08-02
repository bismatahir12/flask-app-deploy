import os
from flask import Flask, request, jsonify, send_from_directory, render_template
from dotenv import load_dotenv
import logging
from datetime import datetime
import yake  # New: Lightweight keyword extractor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/')
def home():
    return render_template('form.html')

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

        # Using YAKE to extract keywords
        extractor = yake.KeywordExtractor(lan="en", n=1, top=10)
        keywords = extractor.extract_keywords(text)
        keyword_list = [kw for kw, score in keywords]

        logging.info(f"{timestamp} - {route} - Success")
        return jsonify({'keywords': keyword_list}), 200

    except Exception as e:
        logging.error(f"{timestamp} - {route} - ERROR: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/favicon.png')
def favicon():
    return send_from_directory(
        os.path.join(BASE_DIR, 'static'),
        'favicon.png',
        mimetype='image/png'
    )

if __name__ == '__main__':
    app.run(debug=True)
