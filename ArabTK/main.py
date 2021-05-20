from utils import tokenize




if __name__ == '__main__':
    text = " عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضًا بروح الإخاء."
    # text = text.decode('utf-8')

    #Class Initialization
    # available methods : reg_exp, keras, word_punkt, tree_bank, default : word_tokenize 
    tokenizer = tokenize.ArabicTokenizer(word_method="reg_exp")

    #Sentence tokenization, Not necessary!
    text = tokenizer.sentence_tokenize(text)
    print(len(text))
    print(text)

    #Word tokenizer to split sentences or paragraphs to tokens
    words = []
    for i in text:
        words.extend(tokenizer.word_tokenize(i))
    print(words)
