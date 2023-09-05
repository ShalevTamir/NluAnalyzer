import nltk
from nltk import word_tokenize, WordNetLemmatizer


class RangeAnalyzer:
    def _extract_parameter(self, pos_tags_lst):
        nouns = []
        for pos_tag in pos_tags_lst:
            if pos_tag[1] == 'NN' and pos_tag[0].lower() != 'parameter':
                nouns.append(pos_tag)
        return nouns[0][0]



    def extract_range(self, str_to_analyze):
        words_in_string = word_tokenize(str_to_analyze)
        pos_tags = nltk.pos_tag(words_in_string)
        return self._extract_parameter(pos_tags)
