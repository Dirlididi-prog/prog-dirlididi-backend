from sys import argv
from flask import Flask
from flask_restful import Api
from db import db
from resources import ProblemDetail, ProblemList

app = Flask(__name__)
api = Api(app)

api.add_resource(ProblemList, '/problem')
api.add_resource(ProblemDetail, '/problem/<string:key>')


if __name__ == "__main__":
    if "test" in argv:
        import pytest
        db.init_app(app)
        db.app = app
        db.create_all()
        pytest.main(['tests'])
    else:
        db.init_app(app)
        db.app = app
        db.create_all()
        app.run(host="0.0.0.0", debug=True)