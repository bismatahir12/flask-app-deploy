from flask import Blueprint, render_template, request
from textblob import TextBlob

app = Blueprint('app', __name__)

@app.route('/')
def home():
    return render_template('form.html')


@app.route('/api/v1/keywords', methods=['POST'])
def extract_keywords():
    text = request.form.get('text', '')  # Use form data
    if not text:
        return render_template('form.html', error='Missing text field')

    blob = TextBlob(text)
    keywords = list(set(blob.noun_phrases))

    return render_template('form.html', keywords=keywords, original=text)
