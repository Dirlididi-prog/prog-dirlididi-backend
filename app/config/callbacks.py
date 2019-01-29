from flask import request, jsonify, redirect, url_for
from exceptions import DirlididiBaseException, MissingAttribute, Unauthorized
from functools import wraps
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from flask_dance.contrib.google import google

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

def google_auth_required(f):
    def wrapper(*args, **kwargs):
        if not google.authorized:
            return redirect(url_for("google.login"))
        try:
            resp = google.get("/oauth2/v2/userinfo")
            if resp.ok:
                return f(*args, **kwargs)
            else:
                return redirect(url_for("google.login"))
        except TokenExpiredError:
            return redirect(url_for("google.login"))
    return wrapper