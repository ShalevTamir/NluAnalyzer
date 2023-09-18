import string

# TODO: change to out if possible
def is_castable(string_to_cast: str, type_to_cast: type):
    try:
        type_to_cast(string_to_cast)
        return True
    except ValueError:
        return False

def parse_number(string_to_parse: str) -> int | float:
    if is_castable(string_to_parse, int):
        return int(string_to_parse)
    elif is_castable(string_to_parse,float):
        return float(string_to_parse)
    else:
        raise ValueError(f"Unable to parse string {string_to_parse} to a valid number")

def remove_punctuation(input_string):
    # Make a translation table that maps all punctuation characters to None
    translator = str.maketrans("", "", string.punctuation)

    # Apply the translation table to the input string
    result = input_string.translate(translator)

    return result
