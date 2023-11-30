from .....models.definitions.spacy_def import SPACY_MODEL
from ..word_embedder import WordEmbedder


class SpacyEmbedder(WordEmbedder):
    def embed_item(self, sentence_to_embed: str) -> list[float]:
        return SPACY_MODEL(sentence_to_embed).vector
