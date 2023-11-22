from enum import Enum
from json import JSONEncoder


class CustomEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Enum):
            return o.value
        else:
            return o.__dict__

