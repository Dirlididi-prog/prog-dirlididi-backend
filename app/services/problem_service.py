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
        tests = sorted(problem.tests, key=lambda x: x._id)
        results = sorted(results, key=lambda x: int(x.get('id')))
        print ([(x._id, x.output) for x in tests])
        print (results)

        for i in range(len(results)):
            user_result = results[i]
            key = user_result.get('id')
            user_result = user_result.get('output')
            if int(key) == tests[i]._id:
                if tests[i].output == user_result:
                    result += "."
                else:
                    result += "f"
        return result

    def create_solution(self, user, problem_key, code, tests):
        results = self.check_response(problem_key, tests)
        solution = Solution(user=user._id, problem=problem_key, code=code, tests=tests, result=results, passed="f" not in results)
        db.session.add(solution)
        db.session.commit()
        return solution
