from collections import namedtuple
from typing import List

import nltk
from nltk import word_tokenize
from numpy import maximum, minimum

from models.enums.adjective_group import AdjectiveGroup
from models.word_pos_tag import WordPosTag
from services.classifier import Classifier
from services.dependency_container import DependencyContainer
from services.subject_detector import SubjectDetector
from nltk.stem import WordNetLemmatizer
from services.str_utils import is_float, remove_punctuation


# TODO: change name because it doesnt have to be a range
class RangeAnalyzer:
    def __init__(self):
        self.param_detector = DependencyContainer.get_instance(SubjectDetector)
        self.classifier = DependencyContainer.get_instance(Classifier)
        self.lemmatizer = WordNetLemmatizer()

    def _extract_parameter_name(self, sentence: str):
        return self.param_detector.detect_param(sentence)

    def _build_range(self, parameter, numbers):
        print(parameter, numbers)

    def _extract_range(self, quantitative_adj, number_compared):
        adjective_group = self.classifier.classify_word(quantitative_adj)
        match adjective_group:
            case AdjectiveGroup.INCREASED:
                return [number_compared, float("inf")]
            case AdjectiveGroup.DECREASED:
                return [-float("inf"), number_compared]

    def parse_sentence(self, str_to_analyze):
        words_in_string: list[str] = word_tokenize(str_to_analyze)
        word_pos_tags: list[WordPosTag] = [WordPosTag(word=pos_tag[0], pos_tag=pos_tag[1])
                                           for pos_tag in nltk.pos_tag(words_in_string)]
        # extracts the adjectives and lemmatizes them
        # TODO: change JJR to const
        quantitative_adjs = [self.lemmatizer.lemmatize(word_pos_tag.word, pos="a")
                             for word_pos_tag in word_pos_tags if word_pos_tag.pos_tag == "JJR"]
        #TODO: change casting to float
        numbers = [float(cleaned_word)
                   for word in words_in_string
                   if is_float((cleaned_word := word.replace(',', '')))]
        parameter_name = self._extract_parameter_name(str_to_analyze)
        # TODO: 1 - individual number, 2 - ...
        # TODO: smaller then 100 and bigger than 120
        # TODO: alert for this
        # TODO: validate the range
        match len(numbers):
            case 2:
                return self._build_range(parameter_name,
                                         [minimum(numbers[0], numbers[1]), maximum(numbers[0], numbers[1])])
            case 1:
                if len(quantitative_adjs) > 0:
                    return self._build_range(parameter_name, self._extract_range(quantitative_adjs[0], numbers[0]))
                else:
                    return self._build_range(parameter_name, numbers[0])
