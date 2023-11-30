from ..definitions.spacy_def import PATTERN_POS_ATTR, ADVERB_POS_TAG, ADVERBIAL_MODIFIER_DEP, PATTERN_DEP_ATTR, \
    PATTERN_TEXT_ATTR, ADJECTIVE_POS_TAG, PATTERN_IN_ATTR, ADPOSITION_POS_TAG, PRONOUN_POS_TAG, \
    SUBORDINATING_CONJUNCTION_POS_TAG, NUMERICAL_POS_TAG, PATTERN_OP_ATTR, PART_POS_TAG, VERB_POS_TAG
from .patterns_group import PatternsGroup
from ...services.pattern_matching.spacy_matchers.spacy_matcher import SpacyMatcher


class RelationalPatternsGroup(PatternsGroup):
    def __init__(self, relational_pattern_factory):
        # <editor-fold desc="Patterns">

        # Parses syntax: as little as 5
        _reverted_adjective_pattern = [
            {
                PATTERN_POS_ATTR: ADVERB_POS_TAG,
                PATTERN_DEP_ATTR: ADVERBIAL_MODIFIER_DEP,
                PATTERN_TEXT_ATTR: 'as'
            },
            {PATTERN_POS_ATTR: ADJECTIVE_POS_TAG},
            {PATTERN_POS_ATTR: {PATTERN_IN_ATTR: [ADPOSITION_POS_TAG,
                                                  PRONOUN_POS_TAG,
                                                  SUBORDINATING_CONJUNCTION_POS_TAG]},
             PATTERN_TEXT_ATTR: 'as'},
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG},
        ]

        # Parses syntax: at least 5
        _reverted_adverb_pattern = [
            {
                PATTERN_POS_ATTR: ADPOSITION_POS_TAG,
                PATTERN_DEP_ATTR: ADVERBIAL_MODIFIER_DEP
            },
            {
                PATTERN_POS_ATTR: {PATTERN_IN_ATTR: [ADVERB_POS_TAG,
                                                     ADPOSITION_POS_TAG,
                                                     ADJECTIVE_POS_TAG]},
                PATTERN_DEP_ATTR: ADVERBIAL_MODIFIER_DEP
            },
            {
                PATTERN_POS_ATTR: NUMERICAL_POS_TAG,
            }
        ]

        # Parses syntax: greater than 5
        _adjective_pattern = [
            {PATTERN_POS_ATTR: ADJECTIVE_POS_TAG},
            {PATTERN_POS_ATTR: ADPOSITION_POS_TAG},
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG},
        ]

        # _noun_adposition_pattern = [
        #     {PATTERN_POS_ATTR: NOUN_POS_TAG},
        #     {PATTERN_POS_ATTR: ADPOSITION_POS_TAG},
        #     {PATTERN_POS_ATTR: NUMERICAL_POS_TAG},
        # ]

        # Parses syntax: above 10
        _adposition_pattern = [
            {PATTERN_POS_ATTR: ADPOSITION_POS_TAG},
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG}
        ]

        # Parses syntax: up to 10
        _reverted_adposition_pattern = [
            {PATTERN_POS_ATTR: ADPOSITION_POS_TAG},
            {PATTERN_POS_ATTR: PART_POS_TAG},
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG}
        ]

        # Parses syntax: exceeds 10
        _verb_pattern = [
            {PATTERN_POS_ATTR: VERB_POS_TAG},
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG},
        ]

        # </editor-fold>

        super().__init__(
            SpacyMatcher(),
            [
                relational_pattern_factory(_reverted_adjective_pattern, reverse_classification=True,
                                           relational_index=1),
                relational_pattern_factory(_reverted_adverb_pattern, reverse_classification=True, relational_index=1),
                relational_pattern_factory(_adjective_pattern),
                relational_pattern_factory(_adposition_pattern),
                relational_pattern_factory(_reverted_adposition_pattern, reverse_classification=True),
                relational_pattern_factory(_verb_pattern)
            ])
