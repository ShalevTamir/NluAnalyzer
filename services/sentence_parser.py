import re

import nltk
from nltk import word_tokenize

from models.enums.sentence_group import SentenceGroup
from models.requirement_range import RequirementRange
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from services.classification.preprocessing.preprocessor import preprocess_sentence
from services.range_handler import RangeHandler
from services.subject_detector import SubjectDetector
from services.utils.nltk_utils import extract_word_pos_tags
from services.utils.str_utils import is_castable

ERROR_MSG = "Unable to parse sentence"


class SentenceParser:
    FIND_NUMBERS_REG = r'\d+(?:\.\d+)?'

    def __init__(self,
                 subject_detector: SubjectDetector,
                 sentence_classifier: SentenceClassifier,
                 range_handler: RangeHandler):
        self.__param_detector = subject_detector
        self.__sentence_classifier = sentence_classifier
        self.__range_handler = range_handler

    def __build_range(self, parameter: str, requirement_range: RequirementRange):
        print(parameter, [requirement_range.value, requirement_range.end_value])

    def __extract_numbers(self, sentence):
        return [int(number) if is_castable(number, int) else float(number)
                for number in re.findall(self.FIND_NUMBERS_REG, sentence)]

    def parse(self, sentence: str):
        sentence = preprocess_sentence(sentence)
        parameter_name = self.__param_detector.detect(sentence)
        sentence_type: SentenceGroup = self.__sentence_classifier.classify_item(sentence)
        match sentence_type:
            case SentenceGroup.RANGE:
                self.__build_range(parameter_name,
                                   self.__range_handler.process_range(extract_word_pos_tags(sentence)))
            case SentenceGroup.PARAMETER:
                pass

        # TODO: smaller then 100 and bigger than 120
        # TODO: alert for this
        # TODO: validate the range
