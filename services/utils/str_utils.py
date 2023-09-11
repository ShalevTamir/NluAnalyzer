import string


def is_castable(string, type_to_cast: type):
    try:
        type_to_cast(string)
        return True
    except ValueError:
        return False


def remove_punctuation(input_string):
    # Make a translation table that maps all punctuation characters to None
    translator = str.maketrans("", "", string.punctuation)

    # Apply the translation table to the input string
    result = input_string.translate(translator)

    return result
