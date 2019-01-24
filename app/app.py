from sys import argv, exit
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config.callbacks import define_api_callbacks
from db import db
from resources import ProblemDetail, ProblemList, UserAuth
from resources import UserDetail, SolveProblem, CourseCRUD, CourseIdDetail
from resources import CourseTokenDetail, UserCourses, Info, AdminPublishRequests


POPULATE = True

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
cors = CORS(app)

app.config['JWT_SECRET_KEY'] = 'testing'
define_api_callbacks(app)


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
api.add_resource(AdminPublishRequests, '/admin/publish-request')

if __name__ == "__main__":
    if "test" in argv:
        import pytest
        db.init_app(app)
        db.app = app
        db.create_all()
        code = pytest.main(['tests'])
        exit(code)
    else:
        if POPULATE:
            from dev.populate_db import Populator
            Populator().start()
        db.init_app(app)
        db.app = app
        db.create_all()
        app.run(host="0.0.0.0")
