from typing import Generator, Iterable

from spacy.tokens import Token, Doc


def matches_dependency(token_property: str, dependencies_to_match: Iterable[str]) -> bool:
    for dependency in dependencies_to_match:
        if dependency in token_property:
            return True
    return False


def find_dependencies(tokens: Iterable[Token], dependencies_to_match: list[str]) \
        -> Generator[Token, None, None]:
    for token in tokens:
        if matches_dependency(token.dep_, dependencies_to_match):
            yield token


def find_dependency(tokens: Iterable[Token], dependency_to_match: str) -> Token:
    return next(filter(lambda token: token.dep_ == dependency_to_match, tokens), None)


def extract_tokens(tokens: Doc, dependency_match) -> Generator[Token, None, None]:
    indexes = dependency_match[1]
    for index in indexes:
        yield tokens[index]



