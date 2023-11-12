from abc import ABC, abstractmethod
from typing import TypeVar

from spacy.tokens import Span, Doc
from models.definitions.spacy_def import DEFAULT_PATTERN_NAME

ResultType = TypeVar("ResultType")

class BaseSpacyMatcher(ABC):

    def __init__(self, matcher):
        self._matcher = matcher

    def match(self, tokens: Doc | Span, pattern: list[dict]) -> ResultType:
        self._matcher.add(DEFAULT_PATTERN_NAME, [pattern])
        result = self._compute_match_result(self._matcher, tokens)
        self._matcher.remove(DEFAULT_PATTERN_NAME)
        return result

    @abstractmethod
    def _compute_match_result(self, matcher, tokens: Doc | Span) -> ResultType:
        pass