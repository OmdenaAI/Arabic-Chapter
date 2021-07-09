import torch

from transformers import Trainer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from arabert.preprocess import ArabertPreprocessor

from utils.download import download

class GenderAnalyser:
    def __init__(self, text):
        download()
        self.model_name = 'aubmindlab/bert-base-arabertv02'
        self.label_index = {0: 'F', 1: 'M', 2: 'NA'}
        self.device = "cpu"
        self.model = AutoModelForSequenceClassification.from_pretrained("models/gender/")
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
