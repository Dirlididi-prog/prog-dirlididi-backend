from flask import request
from flask_restful import Resource, marshal_with
from services import ProblemService
from models import Problem


class ProblemDetail(Resource):

    exercise_service = ProblemService()

    @marshal_with(Problem.api_fields)
    def get(self, key):
        return self.exercise_service.get_exercise_by_key(key)



class ProblemList(Resource):

    exercise_service = ProblemService()
    @marshal_with(Problem.api_fields)
    def get(self):
        return self.exercise_service.get_all()

    @marshal_with(Problem.api_fields)
    def post(self):
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')
        tip = data.get('tip')
        tests = data.get('tests')

        return self.exercise_service.create_exercise(name, description, tip, tests)
        
