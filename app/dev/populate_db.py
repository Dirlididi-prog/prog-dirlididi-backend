#condig: utf-8
import requests
import json
from threading import Thread
from time import sleep
from services.user_service import UserService
from services.problem_service import ProblemService
from services.course_service import CourseService


class Populator(Thread):

    def run(self):
        sleep(10)
        populate()


def populate():
    user_payload = {
        "email": "matheus@mat.com",
        "name": "Matheus Melo"
    }

    user_service = UserService()
    course_service = CourseService()
    problem_service = ProblemService()

    user1 = UserService().create_user(email="matheus@mat.com", name="Matheus Melo", admin=True)

    user2 = UserService().create_user(email="charlin@charlle.com", name="Charlle Dias")

    user3 = UserService().create_user(email="esdras@es.com", name="Esdras Vidal")

    course3 = {
        "name": "Ruby para iniciantes",
        "language": "ruby",
        "description": "Para você que tem pouca experiência na linguagem!"
    }

    course4 = {
        "name": "Python > Ruby",
        "language": "python",
        "description": "Falando apenas a verdade."
    }



    course1 = user1.create_course(name="Algoritmo", description="Curso básico de algoritmos")
    course2 = user2.create_course(name="Python avançado", description="Curso avançado de Python", language="python")
    course3 = user3.create_course(name="Ruby para iniciantes", language="ruby", description="Para você que tem pouca experiência na linguagem!")
    course4 = user1.create_course(name="Python > Ruby", description="Falando apenas a verdade.", language="python")

    course1.add_member(user2)
    course1.add_member(user3)
    course2.add_member(user1)

    with open('dev/problems.json') as f:
        problems = json.loads(f.read())

    for problem in problems:
        name = problem.get('name')
        description = problem.get('description')
        tip = problem.get('tip')
        publish = True
        tests = problem.get('tests')
        tags = problem.get('tags')
        print(user_service.add_problem(id=1, name=name, description=description, tip=tip, publish=publish, tests=tests, tags=None).name)

    for i in range(45):
        problem = problem_service.accept_publish_request(i+1)

    problems = requests.get('http://localhost:5000/problem').json()

    problem = [x for x in problems if "cores" in x['name']][0]

    payload = {
        "key": problem['key'],
        "token": user1.token,
        "code": "print('Hello Dirlididi!')",
        "tests": [{"id": problem['tests'][i]['id'], 
                        "output": problem['tests'][i]['output']} for i in range(len(problem['tests']))]
    }

    for i in range(3):
        requests.post('http://localhost:5000/solve', json=payload)

    payload['token'] = user2.token

    for i in range(2):
        requests.post('http://localhost:5000/solve', json=payload)

    if len(requests.get('http://localhost:5000/problem').json()) == len(problems):
        print("Database populated successfully.")
        print("{} problems loaded".format(len(problems)))

if __name__ == "__main__":
    populate()