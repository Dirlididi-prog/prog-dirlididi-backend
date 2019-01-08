from db import db
from models import Problem, ProblemTest

class ProblemService(object):

    def create_exercise(self, name, description, tip, tests):
        problem = Problem(name=name, description=description, tip=tip)
        problem.add_tests(tests)
        db.session.add(problem)
        db.session.commit()
        return problem

    def get_exercise_by_key(self, key):
        return Problem.query.get(key)
    
    def get_all(self):
        return Problem.query.all()