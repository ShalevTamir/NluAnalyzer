from abc import ABC, abstractmethod


class WordEmbedder(ABC):

    @abstractmethod
    def embed_item(self, item_to_embed: str) -> list[float]:
        pass

    def embed_collection(self, collection_to_embed: list[str]) -> list[list[float]]:

        return [
            self.embed_item(item_to_embed)
            for item_to_embed in collection_to_embed
        ]
