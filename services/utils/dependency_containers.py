from dependency_injector import containers, providers
from services.classification.classifiers.concrete.relational_words_classifier import RelationalWordsClassifier
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from services.classification.relational_handler import RelationalHandler
from services.classification.word_embedding.concrete.spacy_embedder import SpacyEmbedder
from services.classification.word_embedding.concrete.word2vec_embedder import Word2VecEmbedder
from services.range_handler import RangeHandler
from services.subject_detector import SubjectDetector
from services.text_parser import TextParser
from services.text_partitioner import TextPartitioner


class Embedders(containers.DeclarativeContainer):
    word2vec_embedder = providers.Singleton(Word2VecEmbedder)
    spacy_embedder = providers.Singleton(SpacyEmbedder)


class Services(containers.DeclarativeContainer):
    embedders = providers.DependenciesContainer()

    relational_classifier = providers.Singleton(RelationalWordsClassifier,
                                                word2vec_embedder=embedders.word2vec_embedder)

    relational_handler = providers.Factory(RelationalHandler,
                                           relational_classifier=relational_classifier)

    sentence_classifier = providers.Singleton(SentenceClassifier,
                                              spacy_embedder=embedders.spacy_embedder,
                                              relational_handler=relational_handler)

    range_handler = providers.Factory(RangeHandler,
                                      relational_handler=relational_handler)
    subject_detector = providers.Singleton(SubjectDetector)
    text_partitioner = providers.Singleton(TextPartitioner)
    text_parser = providers.Singleton(TextParser,
                                      subject_detector=subject_detector,
                                      sentence_classifier=sentence_classifier,
                                      range_handler_factory=range_handler.provider,
                                      text_partitioner=text_partitioner)


class Application(containers.DeclarativeContainer):
    embedders = providers.Container(Embedders)

    services = providers.Container(
        Services,
        embedders=embedders
    )
