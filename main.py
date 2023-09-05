from Services.DependencyContainer import DependencyContainer
from Services.DiffrentiateAdjectives.classifier import Classifier

def register_dependencies():
    DependencyContainer.register(Classifier)

if __name__ == '__main__':
    register_dependencies()
    classifier = DependencyContainer.get_instance(Classifier)
    adjectives_for_testing = ["heavy", "cold", "light", "great", "more", "less", "big", "large", "small", "warm",
                              "cold",
                              "enormous", "humongous", "bulk"]
    for adjective in adjectives_for_testing:
        print(f'{adjective} - {classifier.classify_word(adjective).name}')
