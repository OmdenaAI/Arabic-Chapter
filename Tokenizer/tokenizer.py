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
        text = text.replace('§', '.')
        self.sentences = [x.strip() for x in text.split("</>") if x != '']


class tokenization:
    """"
    CLass to create tokens from sentences
    """

    def __init__(self, text, split_tokens=[' ', '-']):

        self.tokens = []
        # Separate text into paragraphs at first
        self.paragraphs = ' '.join([prop_paragraph for prop_paragraph in text.split('\n') if len(prop_paragraph) > 1])
        self.sentences = Sentencizer(self.paragraphs).sentences
        self._split_tokens = split_tokens
        self._punctuations = """'!"#$%&'()*+,«».؛،/:؟?@[\]^_`{|}~”“"""
        self._tokenize()

    def _tokenize(self):
        """"
         return tokens from the given sentences
        """
        for text in self.sentences:

            for punctuation in self._punctuations:  # Search for the punctuations inside the sentence
                text = text.replace(punctuation, " " + punctuation + " ")

            for delimiter in self._split_tokens:
                text = text.replace(delimiter, '</>')

            token = [x.strip() for x in text.split('</>') if x != '' and (x not in self._punctuations)]
            self.tokens.append(token)


def findOccurrences(s, ch):
    """"
     Finds all occurrences of a char and returns all indices
    """
    return [i for i, letter in enumerate(s) if letter == ch]


def fullStopCheck(text, indices):
    """"
    Check for all the cases where the full stop doesn't mean the end of the sentence
    example : (ق.م), (أ.د.سعيد), (٩.٢٩ مليون)
    """
    if 1 in indices and len(text) > 2:
        text = text[0:1] + '§' + text[2:]
        indices.remove(1)

    for i in indices:
        if i < len(text) - 1:
            if (text[i - 1].isnumeric() and text[i + 1].isnumeric() or
                    text[i - 2] == ' ' or text[i - 2] == '.'):
                text = text[0:i] + '§' + text[i + 1:]

    return text
