import re
from tqdm.notebook import tqdm

from utils.config import config


#helper method to clean the text and convert it as tokens
def tokenizer(
    texts:list,
    punctuations = config['punctuations'],
    stop_words=config['stop_words']
    )->list:
    """
    helper function to tokenize texts
    params:
    texts: list of texts
    punctuations: punctuations string
    stop_words: list of stop words
    retuns:
    tokenized texts
    """

    list_ = []
    maxlen = 0
    vocab = 0
    # traversing the all the texts
    for i in tqdm(range(len(texts)), total=len(texts)):
        for x in texts[i]:
           if x in punctuations:

               #replacing punctuations with space
               texts[i] = texts[i].replace(x, " ")

        # removing all the non-aschii characters
        texts[i] = re.sub(r'<.*?>', '', texts[i])
        texts[i] = re.sub(r'\w*\d\w*', '', texts[i])
        texts[i] = re.sub(r'[0-9]+', '', texts[i])
        texts[i] = re.sub(r'\s+', ' ', texts[i]).strip()

        #splitting the words and removing words in the stopwords list
        texts[i] = texts[i].split(' ')
        texts[i] = [x for x in texts[i] if x!='']
        texts[i] = [x for x in texts[i] if x not in punctuations]
        texts[i] = [x for x in texts[i] if x not in stop_words]
        list_.append(texts[i])

        maxlen = len(texts[i]) if len(texts[i]) > maxlen else maxlen
        for i in texts[i]:
            vocab += 1
                
    return list_, maxlen, vocab

    
