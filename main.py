from services.dependency_container import DependencyContainer
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier

# TODO: change access modifiers to private or protected respectively
if __name__ == '__main__':
    container = DependencyContainer()
    sentence_classifier: SentenceClassifier = container.sentence_classifier_singleton()
    sentences = [
        "The temperature in the oven can be set anywhere from 200 to 450 degrees Fahrenheit.",
        "The speed limit on the highway ranges from 55 to 70 miles per hour depending on the section.",
        "The age group for this competition is between 18 and 30 years old.",
        "The price of the car varies, with classification_models ranging from $20,000 to $40,000.",
        "The pH level of the solution should be maintained within a range of 6.5 to 7.5 for optimal results.",
        "The number of participants in the marathon typically falls within the range of 1,000 to 1,500 runners.",
        "The battery life of the smartphone can last anywhere from 8 to 16 hours, depending on usage.",
        "The annual rainfall in this region fluctuates between 40 and 60 inches.",
        "The weight of the cargo must be within the range of 500 to 1,000 kilograms for safe transportation.",
        "The dosage of the medication should be administered in the range of 2 to 4 pills per day, as prescribed by the doctor.",
        "The car's tire pressure is set at 32 PSI.",
        "The room temperature is maintained at 72 degrees Fahrenheit.",
        "The coffee machine brews coffee with a water temperature of 200 degrees Fahrenheit.",
        "The weight of the package is 3 kilograms.",
        "The battery capacity of the smartphone is 4000 milliampere-hours (mAh).",
        "The length of the bookshelf is 6 feet.",
        "The screen resolution of the monitor is 1920x1080 pixels.",
        "The pH level of the swimming pool water is 7.2.",
        "The speed of the internet connection is 100 megabits per second (Mbps).",
        "The voltage of the electrical outlet is 120 volts.",
        "engine heat between 50 and 100",
        "engine heat is 50",
        "engine heat 50",
        "engine heat 50 and 100",
        "the parameter value can vary between 50 and 100",
        "the parameter is exactly 50",
        "the parameter can be greater than 78 but also smaller than 98",
        "the parameter can be either 5 or 10",
        "the parmter betwen 50 and 100",
        "the parmter is 50",
    ]
    for sentence in sentences:
        item = sentence_classifier.classify_item(sentence)
        print(item.name, sentence)
