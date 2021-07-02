from datasets import load_dataset,load_metric,list_metrics
from transformers import AutoModelForSequenceClassification, AutoTokenizer,Trainer, TrainingArguments,DataCollatorWithPadding,pipeline
import numpy as np
class huggingface_fine_tuner:
    def __init__(self,model_checkpoint=None, training_path=None,validation_path=None,num_labels=3,sequence_length=64,
                 learning_rate=2e-5, epochs=5,weight_decay=0.01,model_path="model", batch_size=16,
                 labels={0:'neutral',1:'negative',2:'positive'}):
        '''
        inputs: 
        model_checkpoint: the name or the path of the huggingface model to be fine-tuned
        training_path: the path to the csv file of the training dataset- the dataset fields are {labels,sentence}
        validation_path: the path to the csv file of the validation dataset-  the dataset fields are {labels,sentence}
        num_labels: the number of the labels in the dataset
        sequence_length: the preferred length of the sentence
        learning_rate: the learning rate of the model
        epochs: number of the training loops
        weight_decay: training weight_decay
        model_path: a path to save the training checkpoints
        batch_size: the training and validation batch size
        # the csv dataset files must have column named "labels" which contains the labels of the sentiment
        '''
        self.__training_path=training_path
        self.__validation_path=validation_path
        self.__model=AutoModelForSequenceClassification.from_pretrained(model_checkpoint,num_labels=num_labels)
        self.__tokenizer=AutoTokenizer.from_pretrained(model_checkpoint)
        self.__sequence_length=sequence_length
        self.__learning_rate=learning_rate
        self.__epochs=epochs
        self.__weight_decay=weight_decay
        self.__model_path=model_path
        self.__batch_size=batch_size
        self.__collator=DataCollatorWithPadding(tokenizer=self.__tokenizer)
        self.__metric=load_metric('accuracy')
        self.__prepare_dataset()
        self.__tokenize_dataset()
        self.__model.config.id2label=labels
        self.__model.config.label2id={label:id for id,label in labels.items()}
        self.__training_args=TrainingArguments(TrainingArguments(self.__model_path,evaluation_strategy="epoch",
                                per_device_train_batch_size=self.__batch_size,
                                per_device_eval_batch_size=self.__batch_size,
                                learning_rate=self.__learning_rate,
                                weight_decay=self.__weight_decay,
                                num_train_epochs=self.__epochs))
        self.__trainer=Trainer(
                        self.__model,
                        self.__training_args,
                        train_dataset=self.__tokenized_datasets["train"],
                        eval_dataset=self.__tokenized_datasets["validation"],
                        data_collator=self.__collator,
                        tokenizer=self.__tokenizer,
                        compute_metrics=self.__compute_metrics,    
                    )
    def __prepare_dataset(self): 
        self.__dataset=load_dataset('csv',data_files={'train':self.__training_path ,
                                   'validation':self.__validation_path})
    def __tokenization(self,example):
        return self.tokenizer(example["sentence"], truncation=True,max_length=self.__sequence_length)
    def __tokenize_dataset(self):
        self.__tokenized_dataset=self.__dataset.map(self.__tokenization, batched=True)
    
    def __compute_metrics(self,eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return self.__metric.compute(predictions=predictions, references=labels)
    def train(self):
        self.__trainer.train()
        self.__pipeline=pipeline(task='sentiment-analysis',model=self.__model,tokenizer=self.__tokenizer)
    def save_model(self,path=None):
        if path==None:
            return "Please provide a path"
        self.__model.save_pretrained(path)
        self.__tokenizer.save_pretrained(path)
    def inference(self,text,return_all_scores=True):
        self.__pipeline.return_all_scores = return_all_scores
        return self.__pipeline(text)