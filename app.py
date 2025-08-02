from flask import Blueprint, render_template, request, jsonify
from textblob import TextBlob

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('form.html')

@views.route('/api/v1/keywords', methods=['POST'])
def extract_keywords():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'Missing text field'}), 400
    blob = TextBlob(text)
    keywords = list(set(blob.noun_phrases))
    return jsonify({'keywords': keywords})