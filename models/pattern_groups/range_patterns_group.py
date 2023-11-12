from models.definitions.spacy_def import PATTERN_POS_ATTR, NUMERICAL_POS_TAG, NOUN_POS_TAG, PATTERN_IN_ATTR, \
    ADPOSITION_POS_TAG, PATTERN_OP_ATTR, PARTICLE_POS_TAG, CONJUNCTION_POS_TAG, COORDINATING_CONJUNCTION_POS_TAG, \
    SUBORDINATING_CONJUNCTION_POS_TAG, PUNCTUATION_POS_TAG, SYMBOL_POS_TAG
from models.pattern_groups.patterns_group import PatternsGroup
from services.pattern_matching.pattern_handlers.range_pattern_handler import RangePatternHandler
from services.pattern_matching.spacy_matchers.spacy_matcher import SpacyMatcher


class RangePatternsGroup(PatternsGroup):
    def __init__(self):
        # <editor-fold desc="Patterns">

        # Parses syntax: Engine heat is between 100 degrees and 200 degrees, Engine heat is in range 50 to 200
        _explicit_range_pattern = [
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG},
            {PATTERN_POS_ATTR: NOUN_POS_TAG, PATTERN_OP_ATTR: '{0,1}'},
            {PATTERN_POS_ATTR: {PATTERN_IN_ATTR: [ADPOSITION_POS_TAG,
                                                  PARTICLE_POS_TAG,
                                                  CONJUNCTION_POS_TAG,
                                                  COORDINATING_CONJUNCTION_POS_TAG,
                                                  SUBORDINATING_CONJUNCTION_POS_TAG
                                                  ]}},
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG}
        ]

        # Parses syntax: Engine heat in range 100-200
        _linked_range_pattern = [
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG},
            {PATTERN_POS_ATTR: {PATTERN_IN_ATTR: [PUNCTUATION_POS_TAG, SYMBOL_POS_TAG]}},
            {PATTERN_POS_ATTR: NUMERICAL_POS_TAG}
        ]

        # </editor-fold>

        super().__init__(
            SpacyMatcher(),
            [
                RangePatternHandler(_explicit_range_pattern),
                RangePatternHandler(_linked_range_pattern)
            ])
