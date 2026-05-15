from flask import Flask, request, jsonify
import joblib
import re
import nltk 
from nltk.corpus import stopwords

app = Flask(__name__)
model = joblib.load('lexigrade_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('indonesian'))

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words]
    return ' '.join(tokens)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Tidak ada teks'}), 400
    raw = data['text']
    clean = preprocess(raw)
    vec = vectorizer.transform([clean])
    pred = model.predict(vec)[0]
    proba = model.predict_proba(vec).max()
    return jsonify({'level': pred, 'confidence': round(proba, 3)})

if __name__ == "__main__":
    app.run(debug=True, port=5001)