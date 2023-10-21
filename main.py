import json
from flask_app.services.json.custom_encoder import CustomEncoder
from services.text_parser import TextParser
from services.utils.dependency_containers import Application

# TODO: change sentences to tuples
if __name__ == '__main__':
    container = Application()
    text_parser: TextParser = container.services.text_parser()
    parameter_ranges = [
        "The temperature can vary from 0 to 100 degrees Celsius.",
        "The speed of the car ranges from 0 to 60 miles per hour.",
        "The pH level should be maintained within the range of 5 to 9.",
        "The voltage should be within the range of 110 to 120 volts.",
        "Pressure can fluctuate from 20 to 40 psi.",
        "The weight of the product should be between 5 and 10 pounds.",
        "The frequency range for the radio signal is 88-108 MHz.",
        "The time interval can be set from 1 to 24 hours.",
        "The concentration of the solution is within the range of 0.1 to 1.0 M.",
        "The distance covered spans from 50 to 100 meters.",
        "Humidity should be maintained at levels between 30% and 70%.",
        "The size of the screen can range from 5 to 15 inches.",
        "The angle of inclination is adjustable from 0 to 90 degrees.",
        "The depth of the water can range from 2 to 5 feet.",
        "The volume can be adjusted from 0 to 100 decibels.",
        "The resistance of the circuit falls within the range of 10 to 100 ohms.",
        "The concentration of sugar in the solution is in the range of 5-20%.",
        "The wavelength of light is in the range of 400-700 nm.",
        "The car's fuel efficiency is somewhere between 20 and 30 miles per gallon.",
        "The duration of the event can vary between 2 and 3 hours.",
        "The software can handle files ranging from 1 to 10 MB.",
        "The financial interest rate fluctuates between 3 and 5%.",
        "The pH range of the pool water should be kept between 7.2 and 7.8.",
        "The temperature of the oven can be adjusted from 150 to 450 degrees Fahrenheit.",
        "The price of the product falls between $50 and $100.",
        "The diameter of the circle is in the range of 5 to 15 centimeters.",
        "The lifespan of the battery is in the range of 2 to 5 years.",
        "The salary for the job is in the range of $40,000 to $60,000 annually.",
        "The width of the river spans from 50 to 100 meters.",
        "The pressure in the tire should be within the range of 30 to 35 psi.",
        "The age of the participants falls between 18 and 30 years.",
        "The length of the book is anywhere from 200 to 300 pages.",
        "The temperature in the greenhouse is maintained at a range of 20-25 degrees Celsius.",
        "The maximum load capacity is between 500 and 1000 kilograms.",
        "The speed limit on the highway is within the range of 55 to 70 miles per hour.",
        "The range of the Wi-Fi signal extends from 50 to 100 feet.",
        "The number of employees in the company is between 50 and 100.",
        "The altitude of the mountain ranges from 5000 to 10000 feet.",
        "The screen resolution is 1080p, with a pixel count of 1920x1080.",
        "The memory storage capacity ranges from 16 to 64 gigabytes.",
        "The annual rainfall in the region is in the range of 20 to 40 inches.",
        "The calorie content of the food item ranges from 100 to 200 calories.",
        "The voltage output is in the range of 12 to 24 volts.",
        "The price of the stock varies from $50 to $100 per share.",
        "The duration of the movie can range from 90 to 120 minutes.",
        "The dose of the medication can vary from 2 to 4 tablets.",
        "The range of acceptable temperatures falls between -10 to 40 degrees Celsius.",
        "The car's fuel tank can hold between 10 to 20 gallons of gas.",
        "The angle of rotation is adjustable from 0 to 360 degrees.",
        "The frequency of sound waves spans from 20 to 20000 Hz.",
        "The weight limit for luggage is within the range of 20 to 50 pounds.",
        "The height of the building ranges from 50 to 100 meters.",
        "The number of students in the classroom is in the range of 20 to 30.",
        "The response time of the monitor is in the range of 1 to 5 milliseconds.",
        "The data transfer speed ranges from 10 to 100 megabits per second.",
        "The lifespan of a pet rabbit can vary from 5 to 10 years.",
        "The dosage of the medication ranges from 0.5 to 1 milligrams.",
        "The length of the river ranges from 50 to 100 kilometers.",
        "The width of the road ranges from 3 to 4 meters.",
        "The wavelength of the radio signal spans from 10 to 100 meters.",
        "The voltage input range for the laptop charger is from 110 to 240 volts.",
        "The age group for a children's event is in the range of 3 to 12 years.",
        "The temperature range for refrigeration spans from -20 to -5 degrees Celsius.",
        "The salary range for the position is from $60000 to $80000 per year.",
        "The humidity level in the greenhouse falls within the range of 40 to 60 percent.",
        "The weight of a newborn baby ranges from 6 to 8 pounds.",
        "The price of a smartphone ranges from $200 to $500.",
        "The speed of a bicycle can reach from 15 to 25 miles per hour.",
        "The depth of the swimming pool ranges from 5 to 10 feet.",
        "The angle of a camera's lens can be adjusted from 24 to 70 degrees.",
        "The duration of a flight can range from 2 to 4 hours.",
        "The capacity of a storage drive can range from 256 to 512 gigabytes.",
        "The annual precipitation in the desert is within the range of 5 to 15 inches.",
        "The calorie intake for a daily diet ranges from 1500 to 2000 calories.",
        "The voltage output of a power supply ranges from 5 to 12 volts.",
        "The price range for a laptop is from $800 to $1500.",
        "The duration of a concert can vary from 1.5 to 3 hours.",
        "The recommended dose of a vitamin is from 100 to 200 milligrams.",
        "The range of a Wi-Fi router can extend from 100 to 200 meters.",
        "The number of attendees at a conference ranges from 200 to 300.",
        "The altitude of an airplane can vary from 30000 to 40000 feet.",
        "The screen size of a tablet ranges from 7 to 12 inches.",
        "The storage capacity of a hard drive ranges from 1 to 4 terabytes."
    ]
    for sentence in parameter_ranges:
        try:
            # print(extract_word_pos_tags(sentence))
            sensor = text_parser.parse(sentence)
            print(f"Sentence {sentence}", f"Sensor {json.dumps(sensor, cls=CustomEncoder)}", sep='\n', end='\n\n')
        except ValueError as e:
            print(e)
