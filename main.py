import os

from word_embedding import WordEmbedding

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import json

import numpy as np
import pandas as pd

from utils import helper, preprocess

"""
Yet to do:
    expand context
    using pretrained glove
"""

if __name__ == '__main__':

    data = pd.read_excel("data/AJGT.xlsx")
    # text = list(data.Feed)
    # label = list(data.Sentiment)


    # #Keras Neural net features
    # embeddings = WordEmbedding(preprocess.tokenizer, vocab_size=10000, maxlen=80, embedding_vector=10, method="keras")
    # text = embeddings.tokenize(text, stop_words=[' ', '0', '1', '2', '3', '4', '5', '6',
    #                                             '7', '8', '9', '?', 
    #                                             '؟', 'ء', 'ؤ', 'ئ', 'ا', 'ب', 'ت', 'ث',
    #                                             'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ',
    #                                             'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي', '٠', '١',
    #                                             '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'])
    # text, label, unique_words, word_dict = embeddings.encode(text, label)
    # text, label = np.array(text), np.array(label)
    # model = embeddings.train_keras(text, label, epochs=50, validation_split=0.2)

    # word_embeddings = model.get_layer("embedding").get_weights()[0]

    # embeddings = helper.get_embeddings(unique_words, word_dict, word_embeddings)
    # helper.plot(word_dict, embeddings, "embeddings_NN") 
    # helper.save_embeddings(embeddings, "embeddings_NN")


    text = list(data.Feed)
    label = list(data.Sentiment)

    # Word2vec
    embeddings = WordEmbedding(preprocess.tokenizer, vocab_size=10000, maxlen=80, embedding_vector=5, method="word2vec")
    text = embeddings.tokenize(text, stop_words=[' ', '0', '1', '2', '3', '4', '5', '6',
                                                '7', '8', '9', '?', 
                                                '؟', 'ء', 'ؤ', 'ئ', 'ا', 'ب', 'ت', 'ث',
                                                'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ',
                                                'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي', '٠', '١',
                                                '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'])
    words, label, unique_words, word_dict = embeddings.encode_w2v(text)
    model = embeddings.train_w2v(words, label, epochs=50, validation_split=0.2)

    word_embeddings = model.get_weights()[0]

    embeddings = helper.get_embeddings(unique_words, word_dict, word_embeddings)
    helper.plot(word_dict, embeddings, "embeddings_w2v")
    helper.save_embeddings(embeddings, "embeddings_w2v") 
