from typing import NamedTuple

from models.enums.relation_group import RelationGroup


class RelationalBound(NamedTuple):
    relation_group: RelationGroup
    number_bound: int | float
