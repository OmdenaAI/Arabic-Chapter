
# !pip install optuna==2.3.0
# !pip install transformers==4.2.1
# !pip install farasapy
# !pip install pyarabic
# !git clone https://github.com/aub-mind/arabert

# model link: https://drive.google.com/drive/folders/1cTymQ3j60xUzEGIcn_ogU6jSnET-tjRG?usp=sharing
# labels file: https://drive.google.com/file/d/1CwX2TcwlzfIrR-5JhP9Fw7YPq_NYRvQX/view?usp=sharing

from arabert.preprocess import ArabertPreprocessor
import numpy as np
from sklearn.metrics import classification_report, accuracy_score, f1_score, confusion_matrix, precision_score , recall_score

from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer, BertTokenizer
from transformers.data.processors import SingleSentenceClassificationProcessor
from transformers import Trainer , TrainingArguments
from transformers.trainer_utils import EvaluationStrategy
from transformers.data.processors.utils import InputFeatures
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from sklearn.utils import resample
import logging
import torch
import optuna

# (1)load libraries 
import json, sys, regex
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from tqdm import tqdm, trange
import pandas as pd
import os
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, classification_report, confusion_matrix
##----------------------------------------------------
import pandas as pd
import numpy as np

from tqdm import tqdm_notebook as tqdm
from sklearn.model_selection import train_test_split
##------------------------------------------------------
import re



MODEL_PATH_='/content/drive/MyDrive/Omdena_sentiment/Saved_models/Arabert_production/'
LABEL_2_INDEX_PATH='/content/drive/MyDrive/Omdena_sentiment/Saved_models/Production/Arabert/_labels-dict.json'
_DEFAULT_LABELS=[0,1,2]


class Dataset:
    def __init__(
        self,
        name,
        train,
        test,
        label_list,
    ):
        self.name = name
        self.train = train
        self.test = test
        self.label_list = label_list

class BERTDataset(Dataset):
    def __init__(self, text, target, model_name, max_len, label_map):
      super(BERTDataset).__init__()
      self.text = text
      self.target = target
      self.tokenizer_name = model_name
      self.tokenizer = AutoTokenizer.from_pretrained(model_name)
      self.max_len = max_len
      self.label_map = label_map
      

    def __len__(self):
      return len(self.text)

    def __getitem__(self,item):
      text = str(self.text[item])
      text = " ".join(text.split())


        
      input_ids = self.tokenizer.encode(
          text,
          add_special_tokens=True,
          max_length=self.max_len,
          truncation='longest_first'
      )     
    
      attention_mask = [1] * len(input_ids)

      # Zero-pad up to the sequence length.
      padding_length = self.max_len - len(input_ids)
      input_ids = input_ids + ([self.tokenizer.pad_token_id] * padding_length)
      attention_mask = attention_mask + ([0] * padding_length)    
      
      return InputFeatures(input_ids=input_ids, attention_mask=attention_mask, label=self.label_map[self.target[item]])

class BERTDatasetTest(Dataset):
    def __init__(self, text, model_name, max_len, label_map):
      super(BERTDataset).__init__()
      self.text = text
      self.tokenizer_name = model_name
      self.tokenizer = AutoTokenizer.from_pretrained(model_name)
      self.max_len = max_len
      self.label_map = label_map
      

    def __len__(self):
      return len(self.text)

    def __getitem__(self,item):
      text = str(self.text[item])
      text = " ".join(text.split())


        
      input_ids = self.tokenizer.encode(
          text,
          add_special_tokens=True,
          max_length=self.max_len,
          truncation='longest_first'
      )     
    
      attention_mask = [1] * len(input_ids)

      # Zero-pad up to the sequence length.
      padding_length = self.max_len - len(input_ids)
      input_ids = input_ids + ([self.tokenizer.pad_token_id] * padding_length)
      attention_mask = attention_mask + ([0] * padding_length)    
      
      return InputFeatures(input_ids=input_ids, attention_mask=attention_mask)

import collections
class SentIDPred(collections.namedtuple('SentimentPred', ['top', 'scores'])):
    """A named tuple containing sentiment ID prediction results.
    Attributes:
        top (:obj:`str`): The sentiment label with the highest score. See
            :ref:`sentimentid_labels` for a list of output labels.
        scores (:obj:`dict`): A dictionary mapping each sentiment label to it's
            computed score.
    """

