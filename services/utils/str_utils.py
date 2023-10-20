import re
import string
from definitions import FIND_NUMBERS_REG
from services.utils.general import is_castable


def parse_number(string_to_parse: str) -> int | float:
    regex_result = re.search(FIND_NUMBERS_REG, string_to_parse)
    if regex_result:
        string_to_parse = regex_result.group(0)
        if is_castable(string_to_parse, int):
            return int(string_to_parse)
        elif is_castable(string_to_parse, float):
            return float(string_to_parse)

    raise ValueError(f"Unable to parse string {string_to_parse} to a valid number")


def remove_punctuation(input_string):
    # Make a translation table that maps all punctuation characters to None
    translator = str.maketrans("", "", string.punctuation)

    # Apply the translation table to the input string
    result = input_string.translate(translator)

    return result


def extract_numbers(string):
    return [parse_number(number)
            for number in re.findall(FIND_NUMBERS_REG, string)]
