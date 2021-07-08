from gensim.models import KeyedVectors

from utils import helper
from utils.download import download
from utils.tokenizer import clean_str, normalize, strip_all, tokenization, process


class WordEmbedding:
    def __init__(self, text, method):
        download()
        self.text = text
        self.method = method

    def preprocess(self, text):
        return process(text)

    def get_preprocessed_word2vec(self):
        tokens = self.preprocess(self.text)
        return tokens

    def get_preprocessed_aravec(self):
        tokens = [clean_str(x) for x in self.text.strip().split()]
        return tokens

    def get_model(self):
        if self.method == "aravec":
            model = KeyedVectors.load("models/aravec/Twitter_CBOW_100.wordvectors", mmap='r')
            return model
        elif self.method == "word2vec":
            model = KeyedVectors.load("models/mottagah_large_wv.wordvectors", mmap='r')
            return model

    def get_embeddings(self, tokens, model):
        embeddings = dict()
        embeddings_index = helper.get_embedding_matrix(model)
        for token in tokens:
            try:
                embeddings[token] = embeddings_index[token].tolist()
            except :
                embeddings[token] = ["word not found"]
        return embeddings

        
    def get_analogy(self, tokens, model):
        positive = [tokens[1], tokens[2]]
        negative = [tokens[0]]
        print("neg ", negative)
        out = dict()
        analogies = model.most_similar(positive=positive, negative=negative, topn=20) 
        for word, sim in analogies:
            out[word] = sim
        return out

    def get_similar(self, tokens, model, include_token=False):
        similar = dict()
        for token in tokens:
            try:
                similar_list = model.most_similar(token, topn=20)
                if include_token:
                    similar[token] = similar_list
                    continue
                similar_edited = []
                for word, sim in similar_list:
                    if not token in word:
                        similar_edited.append((word, sim))
                similar[token] = similar_edited
            except :
                similar[token] = ["word not found"]
        return similar
