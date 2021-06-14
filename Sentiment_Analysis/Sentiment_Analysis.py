from Alkholi import *
class Sentiment_Analysis:
    def __init__(self,model):
        if model=='Alkholi':
            print('up')
            self.pipeline=Sentiment_analysis()
    def predict(self,text):
        return self.pipeline.inference(text)
