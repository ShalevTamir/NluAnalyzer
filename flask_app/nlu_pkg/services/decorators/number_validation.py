from functools import wraps
from spacy.tokens import Span, Doc

from flask_app.nlu_pkg.services.utils.str_utils import parse_number


def validate_numbers_spacy(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tokens: Doc | Span = func(*args, **kwargs)
        _validate_spacy(tokens)
        return tokens

    return wrapper

def _validate_spacy(tokens: Doc | Span):
    from flask_app.nlu_pkg.models.definitions.spacy_def import NUMERICAL_POS_TAG, UNKNOWN_POS_TAG
    for token in tokens:
        try:
            parse_number(token.text)
        except ValueError:
            if token.pos_ == NUMERICAL_POS_TAG:
                token.pos_ = UNKNOWN_POS_TAG
        else:
            token.pos_ = NUMERICAL_POS_TAG



