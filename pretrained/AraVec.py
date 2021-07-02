import gensim
import json
import urllib.request
import zipfile

class AraVec:
    def __init__(self):
        with open("pretrained/aravec_models.json", "r") as f:
            self.models = json.loads(f.read())


    def list_models(self):
        """
        Lists all AraVec models
        """
        return self.models.keys()


    def get_model(self, model_name , unzip = False):
        """
        Downloads zip archive of AraVec model and can unzip it

        Parameters

        model_name: name of model to be downloaded (from list_models)
        unzip: whether or not to unzip after downloading

        Returns

        model_file: path to model file (can be loaded with load_model)
        """
        assert model_name in self.models.keys() , "model_name is not inserted correctly"

        link = self.models[model_name]
        filename =  link.split('/')[-1]
        urllib.request.urlretrieve (link, filename)
        print("Model Downloaded")

        if unzip == True:
            with zipfile.ZipFile(filename, 'r') as zipf:
                zipf.extractall()
            model_file = filename.replace('zip','mdl')
            print("Model Unzipped ")
        else:
            model_file = filename
        return model_file
        

    def load_model(self, model_path):
        assert model_path.endswith(".mdl") , "model_path should end with .mdl"
        model = gensim.models.Word2Vec.load(model_path)
        return model


    
