from spacy.tokens import Span, Doc, Token

from flask_app.nlu_pkg.models.definitions.spacy_def import SPACY_DEP_ATTR, SUBJECT_DEP, COORDINATION_DEP, SPACY_MODEL, \
    SPACY_POS_ATTR, \
    NUMERICAL_POS_TAG, SPAN_SUBJECT_ATTR, SPAN_DURATION_SEC_ATTR
from flask_app.nlu_pkg.models.pattern_groups.subject_patterns_group import SubjectPatternsGroup
from flask_app.nlu_pkg.services.sensor_parsing.subject_detector import SubjectDetector
from flask_app.nlu_pkg.services.utils.spacy_utils import locate_matching_tokens, locate_matching_token, spacy_getitem


class TextPartitioner:

    def __init__(self, subject_detector: SubjectDetector):
        self._subject_detector = subject_detector
        Span.set_extension(
            SPAN_SUBJECT_ATTR,
            default=None,
            force=True
        )
        Span.set_extension(
            SPAN_DURATION_SEC_ATTR,
            default=None
        )

    def extract_sentences(self, tokens: Doc | Span):
        subjects = list(self._subject_detector.detect(tokens, multiple=True))
        subjects.sort(key=lambda subject: subject.i)
        # print("EXTRACTED SUBJECTS",subjects)
        if subjects:
            sentences = [
                spacy_getitem(tokens, slice(current_subject.i, next_subject.i))
                for current_subject, next_subject in zip(subjects, subjects[1:])
            ]

            sentences.append(spacy_getitem(tokens, slice(subjects[-1].i, None)))
        else:
            subjects = [spacy_getitem(tokens, 0)]
            sentences = [spacy_getitem(tokens, slice(0, None))]

        self._assign_subjects(sentences, subjects)
        return sentences

    def _assign_subjects(self, sentences: list[Span], subjects: list[Token]):
        for i in range(len(sentences)):
            sentences[i]._.set(SPAN_SUBJECT_ATTR, subjects[i])

    def remove_sent_noise(self, sentence: Span):
        """Cuts everything after the last number"""
        numbers = list(locate_matching_tokens(sentence, SPACY_POS_ATTR, NUMERICAL_POS_TAG))
        if numbers:
            return spacy_getitem(sentence, slice(0, numbers[-1].i))
        else:
            return sentence

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
