from itertools import chain

from spacy.tokens import Span, Doc

from models.definitions.spacy_def import SPACY_DEP_ATTR, SUBJECT_DEP, COORDINATION_DEP, SPACY_MODEL
from services.utils.spacy_utils import locate_matching_tokens, locate_matching_token


# TODO: use subject detector to detect the subjects
# TODO: convert to yield

def extract_sentences(tokens: Doc | Span):
    subjects = list(locate_matching_tokens(tokens, SPACY_DEP_ATTR, SUBJECT_DEP))
    if subjects:
        sentences = [
            tokens[current_subject.i:next_subject.i]
            for current_subject, next_subject in zip(subjects, subjects[1:])
        ]
        sentences.append(tokens[subjects[-1].i:])

        return sentences
    else:
        return [tokens]


def _extract_sentences_with_subsentences(tokens: Doc | Span):
    subjects = list(locate_matching_tokens(tokens, SPACY_DEP_ATTR, SUBJECT_DEP))
    if subjects:
        sentences = list(chain.from_iterable([
            _locate_subsentences(tokens[current_subject.i:next_subject.i])
            for current_subject, next_subject in zip(subjects, subjects[1:])
        ]))
        sentences += _locate_subsentences(tokens[subjects[-1].i:])

        return sentences
    else:
        return tokens


def _locate_subsentences(sentence_tokens: Span) -> list[Span]:
    subject_token = locate_matching_token(sentence_tokens, SPACY_DEP_ATTR, SUBJECT_DEP)
    if subject_token:
        conjunction_token = locate_matching_token(subject_token.head.rights, SPACY_DEP_ATTR, COORDINATION_DEP)
        if conjunction_token:
            return [sentence_tokens[:conjunction_token.i]] + _locate_subsentences(sentence_tokens[conjunction_token.i:])
    return [sentence_tokens]


# sentence = "Engine heat is greater than 50, but also the Temperature is lower than 1200"
# print(*extract_sentences(SPACY_MODEL(sentence)), sep='\n')
