from flask_restful import fields
from db import db
from services.problem_service import ProblemService
from models.problem import Problem
from models.course import Course
from util import key_generator


class User(db.Model):
    ''' Represents a User '''

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    token = db.Column(db.String, default=key_generator, nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    owned_problems = db.relationship('Problem')
    owned_courses = db.relationship('Course')
    course_participations = db.relationship('CourseParticipation')
    solutions = db.relationship('Solution')

    @property
    def solution_qnt(self):
        return len(self.solutions)

    @property
    def courses(self):
        print([participation.course.name for participation in self.course_participations])
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
        problem = self.problem_service.create_problem(name, description, tip, publish, tags)
        self.owned_problems.append(problem)
        db.session.add(problem)
        problem.add_tests(tests)
        db.session.commit()
        return problem

    def try_solution(self, problem_key, code, tests):
        return self.problem_service.create_solution(self, problem_key, code, tests)
    
    def create_course(self, name, language):
        course = Course(name=name, language=language)
        self.owned_courses.append(course)
        db.session.add(course)
        db.session.commit()
        course.add_member(self)
        return course
