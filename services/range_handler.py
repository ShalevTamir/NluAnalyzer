import re
from functools import partial
from typing import Callable

from numpy import minimum, maximum

from definitions import INVALID_SENT, NUMERICAL_POS_TAG, COMPARATIVE_ADJECTIVE_POS_TAG, ADJECTIVE_OR_NUMERICAL_POS_TAG, \
    CONJUNCTION_POS_TAG, FIND_NUMBERS_REG, RANGE_NUMBERS_COUNT, PARAMETER_NUMBERS_COUNT
from services.utils.nltk_utils import chunk_sentence, revert_word_pos_tags, find_Nth_in_chunk, \
    validate_number_detection, extract_word_pos_tags
from models.relational_bound import RelationalBound
from models.enums.relation_group import RelationGroup
from models.requirement_range import RequirementRange
from models.word_pos_tag import WordPosTag
from services.classification.relational_handler import RelationalHandler
from services.utils.str_utils import is_castable, parse_number, extract_numbers as extract_numbers_str
from services.utils.nltk_utils import extract_numbers as extract_numbers_nltk

IMPLICIT_RANGE_REGEX = r"Chunk: {<" + NUMERICAL_POS_TAG + "><.+><" + NUMERICAL_POS_TAG + ">}"
EXPLICIT_RANGE_REGEX = r"Chunk: {<" + ADJECTIVE_OR_NUMERICAL_POS_TAG + ">}"


class RangeHandler:

    def __init__(self, sentence: str, relational_handler: RelationalHandler):
        self.__relational_handler = relational_handler
        self.__sentence = sentence
        self.__word_pos_tags = extract_word_pos_tags(sentence)
        self.__relational_bounds = None

    def parse_sentence(self) -> RequirementRange:
        validate_number_detection(self.__word_pos_tags)
        parsing_methods = [
            # Parses syntax: Engine heat is between 100 and 200
            self.__process_implicit_range,
            # Parses syntax: Engine heat in range 100-200
            self.__process_explicit_range,
            # Parses syntax: Engine heat is greater than 50
            self.__process_relational_range,
            # Default parse if not parse succeeded
            self.__default_parsing_case
        ]

        for parsing_method in parsing_methods:
            requirement_range = parsing_method()
            if not requirement_range:
                continue
            # validate range
            if requirement_range.end_value - requirement_range.value > 0:
                return requirement_range
            else:
                # invalid range
                break

    def __default_parsing_case(self) -> RequirementRange:
        numbers_in_sentence = [parse_number(number.word) for number in extract_numbers_nltk(self.__word_pos_tags)]
        if len(numbers_in_sentence) >= RANGE_NUMBERS_COUNT:
            relevant_numbers = [numbers_in_sentence[0], numbers_in_sentence[1]]
            return RequirementRange(minimum(*relevant_numbers), maximum(*relevant_numbers))
        elif len(numbers_in_sentence) == PARAMETER_NUMBERS_COUNT and self.__get_relational_bounds():
            return self.__extract_range(self.__get_relational_bounds()[0])

    def __process_relational_range(self) -> RequirementRange:
        if len(self.__get_relational_bounds()) == PARAMETER_NUMBERS_COUNT:
            return self.__extract_range(self.__get_relational_bounds()[0])

        requirement_range = RequirementRange()
        for index in range(RANGE_NUMBERS_COUNT):
            relational_bound = self.__get_relational_bounds()[index]
            match relational_bound.relation_group:
                case RelationGroup.INCREASED:
                    requirement_range.value = relational_bound.number_bound
                case RelationGroup.DECREASED:
                    requirement_range.end_value = relational_bound.number_bound
        return requirement_range

    def __process_implicit_range(self) -> RequirementRange:
        chunk_list = chunk_sentence(self.__word_pos_tags, IMPLICIT_RANGE_REGEX)
        for chunk in chunk_list:
            return RequirementRange(
                parse_number(find_Nth_in_chunk(chunk, NUMERICAL_POS_TAG, 1)),
                parse_number(find_Nth_in_chunk(chunk, NUMERICAL_POS_TAG, 2)))

    def __process_explicit_range(self) -> RequirementRange:
        chunk_list = chunk_sentence(self.__word_pos_tags, EXPLICIT_RANGE_REGEX)
        for chunk in chunk_list:
            possible_range = chunk[0].word.split('-')
            if len(possible_range) == 2 and is_castable(possible_range[0], int) and \
                    is_castable(possible_range[1], int):
                return RequirementRange(
                    parse_number(possible_range[0]),
                    parse_number(possible_range[1]))

    def __extract_range(self, relational_bound: RelationalBound):
        match relational_bound.relation_group:
            case RelationGroup.INCREASED:
                return RequirementRange(relational_bound.number_bound, float("inf"))
            case RelationGroup.DECREASED:
                return RequirementRange(-float("inf"), relational_bound.number_bound)


    def __get_relational_bounds(self):
        if self.__relational_bounds is None:
            self.__relational_bounds = list(self.__relational_handler.extract_relational_bounds(self.__sentence))
        return self.__relational_bounds
