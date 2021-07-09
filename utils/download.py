import os
from zipfile import ZipFile

import gdown


def download():
    #pos
    if not os.path.exists("models/pos/pytorch_model.bin"):
        if not os.path.exists("models/pos/"):
            os.mkdir("models/pos/")
        url = "https://drive.google.com/uc?id=12DKOHvJGS6lwbvrsevcKGBIxBANo4y3D"
        output = "models/pos/pos.zip"
        gdown.download(url, output)
        print("Model Downloaded")
        with ZipFile(output, 'r') as zipf:
            zipf.extractall("models/pos/")
        os.remove(output)
        print("Model Unzipped ")

    #gender
    if not os.path.exists("models/gender/pytorch_model.bin"):
        if not os.path.exists("models/gender/"):
            os.mkdir("models/gender/")
        url = "https://drive.google.com/uc?id=1wgWKPd4NcOFiuLdVIPRDTBwyt5Twogrx"
        output = "models/gender/gender.zip"
        gdown.download(url, output)
        print("Model Downloaded")
        with ZipFile(output, 'r') as zipf:
            zipf.extractall("models/gender/")
        os.remove(output)
        print("Model Unzipped ")
