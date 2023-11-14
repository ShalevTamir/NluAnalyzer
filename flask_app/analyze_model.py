import json
import logging

from spacy import displacy

from flask_app.nlu_pkg.services.sensor_parsing.text_parser import TextParser
from flask_app.nlu_pkg.services.utils.dependency_containers import Application
from flask_app.services.json.custom_encoder import CustomEncoder

# TODO: handle unable to parse string x to a valid number, instead of just throwing it
# TODO: initiate range stuff on startup, instead on the first range parse request

# TODO: add option to use units and parsing still works
container = Application()
text_parser: TextParser = container.services.text_parser()


icd_parameters = [
    "The Beacon_Lights are either Off (0) or On (1). Moreover, the Navigation_Lights are either Off (0) or On (1); and the Anti_Collision_Lights are either Off (0) or On (1).",
    "The Altitude is between 0 and 50,000 feet. Additionally, the Longitude is within the range of -180 to 180 degrees; and the Wind_Speed ranges from 0 to 100 knots.",
    "The Engine_Heat is within the range of 0 to 300 degrees Celsius. Moreover, the Air_Pressure falls between 800 and 1,100 hPa; and the Current_Thrust varies from 0 to 400 kN.",
    "The Pitch_Angle is between -20 and 20 degrees. Furthermore, the Roll_Angle is within the range of -60 to 60 degrees; and the Fuel_Consumption ranges from 0 to 100 liters.",
    "The Ground_Speed varies from 0 to 700 knots. Similarly, the Vertical_Speed is between -3,000 and 3,000 feet per minute; and the Tempreture is in the range of -50 to 100 degrees Celsius.",
    "The G-Force is between 0 and 5 G. In addition, the Radio_Signal_Strength is within the range of -100 to 0 dBm; and the GPS_Accuracy falls between 0 and 10 meters.",
    "The Oxygen_Level ranges from 0 to 100%. Also, the Flap_Position varies from 0 to 40 degrees; and the Hydraulic_Pressure is within the range of 0 to 3,000 PSI.",
    "The Brake_Pressure is above 0 and below 2,000 degrees. Besides, the Landing_Lights are either Off (0) or On (1); and the Strobe_Lights are either Off (0) or On (1).",
    "The Wing_Lights are either Off (0) or On (1). Additionally, the Cabin_Lights are either Off (0) or On (1); and the Emergency_Lights are either Off (0) or On (1)."
]

for sentence in icd_parameters:
    # try:

    # print(extract_word_pos_tags(sentence))
    sensors = list(text_parser.parse(sentence))
    # if isinstance(range, tuple) and sensor.requirement_param.__class__ == RequirementRange:
    #     requirement_range: RequirementRange = sensor.requirement_param
    #     if requirement_range.value != range[0] or requirement_range.end_value != range[1]:
    #         logging.error(f"Wrong evaluation of sentence {sentence}, evaluated {(requirement_range.value, requirement_range.end_value)} but is actually {range}")
    # elif isinstance(range, int) and sensor.requirement_param.__class__ == RequirementParam:
    #     if sensor.requirement_param.value != range:
    #         logging.error(f"Wrong evaluation of sentence {sentence}, evaluated {sensor.requirement_param.value} but is actually {range[0]}")
    # else:
    #     logging.error(f"Wrong evaluation of sentence {sentence}, evaluated {json.dumps(sensor, cls=CustomEncoder)} but is actually {range}")

    print(f"Sentence {sentence}", f"Sensor {json.dumps(sensors, cls=CustomEncoder)}", sep='\n', end='\n\n')
# except ValueError as e:
#    print(e ,end='\n\n')
