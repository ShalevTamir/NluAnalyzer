import nltk
from nltk import word_tokenize, WordNetLemmatizer

from models.enums.adjective_group import AdjectiveGroup
from models.word_pos_tag import WordPosTag
from services.classification.comparative_adjectives_classification.adjective_classifier import AdjectiveClassifier


class AdjectiveHandler:
    ADJECTIVE_POS_TAG = "JJR"

    def __init__(self,adjective_classifier: AdjectiveClassifier):
        self._lemmatizer = WordNetLemmatizer()
        self._classifier = adjective_classifier

    def extract_adjectives(self, sentence):
        """extracts the adjectives and lemmatizes them"""
        words_in_string: list[str] = word_tokenize(sentence)
        word_pos_tags: list[WordPosTag] = [WordPosTag(word=pos_tag[0], pos_tag=pos_tag[1])
                                           for pos_tag in nltk.pos_tag(words_in_string)]
        return [self._lemmatizer.lemmatize(word_pos_tag.word, pos="a")
                for word_pos_tag in word_pos_tags
                if word_pos_tag.pos_tag == self.ADJECTIVE_POS_TAG]

    def extract_range(self, quantitative_adj, number_compared):
        adjective_group = self._classifier.classify_word(quantitative_adj)
        match adjective_group:
            case AdjectiveGroup.INCREASED:
                return [number_compared, float("inf")]
            case AdjectiveGroup.DECREASED:
                return [-float("inf"), number_compared]
