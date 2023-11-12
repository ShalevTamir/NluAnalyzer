from typing import Iterable, Generator, Tuple

from spacy.matcher import DependencyMatcher, Matcher
from spacy.tokens import Span, Doc, Token

from models.definitions.spacy_def import SPACY_MODEL
from services.pattern_matching.spacy_matchers.base_spacy_matcher import BaseSpacyMatcher

_MATCH_INDEXES_INDEX = 1


class SpacyDependencyMatcher(BaseSpacyMatcher):

    def __init__(self):
        super().__init__(DependencyMatcher(SPACY_MODEL.vocab))

    def _compute_match_result(self, matcher: DependencyMatcher, tokens: Doc | Span) -> \
            list[list[Token]]:
        results = matcher(tokens)
        return [
            [tokens[token_index] for token_index in result[_MATCH_INDEXES_INDEX]]
            for result in results
        ]

