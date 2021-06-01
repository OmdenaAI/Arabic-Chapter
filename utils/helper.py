import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
from scipy import sparse
import json

from tensorflow.keras.layers import *
from tensorflow.keras.models import *


def word_dictionary(text):
    text = set(list(text))
    
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


def pretrained_data(vocab_size):
    embeddings = dict()
    word_vocab = set()
    f = open('utils/glove.6B.50d.txt', 'r')

    for lines in f:
        line = lines.strip().split()
        word = line[0]
        coefs = np.asarray(line[1:], dtype='float32')
        word_vocab.add(word)
        embeddings[word] = coefs
    f.close()

    embedding_matrix = np.zeros((vocab_size+1, 300))
    i=0
    for word in word_vocab:
        embedding_matrix[i] = embeddings[word]
        i+=1
    return embeddings, embedding_matrix

def w2v(texts):
    window = 2
    word_lists = []
    all_text = []

    for text in texts:
        all_text += text 

        for i, word in enumerate(text):
            for w in range(window):
                if i + 1 + w < len(text): 
                    word_lists.append([word] + [text[(i + 1 + w)]]) 
                if i - w - 1 >= 0:
                    word_lists.append([word] + [text[(i - w - 1)]])

    return word_lists, all_text

def encode_w2v(word_lists, word_dict):
    X = []
    Y = []
    l = len(word_dict)+1

    for i, word_list in tqdm(enumerate(word_lists), total=len(word_lists)):
        # print(i, word_list)

        main_word_index = word_dict.get(word_list[0])
        context_word_index = word_dict.get(word_list[1])
        # print(main_word_index, context_word_index)

        X_row = np.zeros(l)
        Y_row = np.zeros(l)
        # print(X_row, Y_row)

        X_row[main_word_index] = 1
        Y_row[context_word_index] = 1
        # print(X_row, Y_row)

        X.append(X_row)
        Y.append(Y_row)
        # print(X, Y)
    X = sparse.csr_matrix(X)
    Y = sparse.csr_matrix(Y)
    return X, Y



def get_model(X, y, vocab_size, embedding_size, maxlen, method="keras"):
    if method == "keras":
        model = Sequential()
        model.add(Embedding(vocab_size, embedding_size, input_length=maxlen ,name="embedding"))
        #model.add(LSTM(128,return_sequences=True,dropout=0.2))
        #model.add(GlobalMaxPooling1D())
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))
    
    elif method == "word2vec":
        inp = Input(shape=(X.shape[1],))
        x = Dense(units=embedding_size, activation='relu')(inp)
        x = Dense(units=y.shape[1], activation='softmax')(x)
        model = Model(inputs=inp, outputs=x)
    

    return model

def convert(dictionary):
    for i in dictionary:
        dictionary[i] = str(dictionary[i])
    return dictionary

def get_embeddings(unique_words, word_dict, word_embeddings):
    embeddings = {}
    for word in unique_words: 
        embeddings.update({
            word: word_embeddings[word_dict.get(word)]
            })
    return embeddings

def plot(word_dict, embeddings):
    plt.figure(figsize=(10, 10))
    for word in list(word_dict.keys()):
        coord = embeddings.get(word)
        plt.scatter(coord[0], coord[1])
        plt.annotate(word, (coord[0], coord[1]))
    plt.show()

def save_embeddings(embeddings):
    embeddings = convert(embeddings)
    emb = open("models/embeddings.json", mode='w')
    json.dump(convert(embeddings), emb, sort_keys=True)
    emb.close()