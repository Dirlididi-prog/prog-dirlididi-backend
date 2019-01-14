from db import db
from models.problem import Problem, Solution


class ProblemService(object):

    def create_problem(self, name, description, tip, publish):
        problem = Problem(name=name, description=description, tip=tip, publish=publish)
        return problem

    def get_problem_by_key(self, key):
        return Problem.query.get(key)
    
    def get_all(self):
        return Problem.query.all()

    def check_response(self, problem, results):
        ''' Returns the test results for a solution '''
        result = ""
        problem = self.get_problem_by_key(problem)
        tests = problem.tests

        for user_result in results:
            key = user_result[0]
            user_result = user_result[1]
            test = self.__get_test(tests, key)
            if test.output == user_result:
                result += "."
            else:
                result += "f"

        return result

    def __get_test(self, tests, key):
        for test in tests:
            if int(test._id) == int(key):
                return test
        return None

    def create_solution(self, user, problem_key, code, tests):
        results = self.check_response(problem_key, tests)
        solution = Solution(user=user._id, problem=problem_key, code=code, tests=tests, result=results, passed="f" not in results)
        db.session.add(solution)
        db.session.commit()
        return solution
