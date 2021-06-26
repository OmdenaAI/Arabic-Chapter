
import collections
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error
from pyarabic import araby
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from random import shuffle
from pyarabic import araby
from tensorflow.keras.layers import LSTM, GRU, Embedding, Dense, Input, InputLayer, Dropout, Bidirectional, BatchNormalization, Flatten, Reshape
from tensorflow.keras.models import Sequential
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from utils import tokenizer
from utils.tokenizer import tokenization
from keras.preprocessing.sequence import pad_sequences


class evaluator:
    def __init__(self, embeddings_index, preprocessor):
        self.embeddings_index = embeddings_index
        self.preprocessor = preprocessor
        return

    def word_similarity(self):
        #https://www.researchgate.net/publication/249313626_Arabic_Word_Semantic_Similarity
        y_true = []
        y_pred = []
        for i in open("word_sim_dataset.txt").read().split('\n'):
            i = self.preprocessor(i)
            w1 = i.split()[-1]
            w2 = i.split()[-2]
            st = float(i.split()[-3]) / 4
            
            try:
                w1 = self.embeddings_index[w1] 
                w2 = self.embeddings_index[w2] 
                w1 = w1 / np.linalg.norm(w1)
                w2 = w2 / np.linalg.norm(w2)
                y_pred.append(np.dot(w1,w2))
                y_true.append(st)
            except:
                pass
        if y_true == []:
            return 1.0
        return mean_squared_error(y_true, y_pred, squared=False)



    def concept_categorization(self):
        #https://github.com/AzChaimae/Categorization-dataset-for-Arabic
        dataset = pd.read_csv("Categorization data set.csv", sep=";", header=None)
        dataset.columns = ['concept','word']
        km = KMeans(n_clusters=22, random_state=0)
        km.fit(np.array(list(self.embeddings_index.values())).astype(np.float32))
        preds = []
        for t in np.unique(dataset.concept.values):
            pred = []
            for i in dataset[dataset.concept == t].word.values:
                try:
                    pred.append(km.predict(np.array([self.embeddings_index[i]]))[0])
                except:
                    pred.append("unk")
            preds.append(pred)
        
        scores = []
        for pred in preds:
            a_counter = collections.Counter(pred)
            most_common = a_counter.most_common(2)
            most_freq = [most_common[0] if most_common[0][0] != 'unk' else most_common[1]][0]
            scores.append(most_freq[1] / len([x for x in  pred]))
        return sum(scores) / len(scores)

    def sentiment_analysis(self):
        train_pos = pd.read_csv("data/train_Arabic_tweets_positive_20190413.tsv", sep='\t', names=["label", "tweet"])
        train_neg = pd.read_csv("data/train_Arabic_tweets_negative_20190413.tsv", sep='\t', names=["label", "tweet"])
        train = pd.concat([train_pos, train_neg]).sample(frac=1.0, random_state=0)
        train.tweet = train.tweet.apply(self.preprocessor).apply(tokenization).apply(lambda x: [n for c in x.tokens for n in c])
        le = LabelEncoder()
        le.fit(train.label)
        train.label = le.transform(train.label)

        vocab = np.unique(np.array([x for y in train.tweet.values for x in y ]))
        word_index = {w: i for i, w in enumerate(vocab)}
        self.vocab_size, self.embedding_size = len(word_index),100

        self.embeddings_matrix = np.zeros((self.vocab_size, self.embedding_size))
        for word, i in word_index.items():
            embedding_vector = self.embeddings_index.get(word)
            if embedding_vector is not None:
                self.embeddings_matrix[i] = embedding_vector
            else:
                self.embeddings_matrix[i] = np.random.uniform(size=(1, self.embedding_size))

        seq_list = []
        for words in train.tweet.values:
            seq = []
            for w in words:
                seq.append(word_index.get(w,0))
            seq_list.append(seq)
        train_padded = pad_sequences(seq_list, padding="post", truncating="post", maxlen=100)

        self.X_train, self.X_valid, self.y_train, self.y_valid = train_test_split(train_padded, train.label.values, test_size=0.5,random_state=0, stratify=train.label.values)

        model = self.train_model()
        y_pred = model.predict(self.X_valid)
        return (np.argmax(y_pred, axis=1) == self.y_valid).sum() / self.y_valid.shape[0]

    def word_analogy(self):
        return
    def nmt(self):
        return

    def evaluate(self):
        scores = []
        scores.append(self.word_similarity())
        print("Word Similarity (MSE): ", scores[0])
        scores.append(self.concept_categorization())
        print("Concept Categorization) (acc): ", scores[1])
        scores.append(self.sentiment_analysis())
        print("Sentiment Analysis (acc): ", scores[2])
        return scores

    def train_model(self):
        model = Sequential()
        model.add(Embedding(input_dim=self.vocab_size, output_dim=self.embedding_size, weights=[self.embeddings_matrix], trainable=True))
        model.add(Bidirectional(GRU(units = 32, return_sequences=True)))
        model.add(Bidirectional(GRU(units = 32, return_sequences=False)))
        model.add(Dense(16, activation = 'relu'))
        model.add(Dropout(0.3))
        model.add(Dense(2, activation = 'softmax'))
        model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
        callbacks = [tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=2, min_delta=0.0001, min_lr=0.0001)]
        model.fit(self.X_train, self.y_train, validation_data= (self.X_valid, self.y_valid),
         epochs = 5, batch_size= 128, shuffle = True, callbacks=callbacks)
        return model
