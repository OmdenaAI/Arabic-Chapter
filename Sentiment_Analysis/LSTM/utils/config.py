import pickle

#custom stopwords list
with open("Datasets/stopWords.pkl", 'rb') as f:
    stop_words = list(pickle.load(f))
    stop_words = list(set(stop_words + ['و','في','من','بواسطة','أ','هو','و','في','سيكون','إلى','كان','كن','هو','ال','و','ما','ء','ه','س']))

#config dir to use for many parameters
config = {
    'vocab_size':60000, # vocabulary size for the data
    'maxlen':180, # maximum length of a sentence
    'embedding_vector':100, # embedding vector dimension

    'method':'1DConv', #other - simpleRNN, bidRNN, 1DConv, lstm
    'stop_words':stop_words,
    'punctuations':"""'!"-#$%&'()*+,«».؛،/:؟?@[\]^_`{|}~""",

    'epochs':70, # iteration range
    'batch_size':32, # batch size for the data
    'optim':'SGD', # other - adamax, adadelta, SGD, Adam, RMSprop
    'learning_rate':5e-3, # learning rate for the optimizer

    'save_model_path':'models/', # path for saving model
    'save_weights_path':"models/", # path for saving model weights OPTIONAL
    'train_data_path':"Datasets/Final_Dataset/Dataset/train.csv", # path to train data
    'val_data_path':"Datasets/Final_Dataset/Dataset/val.csv", # path to val data OPTIONAL
    'test_data_path':"Datasets/Final_Dataset/Dataset/test.csv", # path to test data OPTIONAL
}
