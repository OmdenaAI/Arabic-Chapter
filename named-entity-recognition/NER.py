import spacy

class NER:
    def __init__(self):
        self.model = spacy.load('spacy_model/')
        
    def classify(self, text):
        doc = self.model(text)
        return [(str(ent), ent.label_) for ent in doc.ents]