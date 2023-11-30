from dependency_injector import containers, providers
from ...models.pattern_groups.range_patterns_group import RangePatternsGroup
from ...models.pattern_groups.relational_patterns_group import RelationalPatternsGroup
from ...models.pattern_groups.subject_patterns_group import SubjectPatternsGroup
from ..classification.classifiers.concrete.relational_words_classifier import RelationalWordsClassifier
from ..classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from ..classification.relational_handler import RelationalHandler
from ..classification.word_embedding.concrete.spacy_embedder import SpacyEmbedder
from ..classification.word_embedding.concrete.word2vec_embedder import Word2VecEmbedder
from ..pattern_matching.pattern_handlers.relational_pattern_handler import RelationalPatternHandler
from ..sensor_parsing.duration_handler import DurationHandler
from ..sensor_parsing.range_handler import RangeHandler
from ..sensor_parsing.subject_detector import SubjectDetector
from ..sensor_parsing.text_parser import TextParser
from ..sensor_parsing.text_partitioner import TextPartitioner


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

    relational_match_handler = providers.Factory(RelationalPatternHandler,
                                                 relational_classifier=classifiers.relational)

    relational_patterns_group = providers.Singleton(RelationalPatternsGroup,
                                                    relational_pattern_factory=relational_match_handler.provider)

    relational_handler = providers.Factory(RelationalHandler,
                                           relational_patterns=relational_patterns_group)

    range_patterns_group = providers.Singleton(RangePatternsGroup)

    range_handler = providers.Factory(RangeHandler,
                                      relational_handler=relational_handler,
                                      range_patterns=range_patterns_group)

    subject_patterns_group = providers.Singleton(SubjectPatternsGroup)

    subject_detector = providers.Singleton(SubjectDetector,
                                           subject_patterns=subject_patterns_group)

    text_partitioner = providers.Singleton(TextPartitioner,
                                           subject_detector=subject_detector)

    duration_handler = providers.Singleton(DurationHandler,
                                           range_handler_factory=range_handler.provider)

    text_parser = providers.Singleton(TextParser,
                                      sentence_classifier=classifiers.sentence,
                                      text_partitioner=text_partitioner,
                                      subject_detector=subject_detector,
                                      duration_handler=duration_handler,
                                      range_handler_factory=range_handler.provider)


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
