from functools import partial
from models.enums.sentence_group import SentenceGroup
from models.requirement_param import RequirementParam
from models.sensor import Sensor
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from services.classification.preprocessing.preprocessor import remove_punctuation_marks
from services.subject_detector import SubjectDetector
from services.text_partitioner import TextPartitioner
from services.utils.str_utils import extract_numbers


class TextParser:
    def __init__(self,
                 subject_detector: SubjectDetector,
                 sentence_classifier: SentenceClassifier,
                 range_handler_factory,
                 text_partitioner: TextPartitioner):
        self.__param_detector = subject_detector
        self.__sentence_classifier = sentence_classifier
        self.__range_handler_factory = range_handler_factory
        self.__text_partitioner = text_partitioner

    def __parse_range(self, sentence) -> RequirementParam:
        return self.__range_handler_factory(sentence).parse_sentence()

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
