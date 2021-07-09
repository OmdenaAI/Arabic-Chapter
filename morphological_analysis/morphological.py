import numpy as np
import joblib

from transformers import AutoTokenizer
from arabert.preprocess import ArabertPreprocessor

from utils.gender import GenderAnalyser
from utils.pos import POSAnalyser

class Morphological:
    def __init__(self, text):
        self.text = [text]
        self.tokenizer = AutoTokenizer.from_pretrained("asafaya/bert-base-arabic")
        self.lemmatizer = ArabertPreprocessor(model_name="bert-base-arabertv2")
        self.diacritics = joblib.load("models/diacritics.pkl")
        self.similar = joblib.load("models/similar.pkl")

    def get_tokens(self):
        tokens = [self.tokenizer.tokenize(text) for text in self.text]
        tokens = [" ".join(i).replace(" ##", '+') for i in tokens]
        return tokens

    def get_words(self):
        list_ = ["".join([" "+x+" " if x in """'!"#$%&'()*+,«».؛،/:؟?@[\]^_`{|}~”“""" else x for x in text]) for text in self.text]
        words = [[x for x in text.split()] for text in list_]
        return words

    def get_lemma(self):
        lemma = [[i for x in text.split() for i in self.lemmatizer.preprocess(x).split() if '+' not in i] for text in self.text]
        return lemma

    def get_pos(self):
        pos = POSAnalyser(self.text)
        inputs, mask = pos.tokenize()
        return pos.predict_(inputs, mask)

    def get_gender(self):
        ge = GenderAnalyser(self.text)
        inputs, mask = ge.tokenize()
        return ge.predict_(inputs, mask)

    def get_diacritics(self):
        similar = self.get_similar()
        diacritics = dict()
        for key, val in similar.items():
            if val[0] == "Nan":
                diacritics[key] = val
            else:
                diacritics[key] = [self.diacritics[val[0]]]
        return diacritics

    def get_similar(self):
        similar = dict()
        for val in self.text:
            for i in val.split():
                try:
                    similar[i] = self.similar[i]
                except:
                    similar[i] = ["Nan"]
        return similar