from functools import partial

from spacy.tokens import Span, Doc
from spacy.tokens.token import Token

from models.definitions.spacy_def import SPACY_MODEL, SPACY_DEP_ATTR, SUBJECT_DEP, ROOT_DEP
from services.utils.spacy_utils import locate_matching_token


_SUBJ_DEPENDENCIES = [SUBJECT_DEP, ROOT_DEP]
_SUBJ_SPACE_CHAR = '_'


def detect(tokens: Doc | Span):
    subject_locators = [
        partial(locate_matching_token, tokens, 'text', _SUBJ_SPACE_CHAR),
        *[
            partial(locate_matching_token, tokens, SPACY_DEP_ATTR, subj_dependency)
            for subj_dependency in _SUBJ_DEPENDENCIES
        ]
    ]

    for subject_locator in subject_locators:
        possible_subject = subject_locator()
        if possible_subject:
            return possible_subject.text
