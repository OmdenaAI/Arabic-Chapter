from flask import Flask, jsonify, request

from morphological_analysis.morphological import Morphological

app = Flask(__name__)

@app.route("/", methods=['GET'])
def root():
    return jsonify({
        'Note' : "Arabic Morphological Analyser"
    })

@app.route("/words", methods=['GET', 'POST'])
def predict_words():
    text = request.args.get('text')
    obj = Morphological(text)
    return jsonify({
        'Words':obj.get_words(),
    })

@app.route("/tokens", methods=['GET', 'POST'])
def predict_tokens():
    text = request.args.get('text')
    obj = Morphological(text)
    return jsonify({
        'Tokens':obj.get_tokens(),
    })

@app.route("/Lemmatization", methods=['GET', 'POST'])
def predict_lemma():
    text = request.args.get('text')
    obj = Morphological(text)
    return jsonify({
        'Lemmas':obj.get_lemma(),
    })

@app.route("/gender", methods=['GET', 'POST'])
def predict_gender():
    text = request.args.get('text')
    obj = Morphological(text)
    return obj.get_gender()

@app.route("/pos", methods=['GET', 'POST'])
def predict_pos():
    text = request.args.get('text')
    obj = Morphological(text)
    return obj.get_pos()

@app.route("/similar", methods=['GET', 'POST'])
def predict_similar():
    text = request.args.get("text")
    obj = Morphological(text)
    return obj.get_similar()

@app.route("/diacritics", methods=['GET', 'POST'])
def predict_diacritics():
    text = request.args.get("text")
    obj = Morphological(text)
    return obj.get_diacritics()

if __name__ == '__main__':
    app.run()