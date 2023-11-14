from itertools import chain

from spacy.tokens import Span, Doc, Token

from models.definitions.spacy_def import SPACY_DEP_ATTR, SUBJECT_DEP, COORDINATION_DEP, SPACY_MODEL, SPACY_POS_ATTR, \
    NUMERICAL_POS_TAG, SPAN_SUBJECT_ATTR
from models.pattern_groups.subject_patterns_group import SubjectPatternsGroup
from services.sensor_parsing.subject_detector import SubjectDetector
from services.utils.spacy_utils import locate_matching_tokens, locate_matching_token


# TODO: use subject detector to detect the subjects
# TODO: convert to yield

class TextPartitioner:

    def __init__(self, subject_detector: SubjectDetector):
        self._subject_detector = subject_detector
        Span.set_extension(
            "subject",
            default=None,
            force=True
        )

    def extract_sentences(self, tokens: Doc | Span):
        subjects = list(self._subject_detector.detect(tokens, multiple=True))
        subjects.sort(key=lambda subject: subject.i)
        # print("EXTRACTED SUBJECTS",subjects)
        sentences = []
        if subjects:
            sentences = [
                tokens[current_subject.i:next_subject.i]
                for current_subject, next_subject in zip(subjects, subjects[1:])
            ]

            sentences.append(tokens[subjects[-1].i:])
        else:
            subjects = [tokens[0]]
            sentences = [tokens[::]]

        self._cleanup_sentences(sentences)
        self._assign_subjects(sentences, subjects)
        return sentences

    def _assign_subjects(self, sentences: list[Span], subjects: list[Token]):
        for i in range(len(sentences)):
            sentences[i]._.set(SPAN_SUBJECT_ATTR, subjects[i])

    def _cleanup_sentences(self, sentences: list[Span]):
        for i in range(len(sentences)):
            numbers = list(locate_matching_tokens(sentences[i], SPACY_POS_ATTR, NUMERICAL_POS_TAG))
            if numbers:
                # Cut everything after the last number
                sentences[i] = sentences[i][:numbers[-1].i - sentences[i].start + 1]

    # def _extract_sentences_with_subsentences(self, tokens: Doc | Span):
    #     subjects = list(locate_matching_tokens(tokens, SPACY_DEP_ATTR, SUBJECT_DEP))
    #     if subjects:
    #         sentences = list(chain.from_iterable([
    #             self._locate_subsentences(tokens[current_subject.i:next_subject.i])
    #             for current_subject, next_subject in zip(subjects, subjects[1:])
    #         ]))
    #         sentences += self._locate_subsentences(tokens[subjects[-1].i:])
    #
    #         return sentences
    #     else:
    #         return tokens
    #
    # def _locate_subsentences(self, sentence_tokens: Span) -> list[Span]:
    #     subject_token = locate_matching_token(sentence_tokens, SPACY_DEP_ATTR, SUBJECT_DEP)
    #     if subject_token:
    #         conjunction_token = locate_matching_token(subject_token.head.rights, SPACY_DEP_ATTR, COORDINATION_DEP)
    #         if conjunction_token:
    #             return [sentence_tokens[:conjunction_token.i]] + self._locate_subsentences(
    #                 sentence_tokens[conjunction_token.i:])
    #     return [sentence_tokens]
