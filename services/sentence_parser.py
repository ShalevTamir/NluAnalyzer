import re

from services.classification.adjective_handler import AdjectiveHandler
from services.subject_detector import SubjectDetector
from services.utils.str_utils import is_castable


class SentenceParser:
    NUMERICAL_POS_TAG = "CD"
    FIND_NUMBERS_REG = r'\d+(?:\.\d+)?'

    def __init__(self, subject_detector: SubjectDetector, adjective_handler: AdjectiveHandler):
        self.__param_detector = subject_detector
        self.__adjective_handler = adjective_handler

    def _extract_parameter_name(self, sentence: str):
        return self.__param_detector.detect(sentence)

    def _build_range(self, parameter, numbers):
        print(parameter, numbers)

    def _extract_numbers(self, sentence):
        return [int(number) if is_castable(number, int) else float(number)
                for number in re.findall(self.FIND_NUMBERS_REG, sentence)]

    def parse(self, sentence: str):
        quantitative_adjs = self.__adjective_handler.extract_adjectives(sentence)
        numbers = self._extract_numbers(sentence.replace(',', ''))
        parameter_name = self._extract_parameter_name(sentence)
        # TODO: smaller then 100 and bigger than 120
        # TODO: alert for this
        # TODO: validate the range

