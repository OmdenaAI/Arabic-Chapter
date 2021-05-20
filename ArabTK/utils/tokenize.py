import nltk.data
from nltk.tokenize import sent_tokenize, word_tokenize, TreebankWordTokenizer, WordPunctTokenizer, RegexpTokenizer
from tensorflow.keras.preprocessing.text import text_to_word_sequence

class ArabicTokenizer:
    def __init__(self, word_method="default"):
        self.word_method = word_method

    def sentence_tokenize(self, text):
        text = sent_tokenize(text)
        return text

    def word_tokenize(self, text):
        if(self.word_method == "tree_bank"):
            tokenizer = TreebankWordTokenizer()
            text = tokenizer.tokenize(text)
            return text

        elif(self.word_method == "word_punkt"):
            tokenizer = WordPunctTokenizer()
            text = tokenizer.tokenize(text)
            return text

        elif(self.word_method == "reg_exp"):
            tokenizer = RegexpTokenizer("[\w']+")
            text = tokenizer.tokenize(text)
            return text

        elif(self.word_method == "keras"):
            return text_to_word_sequence(text)

        else:
            return word_tokenize(text)

