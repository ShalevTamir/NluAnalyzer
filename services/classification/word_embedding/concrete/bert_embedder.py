from services.classification.word_embedding.base_word_embedder import IWordEmbedder
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA


class BertEmbedder(IWordEmbedder):
    def __init__(self):
        self._model = SentenceTransformer('bert-base-nli-mean-tokens')
        self._pca = PCA(n_components=96)

    def embed_item(self, item_to_embed: str) -> list[float]:
        return self._pca.fit_transform(self._model.encode([item_to_embed]))[0]

    def embedder_contains(self, item: str) -> bool:
        return True
