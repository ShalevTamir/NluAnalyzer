from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Generic

T = TypeVar("T", bound=type(Enum))


class IClassificationModel(ABC, Generic[T]):
    @abstractmethod
    def predict(self, value: list[float]) -> T:
        pass
