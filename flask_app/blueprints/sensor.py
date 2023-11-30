import json

from flask import Blueprint, abort, Response

from ..decorators.view import includes_body_params
from ..services.json.custom_encoder import CustomEncoder
from ..nlu_pkg.services.sensor_parsing.text_parser import TextParser
from ..nlu_pkg.services.utils.dependency_containers import Application

sensor_bp = Blueprint('sensor', __name__, url_prefix='/sensor')
dependency_injector = Application()
text_parser: TextParser = dependency_injector.services.text_parser()


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


