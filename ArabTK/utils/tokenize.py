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
            words = []
            tokenizer = TreebankWordTokenizer()
            for i in text:
                words.extend(tokenizer.tokenize(i))
            return words

        elif(self.word_method == "word_punkt"):
            words = []
            tokenizer = WordPunctTokenizer()
            for i in text:
                words.extend(tokenizer.tokenize(i))
            return words

        elif(self.word_method == "reg_exp"):
            words = []
            tokenizer = RegexpTokenizer("[\w']+")
            for i in text:
                words.extend(tokenizer.tokenize(i))
            return words

        elif(self.word_method == "keras"):
            words = []
            for i in text:
                words.extend(text_to_word_sequence(i))
            return words

        else:
            words = []
            for i in text:
                words.extend(text_to_word_sequence(i))
            return words

