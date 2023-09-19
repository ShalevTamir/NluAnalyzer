import string
from nltk import word_tokenize


def preprocess_sentence(sentence: str):
    sentence = sentence.lower()
    # remove punctuation marks
    words_in_sentence = word_tokenize(sentence)
    sentence = " ".join([word for word in words_in_sentence if word != '.'])
    chars_to_exclude = ['-', '.']
    return sentence.translate({ord(character): None
                               for character in string.punctuation
                               if character not in chars_to_exclude})
