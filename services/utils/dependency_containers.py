from dependency_injector import containers, providers

from services.classification.classifiers.concrete.adjective_classifier import AdjectiveClassifier
from services.classification.adjective_handler import AdjectiveHandler
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from services.classification.word_embedding.concrete.spacy_embedder import SpacyEmbedder
from services.classification.word_embedding.concrete.word2vec_embedder import Word2VecEmbedder
from services.range_handler import RangeHandler
from services.sentence_parser import SentenceParser
from services.subject_detector import SubjectDetector


class Embedders(containers.DeclarativeContainer):
    word2vec_embedder = providers.Singleton(Word2VecEmbedder)
    spacy_embedder = providers.Singleton(SpacyEmbedder)


class Classifiers(containers.DeclarativeContainer):
    embedders = providers.DependenciesContainer()

    adjective = providers.Singleton(AdjectiveClassifier,
                                    word2vec_embedder=embedders.word2vec_embedder)
    sentence = providers.Singleton(SentenceClassifier,
                                   spacy_embedder=embedders.spacy_embedder)


class Services(containers.DeclarativeContainer):
    classifiers = providers.DependenciesContainer()

    adjective_handler = providers.Factory(AdjectiveHandler,
                                          adjective_classifier=classifiers.adjective)
    range_handler_singleton = providers.Singleton(RangeHandler,
                                                  adjective_handler=adjective_handler.provider)
    subject_detector = providers.Singleton(SubjectDetector)
    sentence_parser = providers.Singleton(SentenceParser,
                                          subject_detector=subject_detector,
                                          sentence_classifier=classifiers.sentence,
                                          range_handler=range_handler_singleton)


class Application(containers.DeclarativeContainer):
    embedders = providers.Container(Embedders)
    classifiers = providers.Container(
        Classifiers,
        embedders=embedders
    )
    services = providers.Container(
        Services,
        classifiers=classifiers
    )