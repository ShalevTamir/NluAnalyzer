from services.dependency_container import DependencyContainer
from services.classifier import Classifier
from services.nlu_service import RangeAnalyzer
from services.subject_detector import SubjectDetector


def register_dependencies():
    DependencyContainer.register(Classifier)
    DependencyContainer.register(SubjectDetector)
    DependencyContainer.register(RangeAnalyzer)


if __name__ == '__main__':
    register_dependencies()
    range_analyzer = DependencyContainer.get_instance(RangeAnalyzer)
    #TODO: save sentences that passed
    parameter_sentences = [
        "Altitude can range from sea level to the 50,000 feet.",
        "Longitude may vary between the -180 degrees (west) and 180 degrees (east).",
        "Wind_Speed falls in the range of 0 to 100 knots.",
        "The Engine_Heat can be as low as 0 degrees Celsius and as high as 300 degrees Celsius.",
        "The Air_Pressure at sea level typically ranges from 800 to 1100 hPa.",
        "The Current_Thrust can vary from no thrust (0 kN) to full power (400 kN).",
        "A steep climb or descent of 20 degrees is within the range of the Pitch_Angle.",
        "Roll_Angle may oscillate from a maximum left roll of -60 degrees to a maximum right roll of 60 degrees.",
        "Fuel_Consumption can be minimal at 0 liters or reach a maximum of 100 liters.",
        "Ground_Speed may vary from a standstill (0 knots) to a rapid 700 knots.",
        "A rapid climb or descent of 3000 feet per minute is within the range of the Vertical_Speed.",
        "The parameter Tempreture can vary significantly, from a frigid -50 degrees Celsius to a scorching 100 degrees Celsius.",
        "G-Force typically stays within the range of 0 to 5 Gs.",
        "The Radio_Signal_Strength can be as strong as 0 dBm or as weak as -100 dBm.",
        "The GPS_Accuracy can vary from pinpoint accuracy of 0 meters to a less precise 10 meters.",
        "The Oxygen_Level may range from dangerously low (0%) to a safe and breathable 100%.",
        "Flap_Position can vary from fully retracted (0 degrees) to fully extended (40 degrees).",
        "Hydraulic_Pressure can fluctuate between 0 PSI (no pressure) and a substantial 3000 PSI.",
        "Brake_Pressure is either applied (1) or not applied (0).",
        "Landing_Lights can be either 1 or 0.",
        "Strobe_Lights can be either 1 or 0.",
        "Beacon_Lights can be either 1 or 0.",
        "Navigation_Lights can be either 1 or 0.",
        "Anti_Collision_Lights can be either 1 or 0.",
        "Wing_Lights can be either 1 or 0.",
        "Cabin_Lights can be either 1 or 0.",
        "Emergency_Lights can be either 1 or 0.",
        "Correlator is a pure number with no specified range.",
        "engine_heat is less than 50",
        "speed more than 50",
        "altitude is colder than 100",
        "altitude equals to 5",
        "when height is bigger 8",
        "the sensor is active only when rpm_rpt is bigger than 8 and smaller than 10"

    ]
    for sentence in parameter_sentences:
        range_analyzer.parse_sentence(sentence)
