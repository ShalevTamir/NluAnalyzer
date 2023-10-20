import json
from flask_app.services.json.custom_encoder import CustomEncoder
from services.text_parser import TextParser
from services.utils.dependency_containers import Application

# TODO: change sentences to tuples
# TODO: negative and doubles
if __name__ == '__main__':
    container = Application()
    text_parser: TextParser = container.services.text_parser()
    parameters = [
        "the table's length is in range 5cm-20cm",
        "the sensor should be above than 10 and under than 27",
        "tempareture between 50",
        "The recommended daily_intake of calcium for adults is around 1,000- 1,200 milligrams.",
        "the sensor should be in the range of 500 -1000",
        "The 454 parameters have a temperature of 5",
        "The speed_limit is 40. 50",
        "The speed_limit on this road is between 40 and 174,200 miles per hour.",
        "The recommended daily_caloric intake for an adult is around -2,000 calories.",
        "The acceptable humidity_range for indoor comfort is 30% to 60%.",
        "The voting_age in most countries is typically 18 years.",
        "The recommended daily_water_intake for an adult is 8 glasses or 64 ounces.",
        "The legal blood_alcohol_concentration_limit for driving in many places is 0.08%.",
        "The average human body_temperature is around 98.6 degrees Fahrenheit.",
        "A healthy adult's heart_rate at rest is usually between 60 and 100 beats per minute.",
        "The maximum payload_capacity of this truck is 2,000 pounds.",
        "The standard atmospheric_pressure at sea level is 101.3 kilopascals.",
        "The Earth's circumference is approximately 24,901 miles.",
        "The distance from the Earth to the Moon is about 238,855 miles on average.",
        "The recommended serving_size for this cereal is 1 cup.",
        "The voltage of a standard household electrical outlet is 120 volts.",
        "The ideal temperature for storing red wine is 55 degrees Fahrenheit.",
        "The width of a standard piece of letter-sized paper is 8.5 inches.",
        "A typical car's fuel efficiency on the highway is 30 miles per gallon.",
        "The melting_point of water at standard atmospheric pressure is 32 degrees Fahrenheit.",
        "The density of lead is 11.34 grams per cubic centimeter.",
        "The legal driving_age in most states is 16 years.",
        "The recommended daily_intake of fiber for adults is 25 grams.",
        "The acceptable noise_level in a residential area is typically 50 decibels during the day.",
        "The maximum_takeoff_weight of a Boeing 737 is around 174,200 pounds.",
        "The average gestation_period for a human pregnancy is approximately 40 weeks.",
        "The Earth's equatorial_radius is about 3,963 miles.",
        "The recommended daily_allowance of vitamin C for adults is 90 milligrams for men and 75 milligrams for women.",
        "The standard_deviation is a measure of the amount of variation or dispersion in a set of data.",
        "The legal blood_pressure range for an adult is typically 90 mm Hg to 120 mm Hg.",
        "The boiling_point of water at standard atmospheric pressure is 212 degrees Fahrenheit.",
        "The average_depth of the world's oceans is roughly 12,080 feet.",
        "The speed_of_light in a vacuum is approximately 299,792,458 meters per second.",
        "The minimum_wage in the United States varies by state but is typically around $7.25 per hour.",
        "The diameter of the Sun is about 864,340 miles.",
        "The Earth's orbital_eccentricity ranges from 0.0025 to 0.0679.",
        "The recommended daily_sodium_intake for adults is an upper limit of 2,300-2,500 milligrams.",
        "The duration of a full moon phase is approximately 29.5 days.",
        "The maximum height for a toddler to safely use a car booster seat is typically 57 inches.",
        "The standard American_football_field is 100 yards long.",
        "The altitude of the highest mountain, Mount Everest, is 29,032 feet.",
        "The legal_limit for blood alcohol concentration for pilots is 0.04% in many countries.",
        "The radius of a standard compact disc (CD) is 4.72 inches.",
        "The typical lifespan of a housefly is around 28 days.",
        "The recommended_tire_pressure for a car's tires is typically 32-35 pounds per square inch (psi).",
        "The atmospheric_pressure on Mars is about 610 pascals, significantly lower than Earth's.",
        "The average adult_human_body contains about 5 liters of blood.",
        "The recommended daily_intake of calcium for adults is around 1,000-1,200 milligrams.",
        "The range of human_hearing is approximately 20 to 20,000 hertz (Hz).",
        "The Earth's mass is approximately 5.972 × 10^24 kilograms.",
        "The maximum diving_depth for recreational scuba diving is often limited to 130 feet.",
        "The legal_age to purchase alcohol in most countries is 18 or 21.",
        "The time it takes for the International Space Station (ISS) to orbit Earth is roughly 90 minutes.",
        "The speed_of_sound in dry air at room temperature is approximately 343 meters per second.",
        "The recommended daily_intake of iron for adult men is 8 milligrams and 18 milligrams for adult women.",
        "The maximum_occupancy of this building is 500 people.",
        "The diameter of the Moon is about 2,159 miles.",
        "The typical shelf_life of canned goods is 1 to 5 years.",
        "The ideal_temperature for a refrigerator is around 37 degrees Fahrenheit.",
        "The Earth's escape_velocity is about 25,020 miles per hour.",
        "The legal_limit for commercial airline pilots' blood alcohol concentration is 0.04%.",
        "The maximum luggage weight for carry-on bags on most flights is 40 pounds.",
        "The minimum voting_age in some countries is 16 years.",
        "The recommended daily_intake of potassium for adults is around 2,000-4,000 milligrams.",
        "The standard_length of a soccer field is 100-130 yards.",
        "The depth of the Mariana Trench, the deepest point in the world's oceans, is approximately 36,070 feet.",
        "The legal_limit for blood alcohol concentration for most non-commercial drivers is 0.08% in many places.",
        "The Earth's polar radius is roughly 3,949 miles.",
        "The average walking_speed for a human is about 3-4 miles per hour.",
        "The recommended daily_intake of protein for adults is approximately 46-56 grams for men and 46-50 grams for women.",
        "The duration of a typical human sleep cycle is around 90 minutes.",
        "The average_weight of a newborn baby is about 7.5 pounds."
    ]

    for sentence in parameters:
        try:
            # print(extract_word_pos_tags(sentence))
            sensor = text_parser.parse(sentence)
            print(f"Sentence {sentence}", f"Sensor {json.dumps(sensor, cls=CustomEncoder)}", sep='\n', end='\n\n')
        except ValueError as e:
            print(e)
