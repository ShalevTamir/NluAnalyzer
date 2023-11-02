from typing import Generator, Iterable
from spacy.tokens import Token, Doc, Span

from models.definitions.spacy_def import SPACY_POS_ATTR, NUMERICAL_POS_TAG


def locate_matching_tokens(tokens: Doc | Span, attribute_name: str, attribute_value: str) \
        -> Generator[Token, None, None]:
    for token in tokens:
        if attribute_value in getattr(token, attribute_name):
            yield token


def locate_matching_token(tokens: Doc | Span, attribute_name: str, attribute_value: str) -> Token:
    return next(filter(lambda token: attribute_value in getattr(token, attribute_name), tokens), None)


def extract_tokens(tokens: Doc, dependency_match) -> Generator[Token, None, None]:
    indexes = dependency_match[1]
    for index in indexes:
        yield tokens[index]


def extract_numbers(tokens: Doc | Span):
    return tuple((number.text for number in
                  locate_matching_tokens(tokens, SPACY_POS_ATTR, NUMERICAL_POS_TAG)))
