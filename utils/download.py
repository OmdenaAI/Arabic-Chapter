#!/usr/bin/env python
import os
from zipfile import ZipFile

import gdown


def download():
    #mottagah
    if not os.path.exists("models/mottagah_large_wv.wordvectors"):
        url = "https://drive.google.com/uc?id=1oT8XW02IjMEuJRqYscSVrQTPi-f8pf8M"
        output = "models/mottagah.zip"
        gdown.download(url, output)
        print("Model Downloaded")
        with ZipFile(output, 'r') as zipf:
            zipf.extractall("models/")
        os.remove(output)
        print("Model Unzipped ")

    #aravec
    if not os.path.exists("models/aravec/Twitter_CBOW_100.wordvectors"):
        url = "https://drive.google.com/uc?id=1hG74OpB9XeQZxMh6MYlyfXIM5CuN_Dus"
        output = "models/aravec.zip"
        gdown.download(url, output)
        print("Model Downloaded")
        with ZipFile(output, 'r') as zipf:
            zipf.extractall("models/")
        os.remove(output)
        print("Model Unzipped ")