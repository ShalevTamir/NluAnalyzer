from typing import NamedTuple

from models.enums.adjective_group import AdjectiveGroup


class AdjectiveBound(NamedTuple):
    adjective_group: AdjectiveGroup
    number_bound: int | float
