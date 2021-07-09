
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import GRU, Embedding, Dense,Dropout, Bidirectional 
from tensorflow.keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
from sklearn import metrics
from utils.tokenizer import tokenization
from utils import helper

class evaluator:
    def __init__(self, embeddings_index, preprocessor, embedding_size):
        self.embeddings_index = embeddings_index
        self.preprocessor = preprocessor
        self.embedding_size = embedding_size
        return


    def word_analogy(self):
        """
        Intrinsic evaluation mehtod that uses a translated
        138-line subset of Google word analogy dataset
        returns accuracy
        """
        data = open("data/word_analogy_subset.en.ar.txt").read().split('\n')
        data = [x for x in data if len(x.split()) == 4]
        cnt = 0
        keys = list(self.embeddings_index.keys())
        vectors = np.array(list(self.embeddings_index.values()))
        norms = np.linalg.norm(vectors, axis=1)
        for i in data:
            i = self.preprocessor(i).split()
            try:
                v = self.embeddings_index[i[0]] -  self.embeddings_index[i[1]] + self.embeddings_index[i[2]]
            except:
                continue
            unit = v / np.linalg.norm(v)
            dists = np.dot(vectors, unit) / norms
            best = np.argpartition(-dists, 10)[:10 + 1]
            best = best.take(np.argsort((-dists).take(best)))
            result = [(keys[sim], float(dists[sim]))
                for sim in best]
            sbv = result[:10]
            for j in sbv:
                if j[0] == i[3]:
                    cnt += 1
        return cnt/ len(data)


    def word_similarity(self):
        """
        Intrinsic evaluation method that compares 
        model word similarity to word similarity 
        judged by human participants 

        returns MSE (lower is better)
        """
        y_true = []
        y_pred = []
        for i in open("data/word_sim_dataset.txt").read().split('\n'):
            i = self.preprocessor(i)
            w1 = i.split()[-1]
            w2 = i.split()[-2] 
            st = float(i.split()[-3]) / 4 #dataset has scale from 0 to 4
            
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
        """
        Intrinsic evaluation method that computes 
        purity score for clustering words
        according to the concept they share

        returns purity (higher is better)
        """
        dataset = pd.read_csv("data/Categorization data set.csv", sep=";", header=None)
        dataset.columns = ['concept','word']

        cti = {}
        for i,c in enumerate(np.unique(dataset.concept.values)):
            cti[c] = i
        y_true = dataset.concept.apply(lambda x: cti[x]).values
        vs = []
        preds = [''] * dataset.shape[0]
        for ind,w in enumerate(dataset.word.values):
            try:
                vs.append(self.embeddings_index[w])
            except:
                preds[ind] = 0 
        km = KMeans(n_clusters=22, random_state=0)
        km.fit(np.array(vs).astype(np.float32))
        for ind,w in enumerate(dataset.word.values):
            if preds[ind] == '':
                preds[ind] = km.predict(np.array([self.embeddings_index[w]]))[0]
        contingency_matrix = metrics.cluster.contingency_matrix(y_true, preds)
        #purity score
        return np.sum(np.amax(contingency_matrix, axis=0)) / np.sum(contingency_matrix) 

    def sentiment_analysis(self):
        """
        Extrinsic evaluation method that trains 
        a sentiment analysis model on a small balanced dataset 

        returns accuracy
        """
        train_pos = pd.read_csv("data/train_Arabic_tweets_positive_20190413.tsv", sep='\t', names=["label", "tweet"])
        train_neg = pd.read_csv("data/train_Arabic_tweets_negative_20190413.tsv", sep='\t', names=["label", "tweet"])
        train = pd.concat([train_pos, train_neg])
        train.tweet = train.tweet.apply(self.preprocessor).apply(tokenization).apply(lambda x: x.tokens[0])
        le = LabelEncoder()
        le.fit(train.label)
        train.label = le.transform(train.label)

        sentence_inds, vocab, self.num_tokens, word_index, index_word = helper.encode_tokens(train.tweet.values)


        self.embeddings_matrix = helper.load_embedding_matrix(self.num_tokens, self.embedding_size, 
                                                                word_index, self.embeddings_index)


        train_padded = pad_sequences(sentence_inds, padding="post", truncating="post", maxlen=100)

        self.X_train, self.X_valid, self.y_train, self.y_valid = train_test_split(train_padded, train.label.values, test_size=0.5,random_state=0, stratify=train.label.values)

        model = self.train_model()
        y_pred = model.predict(self.X_valid)
        return (np.argmax(y_pred, axis=1) == self.y_valid).sum() / self.y_valid.shape[0]


    def evaluate(self):
        """
        Runs all evaluation methods

        returns a list of scores
        """
        scores = []
        scores.append(self.word_analogy())
        print("Word Analogy (acc): ", scores[0])
        scores.append(self.word_similarity())
        print("Word Similarity (MSE): ", scores[1])
        scores.append(self.concept_categorization())
        print("Concept Categorization (purity): ", scores[2])
        scores.append(self.sentiment_analysis())
        print("Sentiment Analysis (acc): ", scores[3])
        return scores

    def train_model(self):
        model = Sequential()
        model.add(Embedding(input_dim=self.num_tokens, output_dim=self.embedding_size, weights=[self.embeddings_matrix], trainable=True))
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