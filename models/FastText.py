##Based on: https://www.kaggle.com/allank/simple-keras-fasttext-with-increased-training-data

import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Embedding, SpatialDropout1D, concatenate
from tensorflow.keras.layers import GRU, Bidirectional, GlobalAveragePooling1D, GlobalMaxPooling1D
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split


class FastText:


    def __init__(self):
        return


    def fasttext_model(self, input_dim, embedding_dims, maxlen, label_dim):
        inp = Input(shape=(maxlen, ))
        x = Embedding(input_dim, embedding_dims,name="word_embedding")(inp)
        x = SpatialDropout1D(0.2)(x)
        x = Bidirectional(GRU(40, return_sequences=True))(x)
        avg_pool = GlobalAveragePooling1D()(x)
        max_pool = GlobalMaxPooling1D()(x)
        conc = concatenate([avg_pool, max_pool])
        outp = Dense(label_dim, activation="softmax")(conc)
        model = Model(inputs=inp, outputs=outp)

        model.compile(loss='categorical_crossentropy',
                    optimizer='adam',
                    metrics=['accuracy'])

        return model


    def train(self, seqs, y, input_dim, embedding_dims=100, maxlen=128, label_dim=2, epochs=5, batch_size=128, split_size=0.3):
        """
        Trains a FastText model by classification 

        Parameters 

        seqs: numpy array of n-gram token indices padded to maxlen
        y: classification labels
        input_dim: number of unique tokens + 1

        Returns 

        model: trained FastText model
        """
        seqs = np.array(seqs)
        x_train, x_test, y_train, y_test = train_test_split(seqs, y, test_size=split_size)

        n_samples = x_train.shape[0]
        model = self.fasttext_model(input_dim, embedding_dims, maxlen, label_dim)
        hist = model.fit(x_train, y_train,
                        batch_size=batch_size,
                        validation_data=(x_test, y_test),
                        epochs=epochs,
                        callbacks=[EarlyStopping(patience=2, monitor='val_loss')])        
        return model

    def create_docs(self, arr, n_gram_max=2):
        def add_ngram(q, n_gram_max):
                ngrams = []
                for n in range(2, n_gram_max+1):
                    for w_index in range(len(q)-n+1):
                        ngrams.append('--'.join(q[w_index:w_index+n]))
                return q + ngrams
            
        docs = []
        for doc in arr:       
            doc = doc.split()
            docs.append(' '.join(add_ngram(doc, n_gram_max)))
        
        return docs
