##Based on: https://github.com/ozgurdemir/word2vec-keras

import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, dot, Dense, Flatten
from tensorflow.keras.models import Model
from keras.initializers import RandomNormal
import random
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np



class W2V:


    def __init__(self):

        return


    def w2v_model(self, learn_rate=0.05, vocab_size=10, vector_dim=3):
        stddev = 1.0 / vector_dim
        initializer = RandomNormal(mean=0.0, stddev=stddev, seed=None)

        word_input = Input(shape=(1,), name="word_input")
        word = Embedding(input_dim=vocab_size, output_dim=vector_dim, input_length=1,
                         name="word_embedding", embeddings_initializer=initializer)(word_input)

        context_input = Input(shape=(1,), name="context_input")
        context = Embedding(input_dim=vocab_size, output_dim=vector_dim, input_length=1,
                            name="context_embedding", embeddings_initializer=initializer)(context_input)

        merged = dot([word, context], axes=2, normalize=False, name="dot")
        merged = Flatten()(merged)
        output = Dense(1, activation='sigmoid', name="output")(merged)

        optimizer = tf.keras.optimizers.Adagrad(learn_rate)
        model = Model(inputs=[word_input, context_input], outputs=output)
        model.compile(loss="binary_crossentropy", optimizer=optimizer)
        return model


    def train(self, sequence, window_size, vocab_size, vector_dim, lr, negative_samples, batch_size, epochs, verbose=0):
        """ Trains the word2vec model """

        # in order to balance out more negative samples than positive
        negative_weight = 1.0 / negative_samples
        class_weight = {1: 1.0, 0: negative_weight}

        sequence_length = len(sequence)
        approx_steps_per_epoch = (sequence_length * (
                window_size * 2.0) + sequence_length * negative_samples) / batch_size
        seed = 1
        batch_iterator = self.batch_iterator(sequence, window_size, negative_samples, batch_size, seed)
        model = self.w2v_model(0.05, vocab_size, vector_dim)
        model.fit(batch_iterator,
                                 steps_per_epoch=approx_steps_per_epoch,
                                 epochs=epochs,
                                 verbose=verbose,
                                 class_weight=class_weight,
                                 max_queue_size=100)
        return model


    def skip_gram_iterator(self, sequence, window_size, negative_samples, seed):
        """ An iterator which at each step returns a tuple of (word, context, label) """
        random.seed(seed)
        sequence_length = sequence.shape[0]
        random_float = 0
        epoch = 0
        i = 0
        while True:
            window_start = max(0, i - window_size)
            window_end = min(sequence_length, i + window_size + 1)
            for j in range(window_start, window_end):
                if i != j:
                    yield (sequence[i], sequence[j], 1)

            for negative in range(negative_samples):
                random_float = random.uniform(0, 1)
                j = int(random_float * sequence_length)
                yield (sequence[i], sequence[j], 0)

            i += 1
            if i == sequence_length:
                epoch += 1
            i = 0

    def batch_iterator(self, sequence,  window_size,  negative_samples,  batch_size, seed):
        iterator = self.skip_gram_iterator(sequence, window_size, negative_samples, seed)
        words = np.empty(shape=batch_size)
        contexts = np.empty(shape=batch_size)
        labels = np.empty(shape=batch_size)
        while True:
            for i in range(batch_size):
                word, context, label = next(iterator)
                words[i] = word
                contexts[i] = context
                labels[i] = label
                yield ([words, contexts], labels)