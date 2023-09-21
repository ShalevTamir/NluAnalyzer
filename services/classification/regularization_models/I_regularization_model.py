from abc import ABC, abstractmethod


class IRegularizationModel(ABC):
    @abstractmethod
    def regularize(self,embedded_group1: list[list[float]], embedded_group2: list[float]):
        pass
