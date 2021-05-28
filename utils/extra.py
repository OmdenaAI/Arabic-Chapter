#Inherited from Ahmed Salah
class Sentencizer:
    """"
    Class for splitting paragraphs to sentences
    """

    def __init__(self, _text, split_chars=['.', '?', '؟', '!', ':']):
        self.sentences = []
        self.text = str(_text)
        self._split_chars = split_chars
        self._sentencize()

    def _sentencize(self):

        """"
        Split sentences according to the split chars we have
        and also handle some special cases for them
        """
        fullStopIndex = findOccurrences(self.text, '.')  # get the indices of all occurrences of (.) to check
        text = self.text
        text = fullStopCheck(text, fullStopIndex)
        for character in self._split_chars:
            text = text.replace(character, character + "</>")
        text = text.replace('<D>', '.')
        self.sentences = [x.strip() for x in text.split("</>") if x != '']

class tokenization:
    """"
    CLass to create tokens from sentences
    """
    def __init__(self, sentences, split_tokens=[' ', '-']):

        self.tokens = []
        self.sentences = Sentencizer(sentences).sentences
        self._split_tokens = split_tokens
        self._punctuations = """'!"#$%&'()*+,«».؛،/:؟?@[\]^_`{|}~"""
        self._tokenize()

    def _tokenize(self):
        """"
         return tokens from the given sentences
        """
        for text in self.sentences:

            for punctuation in self._punctuations:      # Search for the punctuations inside the sentence
                text = text.replace(punctuation, " " + punctuation + " ")

            for delimiter in self._split_tokens:
                text = text.replace(delimiter, '</>')

            token = [x.strip() for x in text.split('</>') if x != '']
            token = [x for x in token if x not in self._punctuations]
            self.tokens.append(list(set(token)))


def findOccurrences(s, ch):

    """"
     Finds all occurrences of a char and returns all indices
    """
    return [i for i, letter in enumerate(s) if letter == ch]


def fullStopCheck(text, indices):
    """"
    Check for all the cases were the full stop doesn't mean the end of the sentence
    example : (ق.م), (أ.د.سعيد), (د.توفيق)
    """
    for index in indices:
        if text[index - 2] == ' ' or index - 1 == 0 or text[index - 2] == '.':
            if text[index - 1] == '.': text = text[0:index] + text[index + 1:]
            else:
              text = text[0:index] + '<D>' + text[index + 1:]

    return text