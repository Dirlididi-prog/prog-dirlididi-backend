from flask_restful import fields
from db import db
from services.problem_service import ProblemService
from models.problem import Problem
from models.course import Course
from util import key_generator


class User(db.Model):
    ''' Represents a User '''

    required_attributes = ["email", "password"]

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    token = db.Column(db.String, default=key_generator, nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    auth_email = db.Column(db.String(100), db.ForeignKey('user_auth.email'))
    auth = db.relationship('UserAuth', foreign_keys=[auth_email])
    admin = db.Column(db.Boolean, default=False, nullable=False)
    owned_problems = db.relationship('Problem')
    owned_courses = db.relationship('Course')
    course_participations = db.relationship('CourseParticipation')
    solutions = db.relationship('Solution')

    @property
    def solution_qnt(self):
        return len(self.solutions)

    @property
    def courses(self):
        return [participation.course for participation in self.course_participations]

    problem_service = ProblemService()

    api_fields = {
        "id": fields.Integer(attribute='_id'),
        "token": fields.String,
        "email": fields.String,
        "ownedProblems": fields.Nested(Problem.api_fields, attribute='owned_problems'),
        "name": fields.String
    }

    def add_problem(self, name, description, tip, publish, tests, tags=None):
        problem = self.problem_service.create_problem(name, description, tip, tags)
        self.owned_problems.append(problem)
        db.session.add(problem)
        problem.add_tests(tests)
        if publish:
            self.problem_service.create_publish_request(problem)
        db.session.commit()
        return problem

    def try_solution(self, problem_key, code, tests):
        solution = self.problem_service.create_solution(self, problem_key, code, tests)
        for participation in self.course_participations:
            participation.course.add_solution(solution)
        db.session.commit()
        return solution
    
    def create_course(self, name, description, language=None, problems=None):
        if problems:
            course = Course(name=name, description=description, language=language, _problems=problems)
        else:
            course = Course(name=name, description=description, language=language)
        self.owned_courses.append(course)
        db.session.add(course)
        db.session.commit()
        course.add_member(self)
        return course


class UserAuth(db.Model):
    
    email = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'))
    user = db.relationship('User', foreign_keys=[user_id])