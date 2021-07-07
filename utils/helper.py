import pickle
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper
from sklearn.manifold import TSNE
import random


def get_embedding_matrix(model, index_word=None, vector_file=False, layer_name="word_embedding"):
    """
    Returns a dictionary of words and their vectors

    Parameters

    model: gensim or Keras model
    index_word: dictionary of indices and corresponding words
                passed only with Keras models
    vector_file: True when loading with KeyedVectors.load (vector-only file)
                 False when loading using Word2Vec.load (full model)

    layer_name: name of embedding layer to be extracted
                passed only with Keras models
    """
    embeddings_index = {}
    if index_word == None:
        if vector_file:
            words_vectors = zip(model.index_to_key,model.vectors)
        else:
            words_vectors = zip(model.wv.index_to_key,model.wv.vectors)
        for word,vector in words_vectors:
            coefs = np.asarray(vector, dtype='float32')
            embeddings_index[word] = coefs
    else:
        embeds = model.get_layer(layer_name).get_weights()[0]
        for idx in range(list(index_word.keys())[-1]):
            embeddings_index[index_word[idx]] = embeds[idx]
    return embeddings_index

def load_embedding_matrix(vocabulary_size, embedding_dim, word_index, embeddings_index):
    """
    Returns a dictionary of indices and word vectors
    of words that are available in the model 
    if a word vector is not available a random vector is used

    Parameters

    vocabulary_size: number of unique tokens in training set
    embedding_dim: dimension of word vectors
    word_index: dictionary of words and their indices
    embeddings_index: dictionary of words and their vectors
    """
    embeddings_matrix = np.zeros((vocabulary_size, embedding_dim))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embeddings_matrix[i] = embedding_vector
        else:
            embeddings_matrix[i] = np.random.uniform(size=(1, embedding_dim))

    return embeddings_matrix


def encode_tokens(tokens):
    """
    Encodes list of list of tokens into list of list of token indices

    Parameters:

    tokens: list of list of tokens

    Returns

    sentence_inds: list of list of token indices
    vocab: numpy array of unique tokens
    num_tokens: number of unique tokens
    word_index: dictionary of words and their indices 
    index_word: dictionary of indices and their corresponding words
    """
    vocab = np.unique(np.array([y for x in tokens for y in x]))
    num_tokens = vocab.shape[0]
    word_index = {w: i for i, w in enumerate(vocab)}
    index_word = {i: w for i, w in enumerate(vocab)}

    sentence_inds = []
    for s in tokens:
        si = []
        for t in s:
            si.append(word_index[t])
        sentence_inds.append(si)
    return sentence_inds, vocab, num_tokens, word_index, index_word


def plot(embeddings_index, name, n=100, seed=0):
    """
    Plots a random subset of length n of the embeddings

    Parameters

    embeddings_index: dictionary of words and their vectors
    name: name of image to be saved
    n: number of words to include in the plots
    seed: random seed of subset of words
    """
    random.seed(seed)
    labels = list(embeddings_index.keys())
    tokens = list(embeddings_index.values())
    labels, tokens = zip(*random.sample(list(zip(labels, tokens)), n))

    
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=0)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
        
    plt.figure(figsize=(16, 16)) 
    for i in range(len(x)):
        label = arabic_reshaper.reshape(labels[i])
        label = get_display(label)

        plt.scatter(x[i],y[i])
        plt.annotate(label,
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.savefig(f"{name}.png")

def save_embeddings(embeddings_index, filename):
    """
    Saves embeddings_index as a pickle file
    """
    embedding_file = open(filename, 'wb')
    pickle.dump(embeddings_index, embedding_file)                     
    embedding_file.close()

def load_embeddings(filename):
    """
    Loads embeddings_index from pickle file
    """
    embedding_file = open(filename, 'rb')     
    embeddings_index = pickle.load(embedding_file)
    embedding_file.close()
    return embeddings_index
