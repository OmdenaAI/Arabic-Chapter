import pickle
with open("data/stopWords.pkl", 'rb') as f:
    stop_words = list(pickle.load(f))
    stop_words = list(set(stop_words + ['و','في','من','بواسطة','أ','هو','و','في','سيكون','إلى','كان','كن','هو','ال','و','ما','ء','ه','س']))

config = {
    'vocab_size':'auto',# use 'auto' for w2v
    'maxlen':2,
    'embedding_vector':50,

    'method':'word2vec',#keras
    'stop_words':stop_words,
    'punctuations':"""'!"-#$%&'()*+,«».؛،/:؟?@[\]^_`{|}~""",

    'epochs':2,
    'test_size':0.2,
    'window_size':2,

    'save_model_path':'models/',
    'save_weights_path':"models/",
    'train_data_path':"Datasets/Final_Dataset/Dataset/train.csv",
    'val_data_path':"Datasets/Final_Dataset/Dataset/val.csv",
    'test_data_path':"Datasets/Final_Dataset/Dataset/test.csv",
}
