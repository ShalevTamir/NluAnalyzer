import json
import pdb

from flask import Blueprint, abort

from flask_app.decorators.view import includes_body_params
from flask_app.services.json.custom_encoder import CustomEncoder
from services.text_parser import TextParser
from services.utils.dependency_containers import Application

sensor_bp = Blueprint('sensor', __name__, url_prefix='/sensor')
dependency_injector = Application()
text_parser: TextParser = dependency_injector.services.text_parser()
sentence_key = 'sentence'


@sensor_bp.post('/')
@includes_body_params
def parse_sentence(sentence):
    # pdb.set_trace()
    try:
        sensors = text_parser.parse(sentence)
    except ValueError as e:
        abort(400, str(e).replace('\"',''))
    else:
        return json.dumps(sensors, cls=CustomEncoder)


