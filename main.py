import json
from flask_app.services.json.custom_encoder import CustomEncoder
from services.text_parser import TextParser
from services.utils.dependency_containers import Application

# TODO: change sentences to tuples
if __name__ == '__main__':
    container = Application()
    text_parser: TextParser = container.services.text_parser()
    parameter_ranges = [
        "The temperature can vary anywhere from zero to 100 degrees Celsius.",
        "The speed of the car ranges between zero and 60 mph.",
        "The pH level should be maintained within the range of five to nine.",
        "The voltage should be within the range of 110 to 120 volts.",
        "Pressure can fluctuate from twenty to 40 psi.",
        "The weight of the product should be between five and ten pounds.",
        "The frequency range for the radio signal is 88-108 MHz.",
        "The time interval can be set anywhere from one to 24 hours.",
        "The concentration of the solution is within the range of 0.1 to 1.0 M.",
        "The distance covered spans from fifty to 100 meters.",
        "Humidity should be maintained at levels between thirty percent and seventy percent.",
        "The size of the screen can range from 5 to 15 inches.",
        "The angle of inclination is adjustable from zero to 90 degrees.",
        "The depth of the water can range from two to five feet.",
        "The volume can be adjusted from zero to 100 decibels.",
        "The resistance of the circuit falls within the range of 10 to 100 ohms.",
        "The concentration of sugar in the solution is in the range of 5-20%.",
        "The wavelength of light is in the range of 400-700 nanometers.",
        "The car's fuel efficiency is somewhere between 20 and 30 miles per gallon.",
        "The duration of the event can vary between two and three hours.",
        "The software can handle files ranging from 1 to 10 megabytes.",
        "The financial interest rate fluctuates between three and five percent.",
        "The pH range of the pool water should be kept between 7.2 and 7.8.",
        "The temperature of the oven can be adjusted from 150 to 450 degrees Fahrenheit.",
        "The price of the product falls between fifty and one hundred dollars.",
        "The diameter of the circle is in the range of 5 to 15 centimeters.",
        "The lifespan of the battery is in the range of two to five years.",
        "The salary for the job is in the range of forty to sixty thousand dollars annually.",
        "The width of the river spans from fifty to one hundred meters.",
        "The pressure in the tire should be within the range of 30 to 35 psi.",
        "The age of the participants falls between eighteen and thirty years.",
        "The length of the book is anywhere from 200 to 300 pages.",
        "The temperature in the greenhouse is maintained at a range of 20-25 degrees Celsius.",
        "The maximum load capacity is between 500 and 1000 kilograms.",
        "The speed limit on the highway is within the range of 55 to 70 miles per hour.",
        "The range of the Wi-Fi signal extends from 50 to 100 feet.",
        "The number of employees in the company is between fifty and one hundred.",
        "The altitude of the mountain ranges from five thousand to ten thousand feet.",
        "The screen resolution is 1080p, with a pixel count of 1920x1080.",
        "The memory storage capacity ranges from sixteen to sixty-four gigabytes.",
        "The annual rainfall in the region is in the range of 20 to 40 inches.",
        "The calorie content of the food item ranges from 100 to 200 calories.",
        "The voltage output is in the range of twelve to twenty-four volts.",
        "The price of the stock varies from fifty to one hundred dollars per share.",
        "The duration of the movie can range from ninety to 120 minutes.",
        "The dose of the medication can vary from two to four tablets.",
        "The range of acceptable temperatures falls between negative ten to 40 degrees Celsius.",
        "The car's fuel tank can hold between ten to twenty gallons of gas.",
        "The angle of rotation is adjustable from zero to 360 degrees.",
        "The frequency of sound waves spans from 20 to 20,000 Hz.",
        "The weight limit for luggage is within the range of 20 to 50 pounds.",
        "The height of the building ranges from 50 to 100 meters.",
        "The number of students in the classroom is in the range of 20 to 30.",
        "The response time of the monitor is in the range of one to five milliseconds.",
        "The data transfer speed ranges from 10 to 100 megabits per second.",
        "The lifespan of a pet rabbit can vary from five to ten years.",
        "The dosage of the medication ranges from 0.5 to 1 milligrams.",
        "The length of the river ranges from 50 to 100 kilometers.",
        "The width of the road ranges from 3 to 4 meters.",
        "The wavelength of the radio signal spans from 10 to 100 meters.",
        "The voltage input range for the laptop charger is from 110 to 240 volts.",
        "The age group for a children's event is in the range of 3 to 100."
    ]

    for sentence in parameter_ranges:
        try:
            # print(extract_word_pos_tags(sentence))
            sensor = text_parser.parse(sentence)
            print(f"Sentence {sentence}", f"Sensor {json.dumps(sensor, cls=CustomEncoder)}", sep='\n', end='\n\n')
        except ValueError as e:
            print(e)
