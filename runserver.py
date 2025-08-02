<<<<<<< HEAD
from flask import Flask, request, jsonify, render_template, send_from_directory
=======
import os
from flask import Flask, request, jsonify, send_from_directory, render_template
>>>>>>> 39286e2032da05d94885887453687711467e4085
from textblob import TextBlob
from dotenv import load_dotenv
import logging, os
from datetime import datetime

# Initialize Flask app with correct templates directory
app = Flask(__name__, template_folder="templates", static_folder="static")

# Optional: for debug - shows template path
print("Templates folder path:", app.template_folder)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

<<<<<<< HEAD
=======
# Logging setup
>>>>>>> 39286e2032da05d94885887453687711467e4085
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

<<<<<<< HEAD
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
=======
@app.route('/')
def home():
    return render_template('form.html')
>>>>>>> 39286e2032da05d94885887453687711467e4085

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

@app.route('/favicon.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
