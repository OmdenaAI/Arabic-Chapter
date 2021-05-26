from data.ar_stopwords import ar_stopwords
from data.stopwordsallforms import STOPWORDS


def remove_stopwords(text,sw_src='STOPWORDS'):
    """
    This function takes in a string and returns a list of words that are not stopwords
    
    INPUT:
    text: String that you want to remove stopwords from.
    sw_src: stands for stopword source (default = STOPWORDS)
    
    OUTPUT:
    list of tokens free of stopwords
    """

    if sw_src.lower() == 'stopwords':
        sw_set = set(STOPWORDS.keys())
    elif sw_src.lower() == 'ar_stopwords':
        sw_set = ar_stopwords
    else:
        return 'Invalid stop word source'
    
    result_list = []
    for token in text.split():
        if token not in sw_set:
            result_list.append(token)
    return result_list

## IN PROGRESS
def add_stopword(word,to='STOPWORDS'):
    if to.lower() == 'stopwords':
        STOPWORDS[word]=""
    elif to.lower() == 'ar_stopwords':
        ar_stopwords.add(word)
    else:
        return 'Invalid stop word destination'
