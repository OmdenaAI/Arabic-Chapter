import gensim
import json
import os
import urllib.request

class aravec:
    def __init__(self):
        with open("pretrained/aravec_models.json", "r") as f:
            self.models = json.loads(f.read())


    def list_models(self):
        """
        Lists all AraVec models
        """
        return self.models.keys()


    def get_model(self, model_name):
        #TODO: raise error if model_name isn't in list of available models
        link = self.models[model_name]
        filename =  link.split('/')[-1]
        #TODO: add option to unzip model file after downloading
        urllib.request.urlretrieve (link, filename)
        print("Downloaded model ", filename)
        return
        

    def load_model(self, model_path):
        #TODO raise error if model_path doesn't end with .mdl
        model = gensim.models.Word2Vec.load(model_path)
        return model


