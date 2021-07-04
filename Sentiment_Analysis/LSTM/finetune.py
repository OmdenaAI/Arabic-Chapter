import os

import numpy as np
import pandas as pd

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf

from Sentiment import SentimentAnalysis
from utils import helper, preprocess
from utils.config import config

if __name__ == '__main__':
    """
    The main code for finetuning out pretrained model with your data
    models including - lstm, 1DConv, BidRNN, simpleRNN
    """

    #load data, note: add data path in the config file
    train_data = pd.read_csv(config['train_data_path'])
    val_data = pd.read_csv(config['val_data_path'])
    test_data = pd.read_csv(config['test_data_path'])

    #remove null values from the data
    train_data = train_data.dropna().reset_index(drop=True)
    val_data = val_data.dropna().reset_index(drop=True)
    test_data = test_data.dropna().reset_index(drop=True)

    #OPTIONAL : to split data as folds with stratified labels
    # train_data = helper.get_folds(train_data, 'cleaned_text', 'Class_camel', split=2, getvalue=0)
    # val_data = helper.get_folds(val_data, 'cleaned_text', 'Class_camel', split=2, getvalue=0)
    # test_data = helper.get_folds(test_data, 'cleaned_text', 'Class_camel', split=2, getvalue=0)

    #convert text and label column from series object to ndarray
    train_text, train_label = train_data['cleaned_text'].values.copy(), train_data['Class_camel'].values.copy()
    val_text, val_label = val_data['cleaned_text'].values.copy(), val_data['Class_camel'].values.copy()
    test_text, test_label = test_data['cleaned_text'].values.copy(), test_data['Class_camel'].values.copy()


    #initializing an object for the main sentiment class with hyperparameters needed
    #note : Check config file to alter the hyperparameters
    sentiment = SentimentAnalysis(preprocess.tokenizer,
                                vocab_size=config['vocab_size'],
                                maxlen=config['maxlen'],
                                embedding_vector=config['embedding_vector'],
                                method=config['method'],)
    
    
    #using the tokenize function from class to tokenize all the text
    #note : Check config file to change stop words and punctuations methodology
    train_text = sentiment.tokenize(train_text, punctuations=config['punctuations'], stop_words=config['stop_words'])

    #vectorizing or encoding the text with encoding function from class object
    train_text, train_label, unique_words, word_dict = sentiment.vectorize(train_text, train_label)

    val_text = sentiment.tokenize(val_text, punctuations=config['punctuations'], stop_words=config['stop_words'])
    val_text, val_label, _, _ = sentiment.vectorize(val_text, val_label)

    test_text = sentiment.tokenize(test_text, punctuations=config['punctuations'], stop_words=config['stop_words'])
    test_text, test_label, _, _ = sentiment.vectorize(test_text, test_label)


    #helper train method from the class to train the model with custom data
    model = sentiment.fit(train_text,
                        train_label,
                        validation_data=(val_text, val_label),
                        epochs=config['epochs'],
                        method=config['method'])


    #evaluating the model with test data
    sentiment.evaluate(test_text, test_label, model, batch_size=32)


    #Validation checking
    print(f"\nText : {test_data['cleaned_text'].iloc[45]} Label : {test_data['Class_camel'].iloc[45]}")
    print(sentiment.predict_([test_data['cleaned_text'].iloc[45]], model, batch_size=32))
