import pandas as pd
import glob

import unicodedata as ud

import numpy as np
import pickle
import matplotlib.pyplot as plt
from collections import Counter

from sklearn import feature_extraction, model_selection

from scipy.stats import entropy
from math import log, e


#get all csv files and concatenate them into single dataframe
path = r'../data/'
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

data = pd.concat(li, axis=0, ignore_index=True)

#remove NaN
data = data[data['article'].notna()]

#remove punctuation
for i in range(data.shape[0]):
    data.iloc[i][0] = ''.join(c for c in data.iloc[i][0] if not ud.category(c).startswith('P'))

#split sentences to words
words = pd.DataFrame()
for i in range(data.shape[0]):
    words = words.append(data.iloc[i][0].split())

wordsFrequency = pd.DataFrame(Counter(words[0]).most_common(50), columns=['word', 'frequency'])

#calculate mean and variance
FreqOfWordInDocs = []
numberOfDistinctWordsInDocs = []
propOfWordInDocs = []

path = r'../data/'
all_files = glob.glob(path + "/*.csv")

li = []
file_number = 0

for filename in all_files:
    data = pd.read_csv(filename, index_col=None, header=0)
    
    #remove NaN
    data = data[data['article'].notna()]

    #remove punctuation
    for i in range(data.shape[0]):
        data.iloc[i][0] = ''.join(c for c in data.iloc[i][0] if not ud.category(c).startswith('P'))

    #split sentences to words
    words = pd.DataFrame()
    for i in range(data.shape[0]):
        words = words.append(data.iloc[i][0].split())

    #add number of distinct words in each doc to a list
    numberOfDistinctWordsInDocs.append(words[0].unique().shape[0])

    #word frequency in each Doc
    FreqOfWord = pd.DataFrame(Counter(words[0]).most_common(30), columns=['word', 'frequency'])
    wordsFrequencyDict = dict()
    for i in range(FreqOfWord.shape[0]):
             wordsFrequencyDict[FreqOfWord.word[i]] = FreqOfWord.frequency[i]

    #add number of frequency of most common words in each doc to a list
    FreqOfWordInDocs.append(wordsFrequencyDict) 

    #probability of each 30 common word in each doc
    wordsProbabilityDict = dict()
    for i in wordsFrequencyDict :
             wordsProbabilityDict[i] = wordsFrequencyDict[i]/numberOfDistinctWordsInDocs[file_number]

    #add probability of most common words in each doc to a list
    propOfWordInDocs.append(dict(sorted(wordsProbabilityDict.items(), key=lambda item: item[1], reverse=True)))
    
    file_number+=1
    
# df_propOfWordInDocs = pd.DataFrame.from_dict(propOfWordInDocs)

key_words = wordsFrequency.word.tolist()
df_propOfWordInDocs = pd.DataFrame(propOfWordInDocs, columns = key_words)
df_propOfWordInDocs.fillna(0)

series_MP = df_propOfWordInDocs.mean()
series_VP = df_propOfWordInDocs.var().sort_values(ascending=False)

totalWordsInAllDocs = 0
for i in range(wordsFrequency.shape[0]):
    totalWordsInAllDocs += wordsFrequency.frequency[i]

ENTRPOY = dict()
for key in key_words:
    p = df_propOfWordInDocs[key].values
    ENTRPOY[key] = entropy(p)

#sorting
ENTRPOY = dict(sorted(ENTRPOY.items(), key=lambda item: item[1], reverse=True))


#### apply Borda ranking
n = 50
RANK = dict()

for key in series_MP.keys():
    RANK[key]=n
    n-=1

n = 50
for key in series_VP.keys():
    RANK[key]+=n
    n-=1
    
n = 50
for key in ENTRPOY.keys():
    RANK[key]+=n
    n-=1

RANK = dict(sorted(RANK.items(), key=lambda item: item[1], reverse=True))
RANK_keys = list(RANK.keys())

print("top 50 Arabic words after applying \"Borda\" ranking:")
print(RANK_keys)