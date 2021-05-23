import numpy as np
from tensorflow.keras.layers import Dense, Embedding, Flatten
from tensorflow.keras.models import Sequential


def word_dictionary(text):
    word = set(list(text))
    
    dictionary = {}
    for i, word in enumerate(text):
        dictionary[word] = i

    return dictionary


def similarity(text1, text2):
    return np.sqrt(np.sum((text1-text2)**2))

def similar_words(token, embeddings, total=5):
    list_ = embeddings[token]
    similar={}

    for key, value in embeddings.items():
        if key != token:
           similar[key] = similarity(list_, value) 

    return sorted(similar.items(), key=lambda x: x[1])[0:total]



def get_model(vocab_size, embedding_size, maxlen):
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_size, input_length=maxlen ,name="embedding"))
    model.add(Flatten())
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    return model