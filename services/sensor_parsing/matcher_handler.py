from spacy.matcher import Matcher

from models.definitions.spacy_def import SPACY_MODEL


class MatcherHandler:
    def __init__(self):
        self._matcher = Matcher(SPACY_MODEL.vocab)

