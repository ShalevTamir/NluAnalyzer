import re
from functools import partial
from typing import Generator

from nltk import pos_tag, word_tokenize

from definitions import FIND_NUMBERS_REG, RANGE_NUMBERS_COUNT, PARAMETER_NUMBERS_COUNT
from models.enums.sentence_group import SentenceGroup
from models.requirement_param import RequirementParam
from models.requirement_range import RequirementRange
from models.sensor import Sensor
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from services.classification.preprocessing.preprocessor import remove_punctuation_marks
from services.range_handler import RangeHandler
from services.subject_detector import SubjectDetector
from services.text_partitioner import TextPartitioner
from services.utils.nltk_utils import extract_word_pos_tags
from services.utils.str_utils import is_castable, parse_number, extract_numbers


class TextParser:
    def __init__(self,
                 subject_detector: SubjectDetector,
                 sentence_classifier: SentenceClassifier,
                 range_handler: RangeHandler,
                 text_partitioner: TextPartitioner):
        self.__param_detector = subject_detector
        self.__sentence_classifier = sentence_classifier
        self.__range_handler = range_handler
        self.__text_partitioner = text_partitioner

    def __build_range(self, parameter: str, requirement_range: RequirementRange):
        print(parameter, [requirement_range.value, requirement_range.end_value])

    def __build_parameter(self, parameter_name: str, correlated_number: int):
        print(parameter_name, correlated_number)

    def __parse_range(self, sentence) -> RequirementParam:
        return self.__range_handler.parse_sentence(extract_word_pos_tags(sentence))

    def __parse_parameter(self, sentence) -> RequirementParam:
        numbers_in_sentence = extract_numbers(sentence)
        if numbers_in_sentence:
            return RequirementParam(numbers_in_sentence[0])

    def __parse_sentence_by_type(self, sentence: str, sentence_type: SentenceGroup) \
            -> RequirementParam:
        return self.__parse_range(sentence) \
            if sentence_type == SentenceGroup.RANGE \
            else self.__parse_parameter(sentence)


    def parse(self, text: str):
        sentence = remove_punctuation_marks(text)
        parameter_name = self.__param_detector.detect(sentence)
        sentence_type: SentenceGroup = self.__sentence_classifier.classify_item(sentence)
        # containing the methods used to parse and their arguments
        parsing_options = [partial(self.__parse_sentence_by_type, sentence, sentence_type),
                           partial(self.__parse_sentence_by_type, sentence, SentenceGroup(1 - sentence_type.value))]
        for parsing_option in parsing_options:
            requirement_param: RequirementParam = parsing_option()
            if requirement_param:
                return Sensor(parameter_name, requirement_param)
