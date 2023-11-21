from enum import Enum

from flask_app.nlu_pkg.models.enums.noun_type import NounType


class DurationType(Enum):
    UNDEFINED = 0
    SECONDS = 1
    MINUTES = 2
    HOURS = 3


def get_type_text(duration_type: DurationType, noun_type: NounType):
    match noun_type:
        case NounType.PLURAL:
            return duration_type.name.lower()
        case NounType.SINGULAR:
            return duration_type.name.lower()[:-1]
