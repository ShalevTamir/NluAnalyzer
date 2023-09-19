import spacy

from services.classification.word_embedding.word_embedder import WordEmbedder


class SpacyEmbedder(WordEmbedder):
    def __init__(self):
        self.__spacy_model = spacy.load('en_core_web_sm')

    def embed_item(self, sentence_to_embed: str) -> list[float]:
        return self.__spacy_model(sentence_to_embed).vector

    def embedder_contains(self, item: str) -> bool:
        return self.__spacy_model(item).has_vector
