import glob
import json
from tqdm import tqdm
import pandas as pd

input_ = ["NER/input/apprentissage_ne/", "NER/input/test_ne/"]

all_text = dict()

for folder in input_:
    for file in tqdm(glob.glob(folder + "*.txt"), total=len(glob.glob(folder + "*.txt"))):
        f = open(file, "r", encoding='utf-8')
        for i in f:
            label, text = i.strip().split(':')
            all_text[text.strip()] = label
#df = pd.DataFrame(all_text, columns=["text", "label"], index=[0])
#df.to_csv("all.csv")

with open('NER/input/data.json', 'w') as fp:
    json.dump(all_text, fp)