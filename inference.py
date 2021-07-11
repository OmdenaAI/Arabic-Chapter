import pandas as pd
import tensorflow as tf

from Sentiment import SentimentAnalysis
from utils import helper, preprocess



if __name__ == '__main__':
    """
    Main code for inferencing with pretrained models
    models including - lstm, 1DConv, BidRNN, simpleRNN
    """

    #read your data
    data = pd.read_csv("data path")

    #remove null values
    data = data.dropna().reset_index(drop=True)

    #array of strings
    #convert text column from series object to ndarray
    text = data["Text"].values

    #load model weights using tensorflow helper method "load_model"
    model = tf.keras.models.load_model("models/lstm_model.h5") # replace model name with the models available

    #initializing an object for the main sentiment class
    sentiment = SentimentAnalysis(preprocess.tokenizer,
                                vocab_size=60000,
                                maxlen=180,
                                embedding_vector=300,
                                method="lstm",) #method need to accsess processing technique related to the model provided

                                
    #calling the helper predict function for inferencing from the sentiment class
    preds = sentiment.predict_(text, model, batch_size=32, print_=False)
    #note : use print_=False to just return array of prediction

    #add the results to the data as a series column
    data["prediction"] = preds

    #check the results
    data.head()
