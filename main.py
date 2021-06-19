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

    data = pd.read_csv("data/IMDB Dataset.csv")

    # text = list(data.review)
    # label = list(data.sentiment)

    # #Keras Neural net features
    # embeddings = Word2Vec(preprocess.tokenizer, vocab_size=config['vocab_size'], maxlen=config['maxlen'], embedding_vector=config['embedding_vector'], method=config['method'])
    # text = embeddings.tokenize(text, stop_words=config['stop_words'], punctuations=config['punctuations'])
    # text, label, unique_words, word_dict = embeddings.encode(text, label)
    # text, label = np.array(text), np.array(label)
    # model = embeddings.train_keras(text, label, epochs=config['epochs'], validation_split=config['test_size'])

    # word_embeddings = model.get_layer("embedding").get_weights()[0]

    # embeddings = helper.get_embeddings(unique_words, word_dict, word_embeddings)
    # helper.plot(word_dict, embeddings, "embeddings_NN") 
    # helper.save_embeddings(embeddings, "embeddings_NN")


    text = list(data.review)
    label = list(data.sentiment)
    # print(text[0])
    # print("\n")

    # Word2vec
    embeddings = Word2Vec(preprocess.tokenizer, vocab_size=config['vocab_size'], maxlen=config['maxlen'], embedding_vector=config['embedding_vector'], method=config['method'])
    text = embeddings.tokenize(text, stop_words=config['stop_words'], punctuations=config['punctuations'])
    # print(text[0])
    # print("\n")
    words, label, unique_words, word_dict = embeddings.encode_w2v(text, window_size=config['window_size'])
    # # print(words[0:5], label[0:5])
    model = embeddings.train_w2v(words, label, epochs=config['epochs'], validation_split=0.1)
    model = tf.keras.models.load_model("models/word_embeddings_w2v.h5")
    print(model.predict([[word_dict['king'], word_dict['has']]]))
    print(word_dict["won"])

    word_embeddings = model.get_weights()[0]
    print(np.sum(word_embeddings, axis=0))

    embeddings = helper.get_embeddings(unique_words, word_dict, word_embeddings)
    helper.plot(word_dict, embeddings, "embeddings_w2v")
    helper.save_embeddings(embeddings, "embeddings_w2v") 
