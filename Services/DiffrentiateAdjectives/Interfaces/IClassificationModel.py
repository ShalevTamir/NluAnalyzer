from abc import ABC, abstractmethod


class IClassificationModel(ABC):
    @abstractmethod
    def predict(self, value: float | int):
        pass
