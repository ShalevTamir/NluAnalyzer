from typing import NamedTuple

from flask_app.nlu_pkg.models.enums.relation_group import RelationGroup


class RelationalBound(NamedTuple):
    relation_group: RelationGroup
    number_bound: int | float
