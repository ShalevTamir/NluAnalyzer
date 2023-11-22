from typing import Generator, Iterable
from spacy.tokens import Token, Doc, Span

from flask_app.nlu_pkg.models.definitions.spacy_def import SPACY_POS_ATTR, NUMERICAL_POS_TAG


def locate_matching_tokens(tokens: Doc | Span, attribute_name: str, attribute_value: str, strong_comparison=False) \
        -> Generator[Token, None, None]:
    for token in tokens:
        if _comparison_method(attribute_name, attribute_value, strong_comparison)(token):
            yield token


def locate_matching_token(tokens: Doc | Span, attribute_name: str, attribute_value: str,
                          strong_comparison=False) -> Token:
    return next(filter(_comparison_method(attribute_name, attribute_value, strong_comparison), tokens), None)


def _comparison_method(attribute_name: str, attribute_value: str, strong_comparison):
    if strong_comparison:
        def comparison_method(token):
            return attribute_value == getattr(token, attribute_name)
    else:
        def comparison_method(token):
            return attribute_value in getattr(token, attribute_name)
    return comparison_method


def extract_tokens(tokens: Doc | Span, dependency_match) -> Generator[Token, None, None]:
    indexes = dependency_match[1]
    for index in indexes:
        yield tokens[index]


def extract_numbers(tokens: Doc | Span):
    return tuple((number.text for number in
                  locate_matching_tokens(tokens, SPACY_POS_ATTR, NUMERICAL_POS_TAG)))
