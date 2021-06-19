import os
import tensorflow as tf
from models.Word2Vec import Word2Vec

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import json

import numpy as np
import pandas as pd

from utils import helper, preprocess
from utils.config import config

"""
Yet to do:
    expand context
    using pretrained glove
"""

if __name__ == '__main__':

    train_pos = pd.read_csv("data/train_Arabic_tweets_positive_20190413.tsv", sep='\t', names=["label", "tweet"])
    train_neg = pd.read_csv("data/train_Arabic_tweets_negative_20190413.tsv", sep='\t', names=["label", "tweet"])
    test_pos = pd.read_csv("data/test_Arabic_tweets_positive_20190413.tsv", sep='\t', names=["label", "tweet"])
    test_neg = pd.read_csv("data/test_Arabic_tweets_negative_20190413.tsv", sep='\t', names=["label", "tweet"])
    train = pd.concat([train_pos, train_neg])#.sample(frac=1, random_state=0)
    test = pd.concat([test_pos, test_neg])

    # text = list(train.tweet)
    # label = list(train.label)

    # #Keras Neural net features
    # embeddings = Word2Vec(preprocess.tokenizer, vocab_size=config['vocab_size'], maxlen=config['maxlen'], embedding_vector=config['embedding_vector'], method=config['method'])
    # text = embeddings.tokenize(text, stop_words=config['stop_words'], punctuations=config['punctuations'])
    # text, label, unique_words, word_dict = embeddings.encode(text, label)
    # text, label = np.array(text), np.array(label)

    # model = embeddings.train_keras(text, label, epochs=config['epochs'], validation_split=config['test_size'])

    # word_embeddings = model.get_layer("embedding").get_weights()[0]

    # embeddings = helper.get_embeddings(unique_words, word_dict, word_embeddings, config['vocab_size'])
    # helper.plot(word_dict, embeddings, "embeddings_NN") 
    # helper.save_embeddings(embeddings, "embeddings_NN")


    text = list(train.tweet)

    # Word2vec
    embeddings = Word2Vec(preprocess.tokenizer, vocab_size=config['vocab_size'], maxlen=config['maxlen'], embedding_vector=config['embedding_vector'], method=config['method'])
    text = embeddings.tokenize(text, stop_words=config['stop_words'], punctuations=config['punctuations'])

    words, label, unique_words, word_dict = embeddings.encode_w2v(text, window_size=config['window_size'])
    words, label = np.array(words), np.array(label)

    model = embeddings.train_w2v(words, label, epochs=config['epochs'], validation_split=config['test_size'])

    word_embeddings = model.get_layer("embedding").get_weights()[0]

    embeddings = helper.get_embeddings(unique_words, word_dict, word_embeddings, len(unique_words))
    helper.plot(word_dict, embeddings, "embeddings_w2v")
    helper.save_embeddings(embeddings, "embeddings_w2v") 
