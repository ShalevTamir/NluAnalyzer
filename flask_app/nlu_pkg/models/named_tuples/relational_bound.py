from typing import NamedTuple

from ..enums.relation_group import RelationGroup


class RelationalBound(NamedTuple):
    relation_group: RelationGroup
    number_bound: int | float
