from definitions import SPACY_MODEL
from services.classification.word_embedding.decorators.valid_item_check import check_validity
from services.classification.word_embedding.word_embedder import WordEmbedder


class SpacyEmbedder(WordEmbedder):

    def embed_item(self, sentence_to_embed: str) -> list[float]:
        return SPACY_MODEL(sentence_to_embed).vector
