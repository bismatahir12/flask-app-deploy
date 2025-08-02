import os
from flask import Flask, request, render_template, send_from_directory
from textblob import TextBlob
from dotenv import load_dotenv
import logging
from datetime import datetime

app = Flask(__name__)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/extract', methods=['POST'])
def extract_keywords():
    timestamp = datetime.now().isoformat()
    text = request.form.get('text', '')

    if not text:
        logging.warning(f"{timestamp} - /extract - Missing text field")
        return render_template('form.html', error="Please enter some text.")

    try:
        blob = TextBlob(text)
        keywords = list(set(blob.noun_phrases))

        logging.info(f"{timestamp} - /extract - Success")
        return render_template('form.html', keywords=keywords)

    except Exception as e:
        logging.error(f"{timestamp} - /extract - ERROR: {str(e)}")
        return render_template('form.html', error="Something went wrong!")

@app.route('/favicon.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
