from typing import Iterable

from spacy.matcher import Matcher
from spacy.tokens import Span, Doc

from models.definitions.spacy_def import SPACY_MODEL
from services.pattern_matching.spacy_matchers.base_spacy_matcher import BaseSpacyMatcher


class SpacyMatcher(BaseSpacyMatcher):

    def __init__(self):
        super().__init__(Matcher(SPACY_MODEL.vocab))

    def _compute_match_result(self, matcher: Matcher, tokens: Doc | Span) -> list[Span]:
        return matcher(tokens, as_spans=True)



