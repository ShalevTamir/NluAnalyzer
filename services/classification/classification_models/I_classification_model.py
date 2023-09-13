from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Generic

GroupEnum = TypeVar("GroupEnum",bound=Enum)


class IClassificationModel(ABC, Generic[GroupEnum]):
    @abstractmethod
    def predict(self, value: list[float]) -> GroupEnum:
        pass
