from data.ar_stopwords import ar_stopwords
from data.stopwordsallforms import STOPWORDS
from data.statmodelresults import stat_stop_words


class stopwords:

    stopwords_long = list(STOPWORDS.keys())
    stopwords_short = list(ar_stopwords)
    stopwords_stat = list(stat_stop_words)

    def remove_stopwords(text,sw_src='stopwords_long'):
    
        """
        This function takes in a string and returns a list of words that are not stopwords.
        
        INPUT:
        text: String that you want to remove stopwords from.
        sw_src: stands for stopword source (default = stopwords_long)
        possible values for sw_src = {'stopwords_long','stopwords_short','stopwords_stat'}
        
        OUTPUT:
        list of tokens free of stopwords
        """

        if sw_src.lower() == 'stopwords_long':
            sw_set = stopwords.stopwords_long
        elif sw_src.lower() == 'stopwords_short':
            sw_set = stopwords.stopwords_short
        elif sw_src.lower() == 'stopwords_stat':
            sw_set = stopwords.stopwords_stat
        else:
            return 'Invalid stop word source'
        
        result_list = []
        for token in text.split():
            if token not in sw_set:
                result_list.append(token)
        return result_list
        
    def show_stop_word_list(sw_src='stopwords_long'):
    
        """
        This function takes in a stopword source and returns available list of stopwords.
        
        INPUT:
        sw_src: stands for stopword source (default = stopwords_long)
        possible values for sw_src = {'stopwords_long','stopwords_short','stopwords_stat'}
        
        OUTPUT:
        list of stopwords from selected source
        """
    
        if sw_src.lower() == 'stopwords_long':
            return stopwords.stopwords_long
        elif sw_src.lower() == 'stopwords_short':
            return stopwords.stopwords_short
        elif sw_src.lower() == 'stopwords_stat':
            return stopwords.stopwords_stat
        else:
            return 'Invalid stop word source'
            
            
    def is_stop_word(word,sw_src='stopwords_long'):
    
        """
        This function takes in a string and returns whether it is a stopword or not
        
        INPUT:
        word: String that you want to test.
        sw_src: stands for stopword source (default = stopwords_long)
        possible values for sw_src = {'stopwords_long','stopwords_short','stopwords_stat'}
        
        OUTPUT:
        True if stop word , False otherwise
        """
    
        if sw_src.lower() == 'stopwords_long':
            return word in stopwords.stopwords_long
        elif sw_src.lower() == 'stopwords_short':
            return word in stopwords.stopwords_short
        elif sw_src.lower() == 'stopwords_stat':
            return word in stopwords.stopwords_stat
        else:
            return 'Invalid stop word source'


    def add_stopword(word,to='stopwords_long'):
    
        """
        This function takes in a string and adds it to selected stopword destination.
        
        INPUT:
        word: String that you want to remove stopwords from.
        to: stands for stopword destination (default = stopwords_long)
        possible values for to = {'stopwords_long','stopwords_short','stopwords_stat'}
        
        OUTPUT:
        None
        """
    
        if to.lower() == 'stopwords_long':
            stopwords.stopwords_long.append(word)
        elif to.lower() == 'stopwords_short':
            stopwords.stopwords_short.append(word)
        elif to.lower() == 'stopwords_stat':
            stopwords.stopwords_stat.append(word)
        else:
            return 'Invalid stop word destination'
