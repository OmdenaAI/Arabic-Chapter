import zipfile

import gdown
import os
import gensim
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from pyarabic import araby
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

from evaluator import evaluator
from pretrained.AraVec import AraVec
from utils import helper
from utils.tokenizer import tokenization, clean_str

np.random.seed(0)

app = Flask(__name__)

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

def get_preprocessed_word2vec(text):
    text = preprocess(text)
    tokens = get_tokens(text)
    return tokens

def get_preprocessed_aravec(text):
    tokens = [clean_str(x) for x in text.strip().split()]
    return tokens

def get_model(name):
    if name == "aravec":
        aravec = AraVec()
        model_path = aravec.get_model("Twitter_CBOW_100", unzip=True)
        model = aravec.load_model(model_path)
        return model
    elif name == "word2vec":
        if not os.path.exists("models/mottagah.zip"):
            url = "https://drive.google.com/uc?id=11nmKLbIC1VMquO_FjLy9t6wxt1AyQFO3"
            output = "models/mottagah.zip"
            gdown.download(url, output, quiet=False)
            print("Model Downloaded")
            with zipfile.ZipFile("models/mottagah.zip", 'r') as zipf:
                zipf.extractall("models/")
            model = gensim.models.Word2Vec.load("models/mottagah/mottagah")
            print("Model Unzipped ")

        elif not os.path.exists("models/mottagah/"):
            with zipfile.ZipFile("models/mottagah.zip", 'r') as zipf:
                zipf.extractall("models/")
            model = gensim.models.Word2Vec.load("models/mottagah/mottagah")
            print("Model Unzipped ")

        else:
            model = gensim.models.Word2Vec.load("models/mottagah/mottagah")
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
        'embeddings' : "use /aravec/embedding?text=" " to get embeddings for each token",
        'similar words' : "to get similar words use /aravec/similar/"
    })

@app.route("/aravec/embedding", methods=['POST'])
def predict_aravec():
    text = request.args.get('text')
    text = get_preprocessed_aravec(text)
    model = get_model("aravec")
    return get_embeddings(text, model)

@app.route("/aravec/similar", methods=['POST'])
def predict_aravec_similar():
    text = request.args.get('text')
    text = get_preprocessed_aravec(text)
    model = get_model("aravec")
    return get_similar(text, model)

@app.route("/word2vec/embedding", methods=['POST'])
def predict_word2vec():
    text = request.args.get('text')
    text = get_preprocessed_word2vec(text)
    model = get_model("word2vec")
    return get_embeddings(text, model)

@app.route("/word2vec/similar", methods=['POST'])
def predict_word2vec_similar():
    text = request.args.get('text')
    text = get_preprocessed_word2vec(text)
    model = get_model("word2vec")
    return get_similar(text, model)



if __name__ == '__main__':
    app.run()