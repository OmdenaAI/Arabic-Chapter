import zipfile

import os
import gensim
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from flask_ngrok import run_with_ngrok
from pyarabic import araby
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

from evaluator import evaluator
from pretrained.AraVec import AraVec
from utils import helper
from utils.tokenizer import tokenization

np.random.seed(0)

app = Flask(__name__)
run_with_ngrok(app)

def normalize(text):
    text = araby.strip_harakat(text)
    text = araby.strip_tashkeel(text)
    text = araby.strip_small(text)
    text = araby.strip_tatweel(text)
    text = araby.strip_shadda(text)
    text = araby.strip_diacritics(text)
    text = araby.normalize_ligature(text)
    text = araby.normalize_teh(text)
    text = araby.normalize_alef(text)
    return text

def strip_all(text):
    l = [' ', '0', '1', '2', '3', '4', '5', '6',
       '7', '8', '9', '?', '.', '.'
       '؟', 'ء', 'ؤ', 'ئ', 'ا', 'ب', 'ت', 'ث',
       'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ',
       'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي', '٠', '١',
       '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']
    return "".join([x for x in text if x in l])
def preprocess(text):
    text = normalize(text)
    text = strip_all(text)
    return text

def get_tokens(text):
    return tokenization(text).tokens[0]


def get_preprocessed(text):
    text = preprocess(text)
    tokens = get_tokens(text)
    print(tokens)
    return tokens

def get_model(name):
    if name == "aravec":
        aravec = AraVec()
        model_path = aravec.get_model("Twitter_SkipGram_100", unzip=True)
        model = aravec.load_model(model_path)
        return model

def get_embeddings(tokens, model):
    embeddings = dict()
    embeddings_index = helper.get_embedding_matrix(model)
    for token in tokens:
        embeddings[token] = embeddings_index[token].tolist()
    return embeddings

def get_similar(tokens, model):
    similar = dict()
    for token in tokens:
        similar[token] = model.wv.most_similar(token, topn=5)
    return similar
    

@app.route("/", methods=['GET'])
def root():
    return jsonify({
        'note' : "use /aravec/embedding?text=" " or  /wor2vec/embedding?text=" " to get embeddings for each token",
        'similar words' : "to get similar words use /aravec/similar/"
    })

@app.route("/aravec/embedding", methods=['GET'])
def predict_aravec():
    text = request.args.get('text')
    text = get_preprocessed(text)
    model = get_model("aravec")
    return get_embeddings(text, model)

@app.route("/aravec/similar", methods=['GET'])
def predict_aravec_similar():
    text = request.args.get('text')
    text = get_preprocessed(text)
    model = get_model("aravec")
    return get_similar(text, model)



if __name__ == '__main__':
    app.run()