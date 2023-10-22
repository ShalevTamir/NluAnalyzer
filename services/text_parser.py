import json
from functools import partial
from typing import Tuple

from flask_app.services.json.custom_encoder import CustomEncoder
from models.enums.parse_status import ParseStatus
from models.enums.sentence_group import SentenceGroup
from models.requirement_param import RequirementParam
from models.sensor import Sensor
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from services.classification.preprocessing.preprocessor import remove_punctuation_marks
from services.range_handler import RangeHandler
from services.subject_detector import SubjectDetector
from services.text_partitioner import TextPartitioner
from services.utils.str_utils import extract_numbers


class TextParser:
    def __init__(self,
                 subject_detector: SubjectDetector,
                 sentence_classifier: SentenceClassifier,
                 range_handler_factory,
                 text_partitioner: TextPartitioner):
        self._param_detector = subject_detector
        self._sentence_classifier = sentence_classifier
        self._range_handler_factory = range_handler_factory
        self._text_partitioner = text_partitioner

    def _parse_range(self, sentence) -> Tuple[RequirementParam, ParseStatus]:
        range_handler: RangeHandler = self._range_handler_factory(sentence)
        range_handler.parse_sentence()
        return range_handler.get_range(), range_handler.get_parse_status()

    def _parse_parameter(self, sentence) -> Tuple[RequirementParam, ParseStatus]:
        numbers_in_sentence = extract_numbers(sentence)
        if numbers_in_sentence:
            return RequirementParam(numbers_in_sentence[0]), ParseStatus.SUCCESSFUL

    def _parse_sentence_by_type(self, sentence: str, sentence_type: SentenceGroup) \
            -> Tuple[RequirementParam, ParseStatus]:
        return self._parse_range(sentence) \
            if sentence_type == SentenceGroup.RANGE \
            else self._parse_parameter(sentence)

    def parse(self, text: str):
        sentence = remove_punctuation_marks(text)
        parameter_name = self._param_detector.detect(sentence)
        sentence_type: SentenceGroup = self._sentence_classifier.classify_item(sentence)
        # containing the methods used to parse and their arguments
        parsing_options = [partial(self._parse_sentence_by_type, sentence, sentence_type),
                           partial(self._parse_sentence_by_type, sentence, SentenceGroup(1 - sentence_type.value))]
        for parsing_option in parsing_options:
            requirement_param, parse_status = parsing_option()
            if parse_status == ParseStatus.SUCCESSFUL:
                return Sensor(parameter_name, requirement_param)
            elif parse_status == ParseStatus.INVALID_RANGE:
                raise ValueError(f"Invalid range for sentence {sentence}, "
                                 f"parsed {json.dumps(Sensor(parameter_name, requirement_param), cls=CustomEncoder)}")
            elif parse_status == ParseStatus.UNABLE_TO_PARSE:
                raise ValueError(f"Unable to parse sentence {sentence}")
