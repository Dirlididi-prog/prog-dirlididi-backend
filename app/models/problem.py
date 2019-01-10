from flask_restful import fields
from db import db
from util import key_generator

class ProblemTest(db.Model):
    ''' Represents a test for a problem '''

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    tip = db.Column(db.String(50), nullable=True)
    input = db.Column(db.String(50))
    output = db.Column(db.String(50))
    problem = db.Column(db.String(9), db.ForeignKey('problem.key'), nullable=False)

    api_fields = {
        "name":fields.String,
        "tip":fields.String,
        "input": fields.String,
        "output": fields.String,
    }
    

class Problem(db.Model):
    ''' Represents a programming question '''

    key = db.Column(db.String(9), default=key_generator, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tip = db.Column(db.String(50), nullable=True)
    tests = db.relationship('ProblemTest')
    owner = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)

    api_fields = {
        "key": fields.String,
        "name": fields.String,
        "description": fields.String,
        "tip": fields.String,
        "tests": fields.Nested(ProblemTest.api_fields)
    }

    def add_tests(self, tests):
        for test in tests:
            name = test.get('name')
            tip = test.get('tip')
            input = test.get('input')
            output = test.get('output')
            test_to_append = ProblemTest(name=name, tip=tip, input=input, output=output)
            self.tests.append(test_to_append)
            db.session.add(test_to_append)
