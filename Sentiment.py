import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa
from sklearn import metrics, model_selection, preprocessing
from tensorflow.keras.callbacks import *
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import SGD, Adadelta, Adam, Adamax, RMSprop
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import one_hot

from utils import helper
from utils.config import config


#Main class for sentiment analysis
class SentimentAnalysis:
    """
    Class to instantiate the analytics functions
    for the analysis
    params:
    tokenizer: helper to convert tokens
    vocab_size: vocabulary size for the texts
    max_len: maximum length of texts
    embedding_vector: embedding vector dimention for the model
    method: model name
    """


    def __init__(self, tokenizer, vocab_size=30000, maxlen=256, embedding_vector=50, method="simpleRNN"):
        #model name for training
        self.method = method

        #tokenizer function
        self.tokenizer = tokenizer

        #hyperparameters - check config file
        self.vocab_size = vocab_size
        self.maxlen = maxlen
        self.embedding_vector = embedding_vector

        #custom optimizer to choose for training
        self.optim = {'adam':Adam,
                    'adamax':Adamax,
                    'adadelta':Adadelta,
                    'SGD':SGD,
                    'RMSprop':RMSprop}


    def tokenize(self, text, punctuations=[], stop_words=[]):
        """
        helper function to convert sentences to tokens
        params:
        text: texts
        punctuations: list of punctuations for removing in the text
        stop_words: stop words list for the text
        returns:
        tokens: splitted tokens
        """

        #returns the tokens, maxlen found within the text and vocab size
        tokens, maxlen, vocab = self.tokenizer(text, punctuations, stop_words)
        if self.maxlen == 'auto':
            self.maxlen = maxlen
        if self.vocab_size == 'auto':
            self.vocab_size = vocab

        # note : providing auto in the config file for the parameters,
        # the tokenizer finds them automatically
        return tokens


    def vectorize(self, text, label, return_label=True):
        """
        helper function to vectorize tokens
        params:
        text: tokenized list of text
        label: list of labels
        return_label: optional, to return the labels
        returns:
        vectors: vectorized tokens
        """
        vector, temp, all_ = [], [], []
        # prcessing each text individually
        for d in text:
            # each tokens in a text
            for i in d:
                # creating a new list containing the vectorized tokens for each token
                # in the text
                temp.extend(one_hot(i, self.vocab_size))
            vector.append(temp)
            temp=[]

        # padding the text array to a fixed length to be able use it for training
        vector = pad_sequences(vector, maxlen=self.maxlen, padding="post")
        for x in text:
            all_.extend(x)
        
        # a helper function to return word dictionary with all the words present in the data
        word_dict = helper.word_dictionary(all_)

        # converting labels as categorical array woth the length of
        # the, no of labels
        if return_label:
            onehot_encoder = preprocessing.OneHotEncoder(sparse=False)
            label = np.array(label).reshape(len(label), 1)
            label = onehot_encoder.fit_transform(label)

            # returning the vectorized text and label with all unique words and its index
            return vector, label, list(word_dict.keys()), word_dict
        return vector, list(word_dict.keys()), word_dict


    def fit(self, trainX, trainY, validation_data=(), epochs=10, batch_size=32, method='simpleRNN'):
        """
        helper function to train vectors of text with the labels
        params:
        trainX: vectorized list of text
        trainY: list of labels
        validation_data: optional, data for validating
        epochs: iteration number
        batch_size: batch size for data
        method: model name
        returns:
        model: trained model
        """
        validX, validY = validation_data

        #helper method tp get the appropriate model
        model = helper.get_model(trainX, trainY, self.vocab_size, self.embedding_vector, self.maxlen, self.method)

        # model compilation
        # check config file to alter the parameters
        model.compile(optimizer=self.optim[config['optim']](learning_rate=config['learning_rate']), loss=tf.keras.losses.CategoricalCrossentropy(), metrics=["accuracy",tf.keras.metrics.Precision(),tf.keras.metrics.Recall(),tf.keras.metrics.AUC()])

        tqdm_callback = tfa.callbacks.TQDMProgressBar()
        # custom callbacks to include in the training
        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1,patience=5)  
        mc = ModelCheckpoint(config['save_model_path'] + method + "_model.h5", monitor='val_loss', mode='min', save_best_only=True,verbose=1)
        
        # predefined fit method from tf module
        model.fit(trainX, trainY, batch_size=batch_size, validation_data=(validX, validY), epochs=epochs, callbacks=[mc, tqdm_callback], verbose=0)
        
        # saving the model weights with the path provided
        model.save_weights(config['save_weights_path'] + method + "_weights.h5", overwrite=True)

        return model

    #custom evaluate function to test on test data
    def evaluate(self, text, label, model, batch_size=32):
        """
        helper function to evaluate on new data
        params:
        text: vectorized list of text
        label: list of labels
        model: trained model
        batch_size: batch size for data
        """
        loss, acc, pre, rec, auc  = model.evaluate(text, label, workers=-1, batch_size=batch_size)
        print("\nValidation loss: {}  Validation acc: {} Precision: {} Recall: {} Auc Roc: {}".format(loss, acc, pre, rec, auc))


    # custom predict function for inferencing
    def predict_(self, text, model, batch_size=32, print_=True):
        """
        helper function to predict results on new data
        params:
        text: vectorized list of text
        model: trained model
        batch_size: batch size for data
        print_: OPTIONAL, if True, just prints, else returns as list
        retuns:
        list of prediction
        """
        temp = text.copy()
        # helper method to vectorize the text
        temp = helper.predict(temp, model, self.tokenizer, self.vocab_size, self.maxlen)

        # defined method to predict results from the model
        pred = model.predict(temp, batch_size=batch_size)

        # conditional - if print_, its just returns the results as dictionary with probabilities
        # if not returns the prediction as an array
        if print_:
            result = dict()
            for i, p in enumerate(pred):
                preds = [{'label:':'Neutral','score:':p[1],},
                        {'label:':'Negative','score:':p[0],},
                        {'label:':'Positive','score:':p[2],}]
                #result[text[i].encode("unicode_escape")]=preds
                result[text[i]]=preds
            return result
        else:
            gtruth = ["Negative", "Neutral", "Positive"]
            return [gtruth[np.argmax(p)] for p in pred]
