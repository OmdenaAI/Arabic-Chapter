# Yarub
###### This is a head start to Modern  standard arabic training dataset library which provides Morphological, Named Entity recognization, Sentiment Analysis, Word Embedding, Dialect Identification,Part of speech and so on training dataset.




# Downloading the library with specific version using pip command.

`pip install yarub==0.1.0`


# Basic Instruction

- You need to first install dependent libraries before download like `requests`, `zipfile`,`os`, `io` and `struct`.
- After successful installation of dependent library you can install `Yarub` library with pip command.



# Example of  `Yarub`

```
import yarub  # Load Library package
from yarub import load_sentiment,load_ner,load_dialect,load_word_embedding,load_morphology,load_pos

```
# OR

```
from yarub import *    # Second method to call library and load entire function.

```

# Load the dataset in your local system.

```

df = load_sentiment()   # This function wil load `Sentiment analysis` training dataset

df1 = load_ner()     	# This function will load `Named entity recognization` training dataset.

df2 = load_dialect()     # This function will load modern standard arabic `Dialect identification` training dataset.

df3 = load_word_embedding()   # This function will load `Word embedding` training dataset.

df4 = load_morphology()       # This function will load  `Morphological analysis` training dataset.

df5 = load_pos()             # This function will load `Part of speech` training dataset.

```


