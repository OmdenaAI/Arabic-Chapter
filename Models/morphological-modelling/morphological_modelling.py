from morphological_analysis.data.roots import raw_roots
from morphological_analysis.data.affixes import VERB_SUFFIX_LIST, VERB_PREFIX_LIST, NOUN_SUFFIX_LIST, NOUN_PREFIX_LIST, \
    VERB_AFFIX_LIST, NOUN_AFFIX_LIST, STEMMING_SUFFIX_LIST, STEMMING_PREFIX_LIST


class Morphology:
    root = list(raw_roots)
    verb_prefix = list(VERB_PREFIX_LIST)
    verb_suffix = list(VERB_SUFFIX_LIST)
    noun_prefix = list(NOUN_PREFIX_LIST)
    noun_suffix = list(NOUN_SUFFIX_LIST)
    prefix = list(STEMMING_PREFIX_LIST)
    suffix = list(STEMMING_SUFFIX_LIST)

    # def __init__(self, root, verb_prefix, verb_suffix, noun_prefix, noun_suffix):
    #     self.root = list(raw_roots)
    #     self.verb_prefix = list(VERB_PREFIX_LIST)
    #     self.verb_suffix = list(VERB_SUFFIX_LIST)
    #     self.noun_prefix = list(NOUN_PREFIX_LIST)
    #     self.noun_suffix = list(NOUN_SUFFIX_LIST)

    @staticmethod
    def get_prefix(word, type_word):

        """
        This function returns the prefix of the word or verb provided.
        :param type_word: Whether a word is a noun or a verb
        :param word: The word or verb we want to analyze.
        :return: The prefix and the word or verb separately.
        """

        # prefix = (lambda x: pre_list[x] == )
        # if word.startswith(lambda x: pre_list[x]):
        #     print('Success!')
        # else:
        #     print('Fail!')
        # prefix = lambda x: re.search(r'^ x', word)
        # print(prefix)

        pref_list = []
        # if type_word == 'noun':
        #     for seq in Morphology.noun_prefix:
        #         if word.startswith(seq):
        #             pref_list.append(seq)
        #
        # elif type_word == 'verb':
        #     for seq in Morphology.verb_prefix:
        #         if word.startswith(seq):
        #             pref_list.append(seq)
        # else:
        #     return
        for seq in Morphology.prefix:
            if word.startswith(seq):
                pref_list.append(seq)

        if len(pref_list) == 0:
            return '', word

        longest_seq = max(pref_list, key=len)
        return longest_seq, word.lstrip(longest_seq)


    @staticmethod
    def get_suffix(word, type_word):

        """
        This function returns the suffix of the word or verb provided.
        :param type_word: type_word: Whether a word is a noun or a verb
        :param word: The word or verb we want to analyze.
        :return: The suffix and the word or verb separately.
        """

        suf_list = []
        if type_word == 'noun':
            for seq in Morphology.noun_suffix:
                if word.endswith(seq):
                    suf_list.append(seq)

        elif type_word == 'verb':
            for seq in Morphology.verb_suffix:
                if word.endswith(seq):
                    suf_list.append(seq)

        else:
            return

        if len(suf_list) == 0:
            return '', word

        longest_seq = max(suf_list, key=len)
        return longest_seq, word.rstrip(longest_seq)


    # @staticmethod
    # def get_root(word):


    @staticmethod
    def word_morphology(word, type_word):

        """
        This function returns the analysis of the word or verb provided.
        :param type_word: type_word: Whether a word is a noun or a verb
        :param word: The word or verb we want to analyze.
        :return: The analysis of the word or verb.
        """

        prefix, word_suf = Morphology.get_prefix(word, type_word)
        suffix, base_word = Morphology.get_suffix(word_suf, type_word)
        # print(prefix + ' + ' + base_word + ' + ' + suffix)
        return prefix + ' + ' + base_word + ' + ' + suffix
        # print(get_prefix(word) + get_root(word) + get_suffix(word))

