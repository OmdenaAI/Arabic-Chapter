import io
import os
import struct
import zipfile

import requests


def load_sentiment():
    if not os.path.exists("Sentiment_Analysis/"):
        os.mkdir("Sentiment_Analysis/")
    print("[INFO] Downloading")
    url = r"https://github.com/messi313/Omdena-Dataset/raw/main/Omdena-seniment-analysis-Datasets.zip"
    r = requests.get(url)
    local_filename = "Sentiment_Analysis/Omdena-seniment-analysis-Datasets.zip"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            f.write(r.content)
    print("[INFO] Extracting")
    z = zipfile.ZipFile("Sentiment_Analysis/Omdena-seniment-analysis-Datasets.zip")
    z.extractall("Sentiment_Analysis/")
    print("[INFO] Done")
    #os.remove("Sentiment_Analysis/Omdena-seniment-analysis-Datasets.zip")

def load_ner():
    if not os.path.exists("Entity_Recognition/"):
        os.mkdir("Entity_Recognition/")
    print("[INFO] Downloading")
    url = r"https://github.com/messi313/Omdena-Dataset/raw/main/NER_data_spacy.json"
    r = requests.get(url)
    local_filename = "Entity_Recognition/NER_data_spacy.json"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            f.write(r.content)
    print("[INFO] Done")

def load_dialect():
    if not os.path.exists("dialect/"):
        os.mkdir("dialect/")
    print("[INFO] Downloading")
    url = r"https://github.com/messi313/Omdena-Dataset/raw/main/Final_Dialect_Dataset.zip"
    r = requests.get(url)
    local_filename = r"dialect/Final_Dialect_Dataset.zip"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            f.write(r.content)
    print("[INFO] Extracting")
    z = zipfile.ZipFile("dialect/Final_Dialect_Dataset.zip")
    z.extractall("dialect/")
    #os.remove("dialect/Final_Dialect_Dataset.zip")
    print("[INFO] Done")
    
def load_word_embedding():
    if not os.path.exists("Word_Embedding/"):
        os.mkdir("Word_Embedding/")
    print("[INFO] Downloading")
    url = r"https://github.com/messi313/Omdena-Dataset/raw/main/Word%20Embedding.zip"
    r = requests.get(url)
    local_filename = r"Word_Embedding/Word Embedding.zip"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            f.write(r.content)
    print("[INFO] Extracting")
    z = zipfile.ZipFile("Word_Embedding/Word Embedding.zip")
    z.extractall("Word_Embedding/")
    #os.remove("Word_Embedding/Word Embedding.zip")
    print("[INFO] Done")

def load_pos():
    if not os.path.exists("Parts_of_speech/"):
        os.mkdir("Parts_of_speech/")
    print("[INFO] Downloading")
    url = r"https://github.com/messi313/Omdena-Dataset/raw/main/Final_Pos.zip"
    r = requests.get(url)
    local_filename = r"Parts_of_speech/Final_Pos.zip"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            f.write(r.content)
    print("[INFO] Extracting")
    z = zipfile.ZipFile("Parts_of_speech/Final_Pos.zip")
    z.extractall("Parts_of_speech/")
    #os.remove("Parts_of_speech/pos_data.zip")
    print("[INFO] Done")

def load_morphology():
    if not os.path.exists("Morphology/"):
        os.mkdir("Morphology/")
    print("[INFO] Downloading")
    url = r"https://github.com/messi313/Omdena-Dataset/raw/main/final_morpho_data.zip"
    r = requests.get(url)
    local_filename = r"Morphology/final_morpho_data.zip"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            f.write(r.content)
    print("[INFO] Extracting")
    z = zipfile.ZipFile("Morphology/final_morpho_data.zip")
    z.extractall("Morphology/")
    #os.remove("Morphology/final_morpho_data.zip")
    print("[INFO] Done")
