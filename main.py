from word_embedding import WordEmbedding

from utils import helper, preprocess

import numpy as np

"""
Yet to do:
    Save embeddings
    Plotting
    dataset without labels, only huge text
    using pretrained word2vec, glove
"""

if __name__ == '__main__':

    text = ["Hello, king! How are your soldiers.",
            "Queen is alright!",
            "Your kingdom is gonna fall",
            "The King is no more."]
    label = [1, 1, 0, 0]

    embeddings = WordEmbedding(preprocess.tokenization, vocab_size=30, maxlen=10, embedding_vector=5, method="keras")

    text = embeddings.tokenize(text)
    print(text)

    text = embeddings.encode(text)
    print(text)

    text, label = np.array(text), np.array(label)

    model = embeddings.train(text, label, epochs=5)

    word_embeddings = model.get_layer("embedding").get_weights()[0]

    print(word_embeddings[12])

    

