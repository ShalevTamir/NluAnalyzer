from dependency_injector import containers, providers

from models.patterns_matcher.range_matcher import RangeMatcher
from models.patterns_matcher.relational_matcher import RelationalMatcher
from services.classification.classifiers.concrete.relational_words_classifier import RelationalWordsClassifier
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from services.classification.relational_handler import RelationalHandler
from services.classification.word_embedding.concrete.spacy_embedder import SpacyEmbedder
from services.classification.word_embedding.concrete.word2vec_embedder import Word2VecEmbedder
from services.pattern_matching.relational_pattern import RelationalPattern
from services.sensor_parsing.range_handler import RangeHandler
from services.sensor_parsing.subject_detector import SubjectDetector
from services.sensor_parsing.text_parser import TextParser
from services.sensor_parsing.text_partitioner import TextPartitioner


class Embedders(containers.DeclarativeContainer):
    word2vec_embedder = providers.Singleton(Word2VecEmbedder)
    spacy_embedder = providers.Singleton(SpacyEmbedder)


class Classifiers(containers.DeclarativeContainer):
    embedders = providers.DependenciesContainer()
    relational = providers.Singleton(RelationalWordsClassifier,
                                     word2vec_embedder=embedders.word2vec_embedder)
    sentence = providers.Singleton(SentenceClassifier,
                                   spacy_embedder=embedders.spacy_embedder)


class Services(containers.DeclarativeContainer):
    classifiers = providers.DependenciesContainer()

    relational_pattern = providers.Factory(RelationalPattern,
                                           relational_classifier=classifiers.relational)

    relational_matcher = providers.Singleton(RelationalMatcher,
                                             relational_pattern_factory=relational_pattern.provider)

    relational_handler = providers.Factory(RelationalHandler,
                                           relational_matcher=relational_matcher)

    range_matcher = providers.Singleton(RangeMatcher)

    range_handler = providers.Factory(RangeHandler,
                                      relational_handler=relational_handler,
                                      range_matcher=range_matcher)
    subject_detector = providers.Singleton(SubjectDetector)
    text_partitioner = providers.Singleton(TextPartitioner)
    text_parser = providers.Singleton(TextParser,
                                      subject_detector=subject_detector,
                                      sentence_classifier=classifiers.sentence,
                                      range_handler_factory=range_handler.provider,
                                      text_partitioner=text_partitioner)


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
