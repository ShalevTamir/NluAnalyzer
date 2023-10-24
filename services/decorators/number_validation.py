from functools import wraps
from spacy.tokens import Span, Doc

from models.named_tuples.word_pos_tag import WordPosTag
from services.utils.str_utils import parse_number


def validate_numbers_spacy(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tokens: Doc | Span = func(*args, **kwargs)
        _validate_spacy(tokens)
        return tokens

    return wrapper

def validate_numbers_nltk(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        word_pos_tags = func(*args, **kwargs)
        _validate_nltk(word_pos_tags)
        return word_pos_tags

    return wrapper

def _validate_spacy(tokens: Doc | Span):
    from definitions import NUMERICAL_POS_TAG_SPACY
    for token in tokens:
        try:
            parse_number(token.text)
        except ValueError:
            continue
        else:
            token.pos_ = NUMERICAL_POS_TAG_SPACY


def _validate_nltk(word_pos_tags: list[WordPosTag]):
    from definitions import NUMERICAL_POS_TAG_NLTK
    for index in range(len(word_pos_tags)):
        word_pos_tag = word_pos_tags[index]
        try:
            parse_number(word_pos_tag.word)
        except ValueError:
            continue
        else:
            word_pos_tags[index] = WordPosTag(word_pos_tag.word, NUMERICAL_POS_TAG_NLTK)


