from abc import ABC, abstractmethod


class IWordEmbedder(ABC):
    @abstractmethod
    def embed_item(self, item_to_embed: str) -> list[float]:
        pass

    @abstractmethod
    def embedder_contains(self, item: str) -> bool:
        pass

    @abstractmethod
    def embed_collection(self, collection_to_embed: list[str]) -> list[list[float]]:
        pass
    