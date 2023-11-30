import json

from flask import Blueprint, abort, Response

from flask_app.decorators.view import includes_body_params
from flask_app.services.json.custom_encoder import CustomEncoder
from flask_app.nlu_pkg.services.sensor_parsing.text_parser import TextParser
from flask_app.nlu_pkg.services.utils.dependency_containers import Application

sensor_bp = Blueprint('sensor', __name__, url_prefix='/sensor')
dependency_injector = Application()
text_parser: TextParser = dependency_injector.services.text_parser()
sentence_key = 'sentence'


@sensor_bp.post('/')
@includes_body_params
def parse_sentence(text):
    # pdb.set_trace()
    try:
        sensors = list(text_parser.parse(text))
    except ValueError as e:
        abort(400, str(e).replace('\"',''))
    else:
        return Response(json.dumps(sensors, cls=CustomEncoder),mimetype='text/json')


