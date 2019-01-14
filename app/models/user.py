from flask_restful import fields
from db import db
from services.problem_service import ProblemService
from models.problem import Problem
from util import key_generator

class User(db.Model):
    ''' Represents a User '''

    _id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, default=key_generator, nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    owned_problems = db.relationship('Problem')
    solutions = db.relationship('Solution')

    problem_service = ProblemService()

    api_fields = {
        "id": fields.Integer(attribute='_id'),
        "token": fields.String(),
        "email": fields.String(),
        "ownedProblems": fields.Nested(Problem.api_fields, attribute='owned_problems')
    }

    def add_problem(self, name, description, tip, publish, tests):
        problem = self.problem_service.create_problem(name, description, tip, publish)
        self.owned_problems.append(problem)
        db.session.add(problem)
        problem.add_tests(tests)
        db.session.commit()
        return problem

    def try_solution(self, problem_key, code, tests):
        return self.problem_service.create_solution(self, problem_key, code, tests)
