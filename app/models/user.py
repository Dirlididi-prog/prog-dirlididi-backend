from flask_restful import fields
from db import db
from services.problem_service import ProblemService
from models.problem import Problem


class User(db.Model):
    ''' Represents a User '''

    _id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    owned_problems = db.relationship('Problem')

    problem_service = ProblemService()

    api_fields = {
        "id": fields.Integer(attribute='_id'),
        "email": fields.String(),
        "ownedProblems": fields.Nested(Problem.api_fields, attribute='owned_problems')
    }

    def add_problem(self, name, description, tests, tip=None):
        problem = self.problem_service.create_problem(name, description, tip)
        self.owned_problems.append(problem)
        db.session.add(problem)
        problem.add_tests(tests)
        db.session.commit()
        return problem
