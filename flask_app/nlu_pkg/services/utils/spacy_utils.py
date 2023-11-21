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


def extract_tokens(tokens: Doc, dependency_match) -> Generator[Token, None, None]:
    indexes = dependency_match[1]
    for index in indexes:
        yield tokens[index]


def extract_numbers(tokens: Doc | Span):
    return tuple((number.text for number in
                  locate_matching_tokens(tokens, SPACY_POS_ATTR, NUMERICAL_POS_TAG)))


def spacy_getitem(tokens: Doc | Span, index: int | slice) -> Token | Span:
    if isinstance(tokens, Doc):
        return tokens[index]
    elif isinstance(tokens, Span):
        if isinstance(index, int):
            index = _adjust_index(tokens, index)
        elif isinstance(index, slice):
            index = slice(
                _adjust_index(tokens, index.start),
                _adjust_index(tokens, index.stop),
                _adjust_index(tokens, index.step)
            )
        return tokens[index]


def _adjust_index(span: Span, index: int | None):
    return index if index is None else span.start - index
