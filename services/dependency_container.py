from dependency_injector import containers, providers

from services.classification.classifiers.concrete.adjective_classifier import AdjectiveClassifier
from services.classification.adjective_handler import AdjectiveHandler
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from services.classification.word_embedding.concrete.spacy_embedder import SpacyEmbedder
from services.classification.word_embedding.concrete.word2vec_embedder import Word2VecEmbedder
from services.sentence_parser import SentenceParser
from services.subject_detector import SubjectDetector


class DependencyContainer(containers.DeclarativeContainer):
    # ----------------EMBEDDERS---------------
    word2vec_embedder_singleton = providers.Singleton(Word2VecEmbedder)
    spacy_embedder_singleton = providers.Singleton(SpacyEmbedder)

    # ----------------CLASSIFIERS---------------
    adjective_classifier_singleton = providers.Singleton(AdjectiveClassifier,
                                                         word2vec_embedder=word2vec_embedder_singleton)
    sentence_classifier_singleton = providers.Singleton(SentenceClassifier,
                                                        spacy_embedder=spacy_embedder_singleton)

    # ----------------SENTENCE PARSER---------------
    adjective_handler_singleton = providers.Singleton(AdjectiveHandler,
                                                      adjective_classifier=adjective_classifier_singleton)
    subject_detector_singleton = providers.Singleton(SubjectDetector)
    sentence_parser_singleton = providers.Singleton(SentenceParser,
                                                    subject_detector=subject_detector_singleton,
                                                    adjective_handler=adjective_handler_singleton)
