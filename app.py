from flask import Flask, render_template, request, jsonify
import re
from POS import POS
from NER import NER_Tagger
from Lemma import lemma

pos_tagger = POS('SVM')
ner_tagger = NER_Tagger()

app  = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/join1',methods=['GET','POST'])
def lemmatization():
    wordlist  = []
    text = request.form['text1']
    for word in text.split():
            temp = lemma(word.strip())
            if len(temp) < 3:
                    wordlist.append(word)
            else:
                    wordlist.append(temp)
    result = {'output':' '.join(wordlist)}
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

@app.route('/join2',methods=['GET','POST'])               
def pos():
    text = request.form['text1']
    output = pos_tagger.predict(text)
    result = {'output':output}
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

@app.route('/join',methods=['GET','POST'])               
def ner():
    text = request.form['text1']
    output = ner_tagger.classify(text)
    result = {'output':output}
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)
    


if __name__ == '__main__':
    app.run(debug=True)
