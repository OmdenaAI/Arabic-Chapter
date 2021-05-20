from utils import tokenize
from utils import stop_words




if __name__ == '__main__':
    text = " عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضًا بروح الإخاء."
    #text = "Hello all, It's Suriya. How are you all?"
    text.decode(encoding='utf-8')

    #Class Initialization
    # available methods : reg_exp, keras, word_punkt, tree_bank, default : word_tokenize 
    tokenizer = tokenize.ArabicTokenizer(word_method="word_punkt")

    #Sentence tokenization, Not necessary!
    text = tokenizer.sentence_tokenize(text)
    print(len(text))
    print(text)

    #Word tokenizer to split sentences or paragraphs to tokens
    text = tokenizer.word_tokenize(text)
    print(len(text))
    print(text)

    #to remove basic un wanted words, feel free to add stop words corpus in the data\Stop_words folder
    text = stop_words.remove_stop_words(text)
    print(len(text))
    print(text)