import gensim
import json
import os
import urllib.request

#TODO: Add ability to list and download models, 
class aravec:
    def __init__(self):
        with open("pretrained/aravec_models.json", "r") as f:
            self.models = json.loads(f.read())
    def list_models(self):
        return self.models.keys()
    def get_model(self, model_name):
        if model_name not in self.models.keys():
            print("ERROR: Model not in list of available models. Try list_models()")
            return
        link = self.models[model_name]
        filename =  link.split('/')[-1]
        urllib.request.urlretrieve (link, filename)
        return self.load_model(filename)
        
    def load_model(self, model_path):
        model = gensim.models.Word2Vec.load(model_path)
        return model


