from Services.DiffrentiateAdjectives.classifier import Classifier

classifier = Classifier()
adjectives_for_testing = ["heavy","cold","light","great","more","less","big","large","small","warm","cold","enormous","humongous","bulk"]
for adjective in adjectives_for_testing:
    print(f'{adjective} - {classifier.classify_word(adjective).name}')

