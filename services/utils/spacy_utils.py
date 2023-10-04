from typing import Generator

from spacy.tokens import Token


def token_match(token_property: str, dependencies_to_match: list[str]) -> bool:
    for dependency in dependencies_to_match:
        if dependency in token_property:
            return True
    return False


def matching_tokens(lst_token, dependencies_to_match: list[str]) \
        -> Generator[Token, None, None]:
    for token in lst_token:
        if token_match(token.dep_, dependencies_to_match):
            yield token


