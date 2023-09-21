import re

from models.enums.sentence_group import SentenceGroup
from models.requirement_param import RequirementParam
from models.requirement_range import RequirementRange
from models.sensor import Sensor
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from services.classification.preprocessing.preprocessor import preprocess_sentence,remove_punctuation_marks
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

    def parse(self, sentence: str) -> Sensor:
        sentence = remove_punctuation_marks(sentence)
        parameter_name = self.__param_detector.detect(sentence)
        sentence_type: SentenceGroup = self.__sentence_classifier.classify_item(sentence)
        word_pos_tags = extract_word_pos_tags(sentence)
        match sentence_type:
            case SentenceGroup.RANGE:
                return Sensor(parameter_name,
                              self.__range_handler.parse_sentence(word_pos_tags))
            case SentenceGroup.PARAMETER:
                return Sensor(parameter_name, RequirementParam(self.__extract_numbers(sentence)[0]))


