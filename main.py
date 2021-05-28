from word_embedding import WordEmbedding
from utils import helper, preprocess

import pandas as pd
import numpy as np
import json

"""
Yet to do:
    expand context
    using pretrained glove
"""

if __name__ == '__main__':

    data = pd.read_csv("./data/training.1600000.processed.noemoticon.csv", nrows=1000)
    text = list(data.iloc[:,5])
    label = list(data.iloc[:,0])


    #Keras Neural net features
    embeddings = WordEmbedding(preprocess.tokenizer, vocab_size=13000, maxlen=150, embedding_vector=10, method="keras")
    text = embeddings.tokenize(text)
    text, unique_words, word_dict = embeddings.encode(text)
    text, label = np.array(text), np.array(label)
    model = embeddings.train_keras(text, label, epochs=50)

    word_embeddings = model.get_layer("embedding").get_weights()[0]

    embeddings = helper.get_embeddings(unique_words, word_dict, word_embeddings)
    helper.plot(word_dict, embeddings) 
    helper.save_embeddings(embeddings)



    # Word2vec
    # embeddings = WordEmbedding(preprocess.tokenizer, vocab_size=13000, maxlen=150, embedding_vector=10, method="word2vec")
    # text = embeddings.tokenize(text)
    # words, label, unique_words, word_dict = embeddings.encode_w2v(text)
    # model = embeddings.train_w2v(words, label, epochs=50)

    # word_embeddings = model.get_weights()[0]

    # embeddings = helper.get_embeddings(unique_words, word_dict, word_embeddings)
    # helper.plot(word_dict, embeddings)
    # helper.save_embeddings(embeddings) 
