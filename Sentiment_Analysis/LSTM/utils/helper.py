from tensorflow.keras import regularizers
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from tensorflow.keras.layers import concatenate
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.regularizers import l1, l2
from sklearn.model_selection import StratifiedKFold


# OPTIONAL - spliting the data as folds with strtifying the labels
def get_folds(df, source, target, split=4, getvalue=0):
    """
    helper function to generate folds
    params:
    df: dataframe to get folds
    source: text column name in the data 
    target: target column name in the data
    split: no of splits
    getvalue: get ith splitted data 
    retuns:
    splitted dataframe
    """
    df.loc[:, "kfold"] = -1

    #shuffling the data
    df = df.sample(frac=1).reset_index(drop=True)
    X = df[source].values
    y = df[target].values

    # initializing the onject for the strtifiedkold class with custom splits
    skf = StratifiedKFold(n_splits=split)

    for fold_, (train_, val_) in enumerate(skf.split(X=X, y=y)):
        df.loc[val_, "kfold"] = fold_
    return df.loc[df['kfold'] == getvalue]


# function to return the word dictionary, 
# word with its encoding 
def word_dictionary(text):
    """
    helper function to generate word index
    params:
    text: tokenized list of text
    retuns:
    dictionary of words with its index
    """

    # removing duplicate texts
    text = set(list(text))

    # creating a dictionary with word and its id
    dictionary = {}
    for i, word in enumerate(text):
        dictionary[word] = i

    return dictionary


# prediction function for inference
def predict(text, model, tokenize, vocab, maxlen):
    """
    helper function to predict results on new data
    params:
    text: vectorized list of text
    model: trained model
    tokenize: tokenizer reference to tokenize the text
    vocab_size: total vocabulary size of the data
    maxlen: maximum length of the texts
    retuns:
    list of prediction
    """

    # returns the tokenized texts
    text, _, _ = tokenize(text)

    #encoding each token in the text with ids
    #and returing after padding with maxlen
    vector, temp = [], []
    for d in text:
        for i in d:
            temp.extend(one_hot(i, vocab))
        vector.append(temp)
        temp=[]
    vector = pad_sequences(vector, maxlen=maxlen, padding="post")
    return vector


def get_model(X, y, vocab_size, embedding_size, maxlen, method):
    """
    helper function to get the model architecture
    params:
    X: vectorized list of text
    y: list of labels
    vocab_size: total vocabulary size of the data
    embedding_size: embedding dim for the model
    maxlen: maximum length of the texts
    method
    returns:
    model: model architecture
    """

    #simpleRNN model architecture
    #layers including - Embedding, SimpleRNN, Dense
    if method == "simpleRNN":
        model = Sequential()
        model.add(Embedding(vocab_size, embedding_size, input_length=maxlen ,name="embedding"))
        model.add(SimpleRNN(64))
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(32, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(3, activation='softmax'))
    
    #bidRNN model architecture
    #layers including - Embedding, lstm, Dense
    elif method == "bidRNN":
        model = Sequential()
        model.add(Embedding(vocab_size, embedding_size, input_length=maxlen ,name="embedding"))
        model.add(Bidirectional(LSTM(64)))
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(32, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(3, activation='softmax'))

    #1DConv model architecture
    #layers including - Embedding, Convolution1D, Dense
    elif method == "1DConv":
        model = Sequential()
        model.add(Embedding(vocab_size, embedding_size, input_length=maxlen ,name="embedding"))
        model.add(Convolution1D(filters=64,kernel_size=7,activation='relu', kernel_regularizer=l2(0.001), bias_regularizer=l2(0.001)))
        model.add(MaxPooling1D(pool_size=3))
        model.add(Convolution1D(filters=64,kernel_size=7,activation='relu', kernel_regularizer=l2(0.001), bias_regularizer=l2(0.001)))
        model.add(MaxPooling1D(pool_size=3))
        model.add(Convolution1D(filters=32,kernel_size=3,activation='relu', kernel_regularizer=l2(0.001), bias_regularizer=l2(0.001)))
        model.add(MaxPooling1D(pool_size=3))
        model.add(Flatten())
        model.add(Dense(activation='relu',units=64))
        model.add(Dropout(0.4))
        model.add(Dense(activation='relu',units=32))
        model.add(Dense(units=3,activation='softmax'))

    #lstm model architecture
    #layers including - Embedding, lstm, Dense
    elif method == "lstm":
        sequence = Input(shape=(maxlen,), dtype='int32')
        embedded = Embedding(vocab_size, embedding_size, input_length=maxlen)(sequence)
        forwards = LSTM(64)(embedded)
        backwards = LSTM(64, go_backwards=True)(embedded)
        merged = concatenate([forwards, backwards])
        after_dp = Dropout(0.2)(merged)
        output = Dense(3, activation='softmax')(after_dp)
        model = Model(inputs=sequence, outputs=output)

    return model
