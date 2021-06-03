import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn import preprocessing, model_selection
from scipy import sparse

import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import *
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences 

from utils import helper


class WordEmbedding:
    def __init__(self, tokenizer, vocab_size=10000, maxlen=256, embedding_vector=5, method="keras"):
        self.method = method
        self.tokenizer = tokenizer
        self.vocab_size = vocab_size
        self.maxlen = maxlen
        self.embedding_vector = embedding_vector

    def tokenize(self, text, stop_words=['and', 'a', 'is', 'the', 'in', 'be', 'will']):
        tokens, maxlen = self.tokenizer(text, stop_words)
        return tokens

    def encode(self, text, label):
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
        onehot_encoder = preprocessing.OneHotEncoder(sparse=False)
        label = np.array(label).reshape(len(label), 1)
        label = onehot_encoder.fit_transform(label)
        return vector, label, list(word_dict.keys()), word_dict

    def train_keras(self, text, label, epochs=5, validation_split=0.2):
        trainX, validX, trainY, validY = model_selection.train_test_split(text, label, test_size=validation_split, random_state=42, shuffle=True)

        model = helper.get_model(trainX, trainY, self.vocab_size, self.embedding_vector, self.maxlen)
        model.compile(optimizer="adam", loss=tf.keras.losses.CategoricalCrossentropy(), metrics=["accuracy"])
        print(model.summary())

        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1,patience=3)  
        mc = ModelCheckpoint('models/word_embeddings_NN.h5', monitor='val_loss', mode='min', save_best_only=True,verbose=1)

        model.fit(trainX, trainY, validation_data=(validX, validY), epochs=epochs, callbacks=[es, mc], verbose=1)

        return model

    def encode_w2v(self, texts):
        word_lists, all_text = helper.w2v(texts)
        word_dict = helper.word_dictionary(all_text)
        X, Y = helper.encode_w2v(word_lists, word_dict)
        #print(X, Y)
        return X, Y, list(word_dict.keys()), word_dict

    def train_w2v(self, words, label, epochs=5, validation_split=0.2):
        trainX, validX, trainY, validY = model_selection.train_test_split(words, label, test_size=validation_split, random_state=42, shuffle=True)

        model = helper.get_model(trainX, trainY, self.vocab_size, self.embedding_vector, self.maxlen, method=self.method)
        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        print(model.summary())

        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1,patience=3)  
        mc = ModelCheckpoint('models/word_embeddings_w2v.h5', monitor='val_loss', mode='min', save_best_only=True,verbose=1)

        model.fit(trainX.toarray(), trainY.toarray(), validation_data=(validX.toarray(), validY.toarray()), epochs=epochs, callbacks=[es, mc], verbose=1)

        return model

