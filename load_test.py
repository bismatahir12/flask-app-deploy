
import os
from flask import Flask, request, jsonify
from textblob import TextBlob
from dotenv import load_dotenv
import logging
from datetime import datetime


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

if __name__ == '__main__':
    app.run(debug=True)

