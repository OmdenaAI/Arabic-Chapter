##Based on: https://github.com/erwtokritos/keras-glove

import numpy as np
from tensorflow.keras.layers import Input, Embedding, Dot, Reshape, Add
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.backend as K
from collections import defaultdict





class Glove:


    def __init__(self):

        return


    def glove_model(self, vocab_size=10, vector_dim=3):

        input_target = Input((1,))
        input_context = Input((1,))

        central_embedding = Embedding(vocab_size, vector_dim, input_length=1 , name="word_embedding")
        central_bias = Embedding(vocab_size, 1, input_length=1)

        context_embedding = Embedding(vocab_size, vector_dim, input_length=1)
        context_bias = Embedding(vocab_size, 1, input_length=1)

        vector_target = central_embedding(input_target)
        vector_context = context_embedding(input_context)

        bias_target = central_bias(input_target)
        bias_context = context_bias(input_context)

        dot_product = Dot(axes=-1)([vector_target, vector_context])
        dot_product = Reshape((1, ))(dot_product)
        bias_target = Reshape((1,))(bias_target)
        bias_context = Reshape((1,))(bias_context)

        prediction = Add()([dot_product, bias_target, bias_context])

        model = Model(inputs=[input_target, input_context], outputs=prediction)
        model.compile(loss=self.custom_loss, optimizer=Adam())

        return model


    def train(self, seqs, num_tokens, vector_size, window, epochs, batch_size):
        """
        Trains GloVe model


        Parameters 

        seqs: list of list of indices of each token in corpus
        num_tokens: total number of unique tokens in corpus
        vector_size: dimension of word vectors to be trained
        

        Returns

        model: trained GloVe model


        """

        cache = defaultdict(lambda: defaultdict(int))

        # get co-occurrences
        self.build_cooccurrences(seqs, cache, window)
        first_indices, second_indices, frequencies = self.cache_to_pairs(cache)

        # build GloVe model & fit
        model = self.glove_model(num_tokens + 1, vector_dim=vector_size)
        model.fit([first_indices, second_indices], frequencies, epochs=epochs, batch_size=batch_size)
        return model


    def bigram_count(self,token_list, window_size, cache):
        sentence_size = len(token_list)

        for central_index, central_word_id in enumerate(token_list):
            for distance in range(1, window_size + 1):
                if central_index + distance < sentence_size:
                    first_id, second_id = sorted([central_word_id, token_list[central_index + distance]])
                    cache[first_id][second_id] += 1.0 / distance


    def build_cooccurrences(self,sequences, cache, window=3):

        for seq in sequences:
            self.bigram_count(seq, window, cache)


    def cache_to_pairs(self, cache):
        first, second, x_ijs = [], [], []

        for first_id in cache.keys():

            for second_id in cache[first_id].keys():

                x_ij = cache[first_id][second_id]

                # add (main, context) pair
                first.append(first_id)
                second.append(second_id)
                x_ijs.append(x_ij)

                # add (context, main) pair
                first.append(second_id)
                second.append(first_id)
                x_ijs.append(x_ij)

        return np.array(first), np.array(second), np.array(x_ijs)

    def custom_loss(self, y_true, y_pred):
        return K.sum(K.pow(K.clip(y_true / 100, 0.0, 1.0), 3/4) * K.square(y_pred - K.log(y_true)), axis=-1)
