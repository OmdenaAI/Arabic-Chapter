import spacy

class NER_Tagger:
    def __init__(self):
        self.model = spacy.load('NER/SPACY/')
        
    def classify(self, text):
        doc = self.model(text)
        return [(str(ent), ent.label_) for ent in doc.ents]