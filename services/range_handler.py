import re
from typing import Callable

from numpy import minimum, maximum

from definitions import INVALID_SENT, NUMERICAL_POS_TAG, COMPARATIVE_ADJECTIVE_POS_TAG, ADJECTIVE_OR_NUMERICAL_POS_TAG, \
    CONJUNCTION_POS_TAG, FIND_NUMBERS_REG, RANGE_NUMBERS_COUNT, PARAMETER_NUMBERS_COUNT
from services.utils.nltk_utils import chunk_sentence, revert_word_pos_tags, find_Nth_in_chunk
from models.adjective_bound import AdjectiveBound
from models.enums.adjective_group import AdjectiveGroup
from models.requirement_range import RequirementRange
from models.word_pos_tag import WordPosTag
from services.classification.adjective_handler import AdjectiveHandler
from services.utils.str_utils import is_castable, parse_number, extract_numbers as extract_numbers_str
from services.utils.nltk_utils import extract_numbers as extract_numbers_nltk


class RangeHandler:

    def __init__(self, adjective_handler: AdjectiveHandler):
        self.__adjective_handler = adjective_handler
        self.regex_dict = {
            # Parses syntax: Engine heat is between 100 and 200
            r"Chunk: {<" + NUMERICAL_POS_TAG + "><.+><" + NUMERICAL_POS_TAG + ">}": self.__process_implicit_range,
            # Parses syntax: Engine heat in range 100-200
            r"Chunk: {<" + ADJECTIVE_OR_NUMERICAL_POS_TAG + ">}": self.__process_explicit_range,
            # Parses syntax: Engine heat is greater than 50
            r"Chunk: {<" + COMPARATIVE_ADJECTIVE_POS_TAG + "><" + CONJUNCTION_POS_TAG + "><" + NUMERICAL_POS_TAG + ">}": self.__process_adjectives_range
        }

    def parse_sentence(self, word_pos_tags: list[WordPosTag]) -> RequirementRange:
        self.__validate_number_detection(word_pos_tags)
        for regex_key in self.regex_dict.keys():
            chunk_list = chunk_sentence(word_pos_tags, regex_key)
            if len(chunk_list) > 0:
                resolving_method: Callable[[list[list[WordPosTag]]], RequirementRange] = self.regex_dict[regex_key]
                requirement_range: RequirementRange = resolving_method(chunk_list)
                if not requirement_range:
                    continue
                if self.__valid_range(requirement_range):
                    return requirement_range
        return self.__default_parsing_case(word_pos_tags)

    def __default_parsing_case(self, word_pos_tags: list[WordPosTag]) -> RequirementRange:
        numbers_in_sentence = [parse_number(number.word) for number in extract_numbers_nltk(word_pos_tags)]
        comparative_adjectives = self.__adjective_handler.extract_comparative_adjectives(word_pos_tags)
        if len(numbers_in_sentence) >= RANGE_NUMBERS_COUNT:
            relevant_numbers = [numbers_in_sentence[0], numbers_in_sentence[1]]
            return RequirementRange(minimum(*relevant_numbers), maximum(*relevant_numbers))
        elif len(numbers_in_sentence) == PARAMETER_NUMBERS_COUNT and comparative_adjectives:
            return self.__extract_range(AdjectiveBound(comparative_adjectives[0], numbers_in_sentence[0]))

    def __validate_number_detection(self, word_pos_tags: list[WordPosTag]):
        numbers = extract_numbers_nltk(word_pos_tags)
        for index in range(len(word_pos_tags)):
            word_pos_tag = word_pos_tags[index]
            if word_pos_tag in numbers and word_pos_tag.pos_tag != NUMERICAL_POS_TAG:
                word_pos_tags[index] = WordPosTag(word_pos_tag.word, NUMERICAL_POS_TAG)

    def __valid_range(self, requirement_range: RequirementRange):
        if requirement_range.end_value - requirement_range.value < 1:
            return False
        return True

    def __process_adjectives_range(self, chunk_list: list[list[WordPosTag]]) -> RequirementRange:
        comparative_bounds = self.__adjective_handler.extract_comparative_bounds(chunk_list)
        if len(comparative_bounds) == PARAMETER_NUMBERS_COUNT:
            return self.__extract_range(comparative_bounds[0])

        requirement_range = RequirementRange()
        for index in range(RANGE_NUMBERS_COUNT):
            comparative_bound = comparative_bounds[index]
            match comparative_bound.adjective_group:
                case AdjectiveGroup.INCREASED:
                    requirement_range.value = comparative_bound.number_bound
                case AdjectiveGroup.DECREASED:
                    requirement_range.end_value = comparative_bound.number_bound
        return requirement_range

    def __process_implicit_range(self, chunk_list: list[list[WordPosTag]]) -> RequirementRange:
        for chunk in chunk_list:
            return RequirementRange(
                parse_number(find_Nth_in_chunk(chunk, NUMERICAL_POS_TAG, 1)),
                parse_number(find_Nth_in_chunk(chunk, NUMERICAL_POS_TAG, 2)))

    def __process_explicit_range(self, chunk_list: list[list[WordPosTag]]) -> RequirementRange:
        for chunk in chunk_list:
            possible_range = chunk[0].word.split('-')
            if len(possible_range) == 2 and is_castable(possible_range[0], int) and \
                    is_castable(possible_range[1], int):
                return RequirementRange(
                    parse_number(possible_range[0]),
                    parse_number(possible_range[1]))

    def __extract_range(self, adjective_bound: AdjectiveBound):
        match adjective_bound.adjective_group:
            case AdjectiveGroup.INCREASED:
                return RequirementRange(adjective_bound.number_bound, float("inf"))
            case AdjectiveGroup.DECREASED:
                return RequirementRange(-float("inf"), adjective_bound.number_bound)
