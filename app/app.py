from sys import argv
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources import ProblemDetail, ProblemList, UserAuth
from resources import UserDetail, SolveProblem, CourseCRUD, CourseIdDetail
from resources import CourseTokenDetail, UserCourses, Info

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = 'testing'

api.add_resource(ProblemList, '/problem')
api.add_resource(ProblemDetail, '/problem/<string:key>')
api.add_resource(UserAuth, '/auth')
api.add_resource(UserCourses, '/user/courses')
api.add_resource(UserDetail, '/user')
api.add_resource(SolveProblem, '/solve')
api.add_resource(CourseCRUD, '/course')
api.add_resource(CourseIdDetail, '/course/id/<int:id>')
api.add_resource(CourseTokenDetail, '/course/token/<string:token>')
api.add_resource(Info, '/info')

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
