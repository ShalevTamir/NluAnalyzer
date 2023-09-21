import json

from flask import Blueprint, request, abort

from flask_app.services.json.custom_encoder import CustomEncoder
from services.sentence_parser import SentenceParser
from services.utils.dependency_containers import Application

sensor_bp = Blueprint('sensor', __name__, url_prefix='/sensor')
dependency_injector = Application()
sentence_parser: SentenceParser = dependency_injector.services.sentence_parser()
sentence_key = 'sentence'


@sensor_bp.post('/')
def parse_sentence():
    if len(request.form) == 0 and len(request.data) == 0:
        abort(400, "Sentence argument missing")
    sentence_requested = None
    if len(request.form) > 0:
        sentence_requested = request.form[sentence_key]
    if len(request.data) > 0:
        data = json.loads(request.data)
        sentence_requested = data[sentence_key]
    sensor = None
    try:
        sensor = sentence_parser.parse(sentence_requested)
    except ValueError as e:
        abort(400, str(e))
    else:
        return json.dumps(sensor, cls=CustomEncoder)


