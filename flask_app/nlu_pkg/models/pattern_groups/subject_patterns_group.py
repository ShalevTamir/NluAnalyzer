from flask_app.nlu_pkg.models.definitions.spacy_def import PATTERN_POS_ATTR, VERB_POS_TAG, NOUN_POS_TAG, \
    PATTERN_DEP_ATTR, DIRECT_OBJECT_DEP, COMPOUND_DEP
from flask_app.nlu_pkg.models.pattern_groups.patterns_group import PatternsGroup
from flask_app.nlu_pkg.services.pattern_matching.pattern_handlers.subject_pattern_handler import SubjectPatternHandler
from flask_app.nlu_pkg.services.pattern_matching.spacy_matchers.spacy_dependency_matcher import SpacyDependencyMatcher


class SubjectPatternsGroup(PatternsGroup):
    def __init__(self):
        # <editor-fold desc="Patterns">
        verb_preceding_subject = [
            {
                "RIGHT_ID": "verb",
                "RIGHT_ATTRS": {PATTERN_POS_ATTR: VERB_POS_TAG}
            },
            {
                "LEFT_ID": "verb",
                "REL_OP": ">",
                "RIGHT_ID": "subject",
                "RIGHT_ATTRS": {PATTERN_POS_ATTR: NOUN_POS_TAG, PATTERN_DEP_ATTR: DIRECT_OBJECT_DEP}
            }
        ]

        double_noun = [
            {
                "RIGHT_ID": "subject",
                "RIGHT_ATTRS": {PATTERN_POS_ATTR: NOUN_POS_TAG}
            },
            {
                "LEFT_ID": "subject",
                "REL_OP": ">",
                "RIGHT_ID": "noun",
                "RIGHT_ATTRS": {PATTERN_DEP_ATTR: COMPOUND_DEP}
            }
        ]
        # </editor-fold>

        super().__init__(SpacyDependencyMatcher(),
                         [
                             SubjectPatternHandler(verb_preceding_subject)
                             # SubjectPatternHandler(double_noun, subject_index=0)
                         ])

