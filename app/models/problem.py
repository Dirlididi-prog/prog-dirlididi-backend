from flask_restful import fields
from db import db
from util import key_generator
from datetime import datetime
from exceptions import Unauthorized

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
        "key": fields.Integer(attribute="_id"),
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

    not_updateable = ["key", "created", "solutions", "courses", "owner", "publish", "publish_request"]

    key = db.Column(db.String(9), default=key_generator, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    publish = db.Column(db.Boolean(), default=False, nullable=False)
    tip = db.Column(db.String(50), nullable=True)
    tests = db.relationship('ProblemTest')
    owner = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)
    courses = db.Column(db.Integer, db.ForeignKey('course._id'))
    solutions = db.relationship('Solution')
    publish_request = db.relationship('PublishRequest')
    created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    _tags = db.Column(db.PickleType)

    @property
    def tags(self):
        return self._tags if self._tags else []

    @tags.setter
    def tags(self, tags):
        self._tags = tags

    api_fields = {
        "key": fields.String,
        "name": fields.String,
        "owner": fields.Integer,
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

    def update(self, data):
        for attr in data.keys():
            if attr == "tests":
                self.delete_all_tests()
                self.add_tests(data[attr])
            elif attr not in self.not_updateable:
                self.__setattr__(attr, data[attr])
        db.session.commit()

    def delete_all_tests(self):
        for test in self.tests:
            db.session.delete(test)
        db.session.commit()

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

    def delete(self, user_id):
        if user_id == self.owner:
            self.delete_all_tests()
            db.session.delete(self)
            db.session.commit()
        else:
            raise Unauthorized("User with id {} is not the owner of this problem".format(user_id))

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


class PublishRequest(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    problem = db.relationship('Problem')
    problem_id = db.Column(db.String, db.ForeignKey('problem.key'))

    api_fields = {
        "id": fields.Integer(attribute="_id"),
        "problem": fields.Nested(Problem.api_fields)
    }

    def accept(self):
        self.problem.publish = True
        db.session.delete(self)
        db.session.commit()
    
    def decline(self):
        db.session.delete(self)
