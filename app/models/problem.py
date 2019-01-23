from flask_restful import fields
from db import db
from util import key_generator
from datetime import datetime

class ProblemTest(db.Model):
    ''' Represents a test for a problem '''

    required_attributes = ["input", "output"]

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    tip = db.Column(db.String(50), nullable=True)
    publish = db.Column(db.Boolean(), default=False, nullable=False)
    input = db.Column(db.String(50))
    output = db.Column(db.String(50))
    problem = db.Column(db.String(9), db.ForeignKey('problem.key'), nullable=False)
    created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    

    api_fields = {
        "name":fields.String,
        "tip":fields.String,
        "input": fields.String,
        "publish": fields.Boolean,
        "output": fields.String,
        "id": fields.String(attribute="_id"),
        "created": fields.DateTime(dt_format='iso8601')
    }
    

class Problem(db.Model):
    ''' Represents a programming question '''

    required_attributes = ["name", "description", "tests"]

    key = db.Column(db.String(9), default=key_generator, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    publish = db.Column(db.Boolean(), default=False, nullable=False)
    tip = db.Column(db.String(50), nullable=True)
    tests = db.relationship('ProblemTest')
    owner = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)
    courses = db.Column(db.Integer, db.ForeignKey('course._id'))
    solutions = db.relationship('Solution')
    created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    _tags = db.Column(db.PickleType)

    @property
    def tags(self):
        return self._tags if self._tags else []

    api_fields = {
        "key": fields.String,
        "name": fields.String,
        "description": fields.String,
        "tip": fields.String,
        "publish": fields.Boolean,
        "tests": fields.Nested(ProblemTest.api_fields),
        "tags": fields.List(fields.String),
        "created": fields.DateTime(dt_format='iso8601')
    }

    def add_tags(self, tags):
        tags = set(tags)
        if self._tags:
            for tag in tags.difference(self._tags):
                self._tags.append(tag)
        else:
            self._tags = tags

    def add_tests(self, tests):
        for test in tests:
            name = test.get('name')
            tip = test.get('tip')
            input = test.get('input')
            output = test.get('output')
            publish = test.get('publish')
            test_to_append = ProblemTest(name=name, tip=tip, input=input, output=output, publish=publish)
            self.tests.append(test_to_append)
            db.session.add(test_to_append)

class Solution(db.Model):
    ''' Represents a possible solution for a problem '''

    required_attributes = ['tests', 'code', 'key', 'token']

    _id = db.Column(db.Integer, primary_key=True)
    tests = db.Column(db.PickleType, nullable=False)
    code = db.Column(db.Text, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user._id'))
    problem = db.Column(db.ForeignKey('problem.key'))
    result = db.Column(db.String, nullable=False)
    passed = db.Column(db.Boolean)

    api_fields = {
        "tests": {"key": fields.Integer, "output": fields.String},
        "code": fields.String,
        "result": fields.String,
        "passed": fields.Boolean,
        "user": fields.String,
        "problem": fields.String,
    }
