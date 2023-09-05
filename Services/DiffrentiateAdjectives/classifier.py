import os
from typing import List

from Services.DependencyContainer import DependencyContainer
from definitions import ROOT_DIR
from Services.DiffrentiateAdjectives.LogisticRegression import LogisticRegression
from Services.DiffrentiateAdjectives.AdjectiveFileParser import parse_file
from gensim.models import KeyedVectors
from Models.Enums.adjective_group import AdjectiveGroup
import gensim.downloader as GensimDownloader

DECREASED_FILE_NAME = "decreased"
INCREASED_FILE_NAME = "increased"
WORD_EMBEDDING_MODEL_NAME = "word2vec-google-news-300"


class Classifier:
    def __init__(self):
        self.word_embedding_model = self._retrieve_embedding_model()

        increased_adjectives = self._embed_adjectives(parse_file(INCREASED_FILE_NAME))
        decreased_adjectives = self._embed_adjectives(parse_file(DECREASED_FILE_NAME))
        all_adjectives = decreased_adjectives + increased_adjectives
        lst_groups = ([AdjectiveGroup.Decreased.value] * len(decreased_adjectives) +
                      [AdjectiveGroup.Increased.value] * len(increased_adjectives))

        self.classification_model = LogisticRegression(all_adjectives, lst_groups)

    @staticmethod
    def _retrieve_embedding_model():
        embedding_model_path = os.path.join(ROOT_DIR, "Documents", WORD_EMBEDDING_MODEL_NAME + ".kv")
        if not os.path.isfile(embedding_model_path) or not os.path.isfile(embedding_model_path + ".vectors.npy"):
            embedding_model = GensimDownloader.load(WORD_EMBEDDING_MODEL_NAME)
            embedding_model.save(embedding_model_path)
        return KeyedVectors.load(embedding_model_path, mmap='r')

    def _embed_adjectives(self, adjectives: List[str]):
        return [
            self.word_embedding_model[adjective.lower()]
            for adjective in adjectives
            if adjective.lower() in self.word_embedding_model
        ]

    def classify_word(self, word_to_classify: str) -> AdjectiveGroup:
        word_vector = self.word_embedding_model.get_vector(word_to_classify)
        return AdjectiveGroup(self.classification_model.predict(word_vector))
