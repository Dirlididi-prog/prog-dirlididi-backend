from flask import request, jsonify
from exceptions import DirlididiBaseException, MissingAttribute
from functools import wraps


def define_api_callbacks(app):

    @app.errorhandler(DirlididiBaseException)
    def handle_bad_request(e):
        return jsonify({"message": e.message}), e.status_code

    @app.before_request
    def verify_json():
        if not request.method == 'GET' and not request.is_json:
            return jsonify({"message" : "Missing JSON in request"}), 400


class verify_attributes(object):

    def __init__(self, attributes):
        self.attributes = attributes

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request_json = request.get_json()
            for attr in self.attributes:
                if attr not in request_json:
                    raise MissingAttribute("Missing attribute: {}".format(attr))
            return f(*args, **kwargs)
    
        return wrapper
