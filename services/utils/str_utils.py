import re
import string
from definitions import FIND_NUMBERS_REG
from services.utils.general import is_castable


def extract_number(string_to_search: str) -> str:
    regex_result = re.search(FIND_NUMBERS_REG, string_to_search)
    if regex_result:
        return regex_result.group(0)

def parse_number(string_to_parse: str) -> int | float:
    number_in_string = extract_number(string_to_parse)
    if number_in_string:
        if is_castable(number_in_string, int):
            return int(number_in_string)
        elif is_castable(number_in_string, float):
            return float(number_in_string)

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
