import re

from models.enums.sentence_group import SentenceGroup
from models.requirement_param import RequirementParam
from models.requirement_range import RequirementRange
from models.sensor import Sensor
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from services.classification.preprocessing.preprocessor import  remove_punctuation_marks
from services.range_handler import RangeHandler
from services.subject_detector import SubjectDetector
from services.utils.nltk_utils import extract_word_pos_tags
from services.utils.str_utils import is_castable


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

    def __build_parameter(self, parameter_name: str, correlated_number: int):
        print(parameter_name, correlated_number)

    def __extract_numbers(self, sentence):
        return [int(number) if is_castable(number, int) else float(number)
                for number in re.findall(self.FIND_NUMBERS_REG, sentence)]

    def __parse_range(self, sentence) -> RequirementParam | None:
        return self.__range_handler.parse_sentence(extract_word_pos_tags(sentence))

    def __parse_parameter(self, sentence) -> RequirementParam | None:
        numbers_in_sentence = self.__extract_numbers(sentence)
        if len(numbers_in_sentence) != 1:
            return None
        else:
            return RequirementParam(self.__extract_numbers(sentence)[0])

    def __parse_sentence_by_type(self, sentence: str,parameter_name: str, sentence_type: SentenceGroup) -> Sensor | None:
        requirement_param: RequirementParam = self.__parse_range(sentence) \
                                              if sentence_type == SentenceGroup.RANGE \
                                              else self.__parse_parameter(sentence)
        if not requirement_param:
            return None
        else:
            return Sensor(parameter_name, requirement_param)

    def parse(self, sentence: str) -> Sensor:
        sentence = remove_punctuation_marks(sentence)
        parameter_name = self.__param_detector.detect(sentence)
        sentence_type: SentenceGroup = self.__sentence_classifier.classify_item(sentence)
        sensor = self.__parse_sentence_by_type(sentence,parameter_name,sentence_type)
        # wrong detection of sentence type
        if not sensor:
            sensor = self.__parse_sentence_by_type(sentence, parameter_name, SentenceGroup(1-sentence_type.value))
        if not sensor:
            raise ValueError(f"Unable to parse sentence {sentence}")

        return sensor
