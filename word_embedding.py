import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy import sparse
from tensorflow.keras.layers import *
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences 

from utils import helper


class WordEmbedding:
    def __init__(self, tokenizer, vocab_size=30, maxlen=10, embedding_vector=5, method="keras"):
        self.method = method
        self.tokenizer = tokenizer
        self.vocab_size = vocab_size
        self.maxlen = maxlen
        self.embedding_vector = embedding_vector

    def tokenize(self, text):
        tokenizer = self.tokenizer(text)
        return tokenizer.tokens

    def encode(self, text):
        vector, temp = [], []
        #text = helper.word_dictionary(text)
        for d in text:
            for i in d:
                temp.extend(one_hot(i, self.vocab_size))
            vector.append(temp)
            temp=[]

        vector = pad_sequences(vector, maxlen=self.maxlen, padding="post")
        return vector

    def train(self, text, label, epochs=5):
        #text = self.encode(text)

        model = helper.get_model(self.vocab_size, self.embedding_vector, self.maxlen)
        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        print(model.summary())

        model.fit(text, label, epochs=epochs, verbose=1)

        return model