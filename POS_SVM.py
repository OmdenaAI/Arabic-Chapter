import pickle
import gensim
import numpy as np

class POS_SVM:
    def __init__(self):
        self.load_files()
        
    def load_files(self):
        with open("POS/SVM/config.pkl", "rb") as tf:
            self.config = pickle.load(tf)
        self.WINDOW = self.config['Window']
        self.embedding_model = gensim.models.Word2Vec.load('POS/SVM/'+self.config['embedding_model_path'])
        self.tags_list = self.config['tags_list']
        self.ambiguities = self.config['ambiguities']
        self.encoder = pickle.load(open('POS/SVM/'+self.config['encoder'], 'rb'))
        self.model = pickle.load(open('POS/SVM/svm_pos_tag.pickle', 'rb'))
    
    def OneHotEncoder(self,number, lenght):
        zero = np.zeros(lenght)
        zero[number] = 1
        return zero

    def getFeatures(self,wordIdx, sentence, pos, w2v, tags, ambiguities, train=True):
        features = []

        keys = w2v.wv.key_to_index.keys()
        for i in reversed(range(1,int(self.WINDOW)//2+1)):
            if sentence[wordIdx-i] not in keys:
                features.append(np.zeros(w2v.vector_size))
            else:
                features.append(w2v.wv.get_vector(sentence[wordIdx-i], norm=True))

        if sentence[wordIdx] not in keys:
            features.append(np.zeros(w2v.vector_size))
        else:
            features.append(w2v.wv.get_vector(sentence[wordIdx], norm=True))

        for i in range(1,int(self.WINDOW)//2+1):
            if sentence[wordIdx+i] not in keys:
                features.append(np.zeros(w2v.vector_size))
            else:
                features.append(w2v.wv.get_vector(sentence[wordIdx+i], norm=True))
        if train:
            for i in reversed(range(1,int(self.WINDOW)//2+1)):
                tag = pos[wordIdx-i]
                features.append(self.OneHotEncoder(tags.index(tag),len(tags)))

            if sentence[wordIdx] in ambiguities:
                features.append(self.OneHotEncoder([tags.index(i) for i in ambiguities[sentence[wordIdx]]],len(tags)))
            else:
                features.append(self.OneHotEncoder([],len(tags)))

        else:
            for i in reversed(range(1,int(self.WINDOW)//2+1)):
                tag = pos[wordIdx-i]
                features.append(self.OneHotEncoder(tags.index(tag),len(tags)))

            if sentence[wordIdx] in ambiguities:
                features.append(self.OneHotEncoder([tags.index(i) for i in ambiguities[sentence[wordIdx]]],len(tags)))
            else:
                features.append(self.OneHotEncoder([],len(tags)))

        features.append([len(sentence[wordIdx])])

        flat_list = []
        for i in features:
            flat_list.extend(i)
        return flat_list
    
    def classify(self,sent):
        words = sent.split()
        words = ["" for i in range(int(self.WINDOW)//2)] + words + ["" for i in range(int(self.WINDOW)//2)]
        pos = ["PAD" for i in range(int(self.WINDOW)//2)]
        for i in range(int(self.WINDOW)//2,len(words) - int(self.WINDOW)//2):
            feature = np.array(self.getFeatures(i , words, pos, self.embedding_model, self.tags_list, self.ambiguities, train = False)).reshape(1,-1)
            tag = self.model.predict(feature)
            pos.append(self.encoder.inverse_transform(tag)[0])
        output = pos[2:]
        pred_tags = [(sent.split()[i],output[i]) for i in range(len(sent.split()))]
        return pred_tags