class SentimentIdentificationArabertTPrediction(object):
  """A class for running a fine-tuned sentiment analysis model to predict
    the sentiment of given sentences.


    Args:
        labels (:obj:`set` of :obj:`str`, optional): The set of dialect labels
            used in the training data in the main model.
            If None, the default labels are used.
            Defaults to None.

        training_model_path (:obj:`str`, optional): Path of training model to be used for inference,
        If none, use defult model for this libaray

        label2index (:obj:`str`, optional): Path of label 2 indexx file to be used for scoring,
        If none, use defult model for this libaray

        max_seq_length (:obj:`int`, optional): maximum sequence length for the model
            
            If None, the default max_seq_length are used.
            Defaults to 256 .

    """
  def __init__(self):
       
        self.labels = _DEFAULT_LABELS
        self._labels_sorted = sorted(self.labels)
        self.model_name='aubmindlab/bert-base-arabertv02'
        self.task='classification'
        self.batch_size=16
        self.max_seq_length=256
        self.__arabert_prep = ArabertPreprocessor(self.model_name.split("/")[-1])
      
        self.label_map = json.load(open(LABEL_2_INDEX_PATH))
        


        self.trainer = Trainer(
            model = self.model_init(MODEL_PATH_),
            # args = training_args,
            # train_dataset = train_dataset,
            # eval_dataset=test_dataset,
            compute_metrics=self.compute_metrics,
        )
          
        
  def model_init(self,Path=None):
    if Path is None:
      return AutoModelForSequenceClassification.from_pretrained(self.model_name, return_dict=True, num_labels=len(self.label_map)) 
    else:
      return AutoModelForSequenceClassification.from_pretrained(Path, return_dict=True, num_labels=len(self.label_map)) 
  def compute_metrics(self,p):

    #p should be of type EvalPrediction

    preds = np.argmax(p.predictions, axis=1)
    assert len(preds) == len(p.label_ids)
    #print(classification_report(p.label_ids,preds))
    #print(confusion_matrix(p.label_ids,preds))

    macro_f1_pos_neg = f1_score(p.label_ids,preds,average='macro',labels=[0,1])
    macro_f1 = f1_score(p.label_ids,preds,average='macro')
    macro_precision = precision_score(p.label_ids,preds,average='macro')
    macro_recall = recall_score(p.label_ids,preds,average='macro')
    acc = accuracy_score(p.label_ids,preds)
    return {
        'macro_f1' : macro_f1,
        'macro_f1_pos_neg' : macro_f1_pos_neg,  
        'macro_precision': macro_precision,
        'macro_recall': macro_recall,
        'accuracy': acc
    }

        
  def data_prepare_BERT(self,X_train,y_train):
    X_train = X_train.apply(self.__arabert_prep.preprocess)

    train_dataset = BERTDataset(X_train.to_list(),y_train.to_list(),self.model_name,self.max_seq_length,self.label_map)
    
      
    return train_dataset
  def data_prepare_BERT_test(self,X_test):
    X_test = X_test.apply(self.__arabert_prep.preprocess)

    test_dataset = BERTDatasetTest(X_test.to_list(),self.model_name,self.max_seq_length,self.label_map)
    
    return test_dataset
  def eval(self,X_eval,y_eval, data_set='DEV'):

    """Evaluate the trained model on a given data set.
        Args:
            X_eval (:obj:`np array or pandas series`, optional): loaded data for evaluation.

            y_eval (:obj:`np array or pandas series`, optional): loaded labels for evaluation.

            data_set (:obj:`str`, optional): Name of the provided data set to
                use. This is ignored if data_path is not None. Can be either
                'VALIDATION' or 'TEST'. Defaults to 'VALIDATION'.
        Returns:
            :obj:`dict`: A dictionary mapping an evaluation metric to its
            computed value. The metrics used are accuracy, f1_micro, f1_macro,
            recall_micro, recall_macro, precision_micro and precision_macro.
        """
    validation_inputs = self.data_prepare_BERT(X_eval,y_eval)
    predictions=self.trainer.predict(validation_inputs)
    all_pred=np.argmax(predictions[0],axis=1)
    all_label= [self.label_map[i] for i in y_eval]    
    accuracy = accuracy_score(all_label, all_pred)
    macro_f1_pos_neg = f1_score(all_label, all_pred,average='macro',labels=[0,1])
    f1score = f1_score(all_label, all_pred, average='macro') 
    recall = recall_score(all_label, all_pred, average='macro')
    precision = precision_score(all_label, all_pred, average='macro')
    # Get scores
    scores = {
        'Sentiment': {
            'accuracy': accuracy,
            'f1_macro': f1score,
            'recall_macro': recall,
            'precision_macro':precision
        }
    }
    return scores

  def predict(self,sentences):
    """Predict the sentiment  probability scores for a given list of
        sentences.
        Args:
            sentences (:obj:`list` of :obj:`str`): The list of sentences.
            output (:obj:`str`): The output label type. Possible values are
                'postive', 'neagtive', 'neutral'.
        Returns:
            :obj:`list` of :obj:`SentIDPred`: A list of prediction results,
            each corresponding to its respective sentence.
        """
    if isinstance(sentences, str):
      sentences=pd.Series(sentences)
    validation_inputs = self.data_prepare_BERT_test(sentences)
    predictions=self.trainer.predict(validation_inputs)
    probabilities=predictions[0]
    predicted = np.argmax(predictions[0],axis=1)   
    result = collections.deque()
    convert = lambda x: x     
    for i in range(0,len(predicted)):
      for j, val in self.label_map.items():
      
        if val==predicted[i]:
          result.append(convert(SentIDPred(j, probabilities[i])))
          break

        
      
    return list(result)

"""# Testing Production code"""
Marbert_predictor=SentimentIdentificationArabertTPrediction()

Marbert_predictor.predict('صفاء الهاشم سيده كويتيه المراه الوحيده حاليا مجلس الامه الكويتي مدافعه شرسه حقوق المراه وحق المواطن الكويتي وتمتلك عقليه اقتصاديه مميزه اختيرت ضمن سيده عربيه مؤsثره مجتمعها')