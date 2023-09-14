import string


def preprocess_sentence(sentence: str):
    # remove punctuation marks
    return sentence.translate({ord(character): None
                               for character in string.punctuation
                               if character != '-'})
