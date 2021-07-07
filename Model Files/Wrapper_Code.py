import gensim
import json
import os
import numpy as np
import pickle
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import *
from keras.optimizers import Adam,SGD
from keras.models import Model
import re

class Pos_Tagger:
    def __init__(self):
        self.word_tokenizer ,self.tag_tokenizer = self.__get_tokenizers()
        self.VOCABULARY_SIZE = len(self.word_tokenizer.word_index) + 1                  
        self.NUM_CLASSES = 35
        self.__embedding_dim = 300
        self.__MAX_SEQUENCE_LENGTH = 398
        self.__trunc_type='post'
        self.__padding_type='post'
        self.__oov_tok = "<OOV>"
        self.__model = self.__define_model()

    def __get_tokenizers(self):

        with open('word_tokenizer.pickle', 'rb') as handle:
            word_tokenizer = pickle.load(handle)
        with open('tag_tokenizer.pickle', 'rb') as handle:
            tag_tokenizer = pickle.load(handle)

        return word_tokenizer , tag_tokenizer


    def __define_model(self):
        
        model = Sequential()
        model.add(InputLayer((self.__MAX_SEQUENCE_LENGTH)))
        model.add(Embedding(input_dim = self.VOCABULARY_SIZE,
                                    output_dim    = self.__embedding_dim,
                                    input_length  = self.__MAX_SEQUENCE_LENGTH,
                                    trainable     = True
        ))
        model.add(Bidirectional(LSTM(256, return_sequences=True)))
        model.add(Bidirectional(LSTM(256, return_sequences=True)))
        model.add(Bidirectional(LSTM(256, return_sequences=True)))
        model.add(Bidirectional(LSTM(256, return_sequences=True)))
        model.add(TimeDistributed(Dense(self.NUM_CLASSES, activation='softmax')))

        model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
        model.load_weights('Bi_LSTM_checkpoint.h5')

        return model


    def clean_str(self, text):
        
        #remove tashkeel
        p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
        text = re.sub(p_tashkeel,"", text)
        
        #remove longation
        p_longation = re.compile(r'(.)\1+')
        subst = r"\1\1"
        text = re.sub(p_longation, subst, text)
        
        text = text.replace('وو', 'و')
        text = text.replace('يي', 'ي')
        text = text.replace('اا', 'ا')
        text = text.replace('أ', 'ا')
        text = text.replace('إ', 'ا')
        text = text.replace('آ', 'ا')
        text = text.replace('ى', 'ي')

        return text.split()


    def classify(self, sentence):

        sentence = self.clean_str(sentence)
        seq = [self.word_tokenizer.texts_to_sequences(sentence)]
        pad_seq = pad_sequences(seq, maxlen=self.__MAX_SEQUENCE_LENGTH, padding=self.__padding_type, truncating=self.__trunc_type)
        pad_seq = np.squeeze(pad_seq,axis=-1)
        pred = np.squeeze(self.__model.predict(pad_seq).argmax(-1))
        output = [self.tag_tokenizer.index_word[tag] for tag in pred if tag != 0]
        return output
