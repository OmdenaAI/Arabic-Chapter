from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import tokenizers
import os
'''
this model employs the https://huggingface.co/akhooli/xlm-r-large-arabic-sent model
'''
class Sentiment_analysis:
    def __init__(self):
        self.__loadModel()
        self.nlp = pipeline

    def __loadModel(self):
        '''
        to check whether the model exists. If so, it will load it from the saved model; otherwise, it will be downloaded
        '''
        if os.path.isdir('model') and \
                os.path.isfile("model/pytorch_model.bin") and os.path.isfile("model/sentencepiece.bpe.model") and \
                os.path.isfile('config.json') and os.path.isfile('special_tokens_map.json') and \
                os.path.isfile('tokenizer_config.json') and os.path.isfile('tokenizer.json'):
            model = AutoModelForSequenceClassification.from_pretrained('model')
            tokenizer = AutoTokenizer.from_pretrained('model')

            self.nlp = pipeline(task='sentiment-analysis', model=model, tokenizer=tokenizer)
        else:
            print('Model does not exist. Downloading...')
            self.nlp = pipeline(task='sentiment-analysis', model='akhooli/xlm-r-large-arabic-sent')
            self.nlp.model.save_pretrained(save_directory='model')
            self.nlp.tokenizer.save_pretrained('model')

    def inference(self, text, return_all_scores=True):
        '''
        Input: raw Arabic text
        parameters:
        text (string): raw Arabic text (maximum length(200 words)
        return_all_score (Boolean):default (true) returns all possibility socre for all classes
        returns:
        a tuple for all the class scores:
        LABEL_0: Mixed class
        LABEL_1:Negative class
        LABEL_2:Positive class
        : '''
        if len(text.split(" ")) <= 200:
            self.nlp.return_all_scores = return_all_scores
            return self.nlp(text)
        else:
            print('Text exceeded the maximum length')
            return
