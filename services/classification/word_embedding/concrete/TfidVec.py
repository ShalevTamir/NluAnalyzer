from services.classification.word_embedding.word_embedder import WordEmbedder
from sklearn.feature_extraction.text import TfidfVectorizer

class TfidVec(WordEmbedder):
    def __init__(self):
        self.__vectorizer = TfidfVectorizer()
    def embedder_contains(self, item: str) -> bool:
        return True

    def embed_item(self, item_to_embed: str) -> list[float]:
        return self.__vectorizer.fit_transform([item_to_embed])

    def embed_collection(self, collection_to_embed: list[str]) -> list[list[float]]:
        return self.__vectorizer.fit_transform(text for text in collection_to_embed)

