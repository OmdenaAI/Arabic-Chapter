import torch

from transformers import Trainer, TrainingArguments
from transformers.data.processors.utils import InputFeatures
from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer, BertTokenizer
from transformers.data.processors import SingleSentenceClassificationProcessor
from arabert.preprocess import ArabertPreprocessor

from utils.download import download

class POSAnalyser:
    def __init__(self, text):
        download()
        self.model_name = 'aubmindlab/bert-base-arabertv02'
        self.label_index = {0: 'Quantity Noun', 1: 'Verb',2: 'Number Noun',3: 'Interrogative Pronoun',4: 'Particle',5: 'Restrictive Particle',
            6: 'Digit',7: 'Preposition',8: 'Conjunction',9: 'Abbreviation',10: 'Numerical Adjective',11: 'Focus Particle',12: 'Relative Adverb',
            13: 'Relative Pronoun',14: 'Comparative Adjective',15: 'Proper Noun',16: 'Vocalized Particle',17: 'Pseudo Verb',18: 'Demonstrative Pronoun',
            19: 'Foreign',20: 'Verbal Particle',21: 'Interrogative Adverb',22: 'Adverb',23: 'Adjective',24: 'Negative Particle',25: 'Interrogative Particle',
            26: 'Pronoun',27: 'Noun',28: 'Future Particle',29: 'Punctuation',30: 'Subordinating Conjunction',31: 'Determiner Particle'}
        self.device = "cpu"
        self.model = AutoModelForSequenceClassification.from_pretrained("models/pos/")
        self.maxlen = 256
        self.preprocessor = ArabertPreprocessor(self.model_name.split("/")[-1])
        self.text = self.preprocessor.preprocess(text)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def tokenize(self):
        inputs, mask = [], []
        for val in self.text.split():
            input_ids = self.tokenizer(
                val,
                add_special_tokens=True,
                max_length=self.maxlen,
                truncation='longest_first',
                padding="max_length",
                return_tensors="pt",
            )     
            
            inputs.append(input_ids["input_ids"])
            mask.append(input_ids["attention_mask"])
        return inputs, mask

    def predict_(self, inputs, mask):
        preds = dict()
        splits = self.text.split()
        self.model = self.model.eval().to(self.device)
        for i, (input_ids, attention_mask) in enumerate(zip(inputs, mask)):
            with torch.no_grad():
                prediction = self.model(input_ids=input_ids.to(self.device), attention_mask=attention_mask.to(self.device)).logits
                prediction = self.label_index[torch.argmax(prediction, dim=1).item()]
            preds[splits[i]] = prediction
        return preds