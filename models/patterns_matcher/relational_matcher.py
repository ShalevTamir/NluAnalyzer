from models.definitions.spacy_def import PATTERN_POS_ATTR, ADVERB_POS_TAG, PATTERN_DEP_ATTR, ADVERBIAL_MODIFIER_DEP, \
    ADJECTIVE_POS_TAG, ADPOSITION_POS_TAG, NUMERICAL_POS_TAG, PATTERN_OP_ATTR, VERB_POS_TAG, PATTERN_IN_ATTR, \
    NOUN_POS_TAG, PRONOUN_POS_TAG, SUBORDINATING_CONJUNCTION_POS_TAG
from models.patterns_matcher.base_matcher import PatternsMatcher


class RelationalMatcher(PatternsMatcher):
    def __init__(self, relational_pattern_factory):
        # <editor-fold desc="Patterns">

        # Parses syntax: as little as 5
        _reverted_adjective_pattern = [
            {PATTERN_POS_ATTR: ADVERB_POS_TAG, PATTERN_DEP_ATTR: ADVERBIAL_MODIFIER_DEP},
            {PATTERN_POS_ATTR: ADJECTIVE_POS_TAG},
            {PATTERN_POS_ATTR: {PATTERN_IN_ATTR: [ADPOSITION_POS_TAG,
                                                  PRONOUN_POS_TAG,
                                                  SUBORDINATING_CONJUNCTION_POS_TAG]}},
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG},
        ]

        # Parses syntax: greater than 5
        _adjective_pattern = [
            {PATTERN_POS_ATTR: ADJECTIVE_POS_TAG},
            {PATTERN_POS_ATTR: ADPOSITION_POS_TAG},
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG},
        ]

        _noun_adposition_pattern = [
            {PATTERN_POS_ATTR: {PATTERN_IN_ATTR: [ADPOSITION_POS_TAG, NOUN_POS_TAG]}},
            {PATTERN_POS_ATTR: ADPOSITION_POS_TAG},
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG},
        ]

        # Parses syntax: above than 10, above 10
        _adposition_pattern = [
            {PATTERN_POS_ATTR: ADPOSITION_POS_TAG, PATTERN_OP_ATTR: '{0,1}'},
            {PATTERN_POS_ATTR: ADPOSITION_POS_TAG},
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG}
        ]


        # Parses syntax: exceeds 10
        _verb_pattern = [
            {PATTERN_POS_ATTR: VERB_POS_TAG},
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG},
        ]

        # </editor-fold>

        super().__init__([
            relational_pattern_factory(_reverted_adjective_pattern, reverse_classification=True, relational_index=1),
            relational_pattern_factory(_adjective_pattern),
            relational_pattern_factory(_noun_adposition_pattern, reverse_classification=True),
            relational_pattern_factory(_adposition_pattern),
            relational_pattern_factory(_verb_pattern)
        ])
