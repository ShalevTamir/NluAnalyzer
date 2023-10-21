from typing import NamedTuple


class Pattern(NamedTuple):
    pattern_rules: list[dict]
    is_reversed: bool
    relational_index: int
    number_index: int


_reverted_adjective_pattern = [
    {
        "RIGHT_ID": "adverb_modifier",
        "RIGHT_ATTRS": {"POS": "ADV", "DEP": "advmod"}
    },
    {
        "LEFT_ID": "adverb_modifier",
        "REL_OP": ".",
        "RIGHT_ID": "adjective",
        "RIGHT_ATTRS": {"POS": "ADJ"}
    },
    {
        "LEFT_ID": "adjective",
        "REL_OP": ".",
        "RIGHT_ID": "adposition",
        "RIGHT_ATTRS": {"POS": "ADP"}
    },
    {
        "LEFT_ID": "adposition",
        "REL_OP": ".",
        "RIGHT_ID": "number",
        "RIGHT_ATTRS": {"POS": "NUM"}
    }
]

_adjective_pattern = [
    {
        "RIGHT_ID": "adjective",
        "RIGHT_ATTRS": {"POS": "ADJ"}
    },
    {
        "LEFT_ID": "adjective",
        "REL_OP": ".",
        "RIGHT_ID": "adposition",
        "RIGHT_ATTRS": {"POS": "ADP"}
    },
    {
        "LEFT_ID": "adposition",
        "REL_OP": ".",
        "RIGHT_ID": "number",
        "RIGHT_ATTRS": {"POS": "NUM"}
    }
]


_adposition_pattern_variation1 = [
    {
        "RIGHT_ID": "first_adposition",
        "RIGHT_ATTRS": {"POS": "ADP"}
    },
    {
        "LEFT_ID": "first_adposition",
        "REL_OP": ".",
        "RIGHT_ID": "second_adposition",
        "RIGHT_ATTRS": {"POS": "ADP"}
    },
    {
        "LEFT_ID": "second_adposition",
        "REL_OP": ".",
        "RIGHT_ID": "number",
        "RIGHT_ATTRS": {"POS": "NUM"}
    }
]

_adposition_pattern_variation2 = [
    {
        "RIGHT_ID": "adposition",
        "RIGHT_ATTRS": {"POS": "ADP"}
    },
    {
        "LEFT_ID": "adposition",
        "REL_OP": ".",
        "RIGHT_ID": "number",
        "RIGHT_ATTRS": {"POS": "NUM"}
    }
]

_verb_pattern = [
    {
        "RIGHT_ID": "verb",
        "RIGHT_ATTRS": {"POS": "VERB"}
    },
    {
        "LEFT_ID": "verb",
        "REL_OP": ".",
        "RIGHT_ID": "number",
        "RIGHT_ATTRS": {"POS": "NUM"}
    }
]

patterns = [
    Pattern(_reverted_adjective_pattern, True, 1, -1),
    Pattern(_adjective_pattern, False, 0, -1),
    Pattern(_adposition_pattern_variation1, False, 0, -1),
    Pattern(_adposition_pattern_variation2, False, 0, -1),
    Pattern(_verb_pattern, False, 0, -1)
]
