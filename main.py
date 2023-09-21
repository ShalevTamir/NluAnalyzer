from models.requirement_param import RequirementParam
from services.utils.dependency_containers import Application

# TODO: change sentences to tuples
if __name__ == '__main__':
    container = Application()
    sentence_parser = container.services.sentence_parser()
    sentence_subject_pairs = [
        ('Engine heat is greater than 100 and smaller than 100','Engine heat'),
        ('Engine heat is between 100 and 200', 'Engine heat'),
        ('Engine heat in range 100-200', 'Engine heat'),
        ('Engine heat is greater than 50', 'Engine heat'),
        ('The parameter may be stronger than 100', 'parameter'),
        ('The temperature in the oven can be set anywhere from 200 to 450 degrees Fahrenheit.', 'temperature'),
        ('The speed limit on the highway ranges from 55 to 70 miles per hour depending on the section.', 'speed limit'),
        ('The age group for this competition is between 18 and 30 years old.', 'age group'),
        ('The price of the car varies, with classification_models ranging from $20,000 to $40,000.', 'price'),
        ('The pH level of the solution should be maintained within a range of 6.5 to 7.5 for optimal results.',
         'pH level'),
        ('The number of participants in the marathon typically falls within the range of 1,000 to 1,500 runners.',
         'number'),
        (
        'The battery life of the smartphone can last anywhere from 8 to 16 hours, depending on usage.', 'battery life'),
        ('The annual rainfall in this region fluctuates between 40 and 60 inches.', 'annual rainfall'),
        ('The weight of the cargo must be within the range of 500 to 1,000 kilograms for safe transportation.',
         'weight'),
        (
        'The dosage of the medication should be administered in the range of 2 to 4 pills per day, as prescribed by the doctor.',
        'dosage'),
        ("The car's tire pressure is set at 32 PSI.", "tire pressure"),
        ('The room temperature is maintained at 72 degrees Fahrenheit.', 'room temperature'),
        ('The coffee machine brews coffee with a water temperature of 200 degrees Fahrenheit.', 'coffee machine'),
        ('The weight of the package is 3 kilograms.', 'weight'),
        ('The battery capacity of the smartphone is 4000 milliampere-hours (mAh).', 'battery capacity'),
        ('The length of the bookshelf is 6 feet.', 'length'),
        ('The screen resolution of the monitor is 1920x1080 pixels.', 'screen resolution'),
        ('The pH level of the swimming pool water is 7.2.', 'pH level'),
        ('The speed of the internet connection is 100 megabits per second (Mbps).', 'speed'),
        ('The voltage of the electrical outlet is 120 volts.', 'voltage'),
        ('engine heat between 50 and 100', 'engine heat'),
        ('engine heat is 50', 'engine heat'),
        ('engine heat 50', 'engine heat'),
        ('engine heat 50 and 100', 'engine heat'),
        ('the parameter value can vary between 50 and 100', 'parameter value'),
        ('the parameter is exactly 50', 'parameter'),
        ('the parameter can be greater than 78 but also smaller than 98', 'parameter'),
        ('the parameter can be either 5 or 10', 'parameter'),
        ('the parmter betwen 50 and 100', 'parmter'),
        ('the parmter is 50', 'parmter'),
        ('parameter between 100-200', 'parameter'),
        ('parameter between 50-100', 'parameter'),
        ('engine heat needs to be with 100 degrees', 'engine heat'),
        ('engine heat is 100 degrees', 'engine heat'),
        ('engine heat is greater than 5', 'engine heat'),
        ('the parameter in question should be larger than 5KW', 'parameter'),
        ('altitude should be greater than 50', 'altitude'),
        ('engine heat higher than 20 and also smaller than 20', 'engine heat'),
        ('engine heat higher than 10 but also smaller than 20','engine heat'),
        ('The dog started flying within 20 - 50', 'dog')
    ]
    count_successful = 0
    for sentence in sentence_subject_pairs:
        #try:
        sensor = sentence_parser.parse(sentence[0])
            #if sensor.parameter_name == sentence[1].lower():
        count_successful += 1
            #else:
            #    print(
            #        f"FAILED DETECTING SUBJECT, correct subject: {sentence[1]}, detected subject: {sensor.parameter_name}, sentence {sentence}")
        # except ValueError as e:
        #     if "Invalid sentence" in str(e):
        #         count_successful+=1
        #     print(e)
    print(f"accuracy {count_successful / len(sentence_subject_pairs)}")
