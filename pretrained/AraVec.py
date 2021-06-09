import gensim
import json
import os
import urllib.request
import numpy as np
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


    def get_embedding_matrix(self, model):

        embeddings_index = {}
        for word,vector in zip(model.wv.index_to_key,model.wv.vectors):
            coefs = np.asarray(vector, dtype='float32')
            embeddings_index[word] = coefs
        return embeddings_index

    def load_embedding_matrix(self, vocabulary_size, embedding_dim, word_index, embeddings_index):

      embeddings_matrix = np.zeros((vocabulary_size, embedding_dim))
      for word, i in word_index.items():
          embedding_vector = embeddings_index.get(word)
          if embedding_vector is not None:
              embeddings_matrix[i] = embedding_vector
          else:
              embeddings_matrix[i] = np.random.uniform(size=(1, embedding_dim))

      return embeddings_matrix
    
