# Overview 
This github repo contains different model implementation for sentiment analysis task, as part of Omdena for building a unified arabic tool on MSA dialect.

# Datasets
The dataset used is based on 7 dataset in MSA and resulting a total of 1,98,389 tweets/reviews divided into 3 classes neutral, negative and positive. 
More information can be found in this link 
[link](https://docs.google.com/spreadsheets/d/17MT_OPUmjSKF323rFNM3pxUBAuES6Mu9Zzpd8V06c34/edit#gid=0)

# Metrics
- F1-Score macro avg
- Percsion macro avg 
- Recall   macro avg
- Accuracy

# Results
| Model                                                       | F1-Macro | Percsion | Recall | Accuracy |
|-------------------------------------------------------------|----------|----------|--------|----------|
| QARiB                                                       | 0.84     | 0.85     | 0.84   | 0.859    |
| MARBERT                                                     | 0.84     | 0.85     | 0.83   | 0.86     |
| AraBERT                                                     | 0.825    | 0.83     | -      | 0.856    |
| Linear SVM + TF-IDF word and character level + CountVector  | 0.71     | 0.71     | 0.72   | 0.739    |
| LR+ TF-IDF word and character level + CountVector           | 0.67     | 0.66     | 0.69   | 0.692    |









