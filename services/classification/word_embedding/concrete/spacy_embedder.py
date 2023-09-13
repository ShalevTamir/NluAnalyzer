import spacy

from services.classification.word_embedding.base_word_embedder import IWordEmbedder


class SpacyEmbedder(IWordEmbedder):
    def __init__(self):
        self.spacy_model = spacy.load('en_core_web_sm')

    def embed_item(self, sentence_to_embed: str) -> list[float]:
        return self.spacy_model(sentence_to_embed).vector

    def embedder_contains(self, item: str) -> bool:
        return self.spacy_model(item).has_vector
