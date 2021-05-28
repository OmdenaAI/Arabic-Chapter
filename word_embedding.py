import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy import sparse

import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import *
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
        tokens, maxlen = self.tokenizer(text)
        return tokens

    def encode(self, text):
        vector, temp, all_ = [], [], []
        for d in text:
            for i in d:
                temp.extend(one_hot(i, self.vocab_size))
            vector.append(temp)
            temp=[]
        vector = pad_sequences(vector, maxlen=self.maxlen, padding="post")
        for x in text:
            all_.extend(x)
        word_dict = helper.word_dictionary(all_)
        return vector, list(word_dict.keys()), word_dict

    def train_keras(self, text, label, epochs=5):
        #text = self.encode(text)

        model = helper.get_model(text, label, self.vocab_size, self.embedding_vector, self.maxlen)
        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        print(model.summary())

        es = EarlyStopping(monitor='loss', mode='min', verbose=1,patience=3)  
        mc = ModelCheckpoint('models/word_embeddings.h5', monitor='loss', mode='min', save_best_only=True,verbose=1)

        model.fit(text, label, epochs=epochs, callbacks=[es, mc], verbose=1)

        return model

    def encode_w2v(self, texts):
        word_lists, all_text = helper.w2v(texts)
        word_dict = helper.word_dictionary(all_text)
        X, Y = helper.encode_w2v(word_lists, word_dict)
        #print(X, Y)
        return X, Y, list(word_dict.keys()), word_dict

    def train_w2v(self, words, label, epochs=5):
        model = helper.get_model(words, label, self.vocab_size, self.embedding_vector, self.maxlen, method=self.method)
        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        print(model.summary())

        es = EarlyStopping(monitor='loss', mode='min', verbose=1,patience=3)  
        mc = ModelCheckpoint('models/word_embeddings.h5', monitor='loss', mode='min', save_best_only=True,verbose=1)

        model.fit(words.toarray(), label.toarray(), epochs=epochs, callbacks=[es, mc], verbose=1)

        return model

