from dependency_injector import containers, providers

from services.classification.comparative_adjectives_classification.adjective_classifier import AdjectiveClassifier
from services.classification.comparative_adjectives_classification.adjective_handler import AdjectiveHandler
from services.classification.sentence_classification.sentence_classifier import SentenceClassifier
from services.sentence_parser import SentenceParser
from services.subject_detector import SubjectDetector


class DependencyContainer(containers.DeclarativeContainer):
    adjective_classifier_provider = providers.Singleton(AdjectiveClassifier)
    adjective_handler_provider = providers.Singleton(AdjectiveHandler,
                                                     adjective_classifier=adjective_classifier_provider)
    subject_detector_provider = providers.Singleton(SubjectDetector)
    sentence_parser_provider = providers.Singleton(SentenceParser,
                                                   subject_detector=subject_detector_provider,
                                                   adjective_handler= adjective_handler_provider)
    sentence_classifier_provider = providers.Singleton(SentenceClassifier)