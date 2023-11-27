import json
from functools import partial

from spacy.tokens import Span, Doc

from deep_translator import GoogleTranslator


from flask_app.nlu_pkg.services.sensor_parsing.duration_handler import DurationHandler
from flask_app.nlu_pkg.services.sensor_parsing.parameter_handler import parse_parameter
from flask_app.services.json.custom_encoder import CustomEncoder
from flask_app.nlu_pkg.models.definitions.spacy_def import SPACY_MODEL, SPAN_SUBJECT_ATTR
from flask_app.nlu_pkg.models.enums.parse_status import ParseStatus
from flask_app.nlu_pkg.models.enums.sentence_group import SentenceGroup
from flask_app.nlu_pkg.models.named_tuples.range_parse import ParseResult
from flask_app.nlu_pkg.models.sensor_dto.sensor import Sensor
from flask_app.nlu_pkg.services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from flask_app.nlu_pkg.services.classification.preprocessing.preprocessor import remove_punctuation_marks
from flask_app.nlu_pkg.services.sensor_parsing.subject_detector import SubjectDetector
from flask_app.nlu_pkg.services.sensor_parsing.text_partitioner import TextPartitioner


class TextParser:
    def __init__(self,
                 sentence_classifier: SentenceClassifier,
                 text_partitioner: TextPartitioner,
                 subject_detector: SubjectDetector,
                 duration_handler: DurationHandler,
                 range_handler_factory):
        self._sentence_classifier = sentence_classifier
        self._text_partitioner = text_partitioner
        self._subject_detector = subject_detector
        self._duration_handler = duration_handler
        self._range_handler_factory = range_handler_factory
        self._translator = GoogleTranslator(source='auto', target='en')

    def _parse_range(self, sentence_tokens: Doc | Span) -> ParseResult:
        return self._range_handler_factory(sentence_tokens).parse_sentence()

    # def _parse_parameter(self, sentence_tokens: Doc | Span) -> ParseResult:
    #     numbers_in_sentence = extract_numbers(sentence_tokens)
    #     if numbers_in_sentence:
    #         return ParseResult([RequirementParam(parse_number(numbers_in_sentence[0]))], ParseStatus.SUCCESSFUL)
    #     else:
    #         return ParseResult([], ParseStatus.UNABLE_TO_PARSE)

    def _parse_sentence_by_type(self, sentence_tokens: Doc | Span, sentence_type: SentenceGroup) \
            -> ParseResult:
        return self._parse_range(sentence_tokens) \
            if sentence_type == SentenceGroup.RANGE \
            else parse_parameter(sentence_tokens)

    def parse(self, text: str):
        text = self._translator.translate(text)
        print(f"TRANSLATED TEXT {text}")
        text = remove_punctuation_marks(text)
        tokens = SPACY_MODEL(text)
        for sentence_tokens in self._text_partitioner.extract_sentences(tokens):
            parameter_name = sentence_tokens._.get(SPAN_SUBJECT_ATTR).text
            sentence_tokens, duration = self._duration_handler.extract_duration(sentence_tokens)
            sentence_tokens = self._text_partitioner.remove_sent_noise(sentence_tokens)
            if not sentence_tokens:
                continue
            sentence_type: SentenceGroup = self._sentence_classifier.classify_item(sentence_tokens.text)
            # containing the methods used to parse and their arguments
            parsing_options = [partial(self._parse_sentence_by_type, sentence_tokens, sentence_type),
                               partial(self._parse_sentence_by_type, sentence_tokens, SentenceGroup(1 - sentence_type.value))]

            for parsing_option in parsing_options:
                parse_result: ParseResult = parsing_option()
                if parse_result.parse_status == ParseStatus.SUCCESSFUL:
                    for requirement in parse_result.requirement:
                        yield Sensor(parameter_name, requirement, duration)
                    break
                elif parse_result.parse_status == ParseStatus.INVALID_RANGE:
                    raise ValueError(f"Invalid range for sentence {sentence_tokens.text}, "
                                     f"parsed {[json.dumps(Sensor(parameter_name, requirement, duration), cls=CustomEncoder) for requirement in parse_result.requirement]}")

            # if parse_result.parse_status == ParseStatus.UNABLE_TO_PARSE:
            #     logging.warning(f"Unable to parse sentence {sentence_tokens.text}")
                # raise ValueError(f"Unable to parse sentence {sentence_tokens}")
