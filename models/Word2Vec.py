import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

from sklearn import preprocessing, model_selection
from scipy import sparse

import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import *
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences 

from utils import helper


class Word2Vec:
    def __init__(self, tokenizer, vocab_size=10000, maxlen=256, embedding_vector=5, method="keras"):
        self.method = method
        self.tokenizer = tokenizer
        self.vocab_size = vocab_size
        self.maxlen = maxlen
        self.embedding_vector = embedding_vector

    def tokenize(self, text, punctuations=[], stop_words=[]):
        tokens, maxlen, vocab = self.tokenizer(text, punctuations, stop_words)
        if self.maxlen == 'auto':
            self.maxlen = maxlen
        if self.vocab_size == 'auto':
            self.vocab_size = vocab
        # print(vocab, maxlen)
        return tokens

    def encode(self, text, label):
        vector, temp, all_ = [], [], []
        for d in tqdm(text, total=len(text)):
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

        model = helper.get_model(text, label, self.vocab_size, self.embedding_vector, self.maxlen, self.method)
        model.compile(optimizer="SGD", loss=tf.keras.losses.CategoricalCrossentropy(), metrics=["accuracy"])
        # print(model.summary())

        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1,patience=4)  
        mc = ModelCheckpoint('models/word_embeddings_NN.h5', monitor='val_loss', mode='min', save_best_only=True,verbose=1)

        model.fit(text, label, validation_split=validation_split, epochs=epochs, callbacks=[es, mc], verbose=1)

        return model

    def encode_w2v(self, texts, window_size=2):
        word_lists, all_text = helper.w2v2(texts, window_size=window_size)
        word_dict = helper.word_dictionary(all_text)
        X, Y = helper.encode_w2v2(word_lists, word_dict)
        return X, Y, list(word_dict.keys()), word_dict

    def train_w2v(self, words, label, epochs=5, validation_split=0.2):

        model = helper.get_model(words, label, self.vocab_size, self.embedding_vector, self.maxlen, method=self.method)
        model.compile(optimizer="SGD", loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=["accuracy"])
        # print(model.summary())

        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1,patience=4)  
        mc = ModelCheckpoint('models/word_embeddings_w2v.h5', monitor='val_loss', mode='min', save_best_only=True,verbose=1)

        # model.fit(trainX.toarray(), trainY.toarray(), validation_data=(validX.toarray(), validY.toarray()), epochs=epochs, callbacks=[es, mc], verbose=1)
        model.fit(words, label, validation_split=validation_split, epochs=epochs, callbacks=[es, mc], verbose=1)

        return model

