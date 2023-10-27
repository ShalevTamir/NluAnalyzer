from enum import Enum, auto


class RelationGroup(Enum):
    DECREASED = 0
    INCREASED = 1


def revert_relation_group(relation_group: RelationGroup):
    return RelationGroup(1 - relation_group.value)
