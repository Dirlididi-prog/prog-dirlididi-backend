#condig: utf-8
import requests
import json
from threading import Thread
from time import sleep

class Populator(Thread):

    def run(self):
        sleep(10)
        populate()

def authed_request(action, url, data, jwt):
    return action(url, headers={"Authorization": "Bearer {}".format(jwt)},
        json=data)


def populate():
    user_payload = {
        "email": "matheus@mat.com",
        "password": "010101",
        "name": "Matheus Melo"
    }

    user2 = {
        "email": "charlin@charlle.com",
        "password": "12345",
        "name": "Charlle Dias"
    }

    user3 = {
        "email": "esdras@es.com",
        "password": "789734",
        "name": "Esdras Vidal"
    }

    course1 = {
        "name": "Algoritmo"
    }

    course2_ = {
        "name": "Python avançado"
    }

    course3 = {
        "name": "Ruby para iniciantes"
    }

    course4 = {
        "name": "Python > Ruby"
    }


    user1_token = requests.post('http://localhost:5000/user', json=user_payload).json().get('token')
    user2_token = requests.post('http://localhost:5000/user', json=user2).json().get('token')
    requests.post('http://localhost:5000/user', json=user3)

    jwt1 = requests.post('http://localhost:5000/auth', json=user_payload).json().get('jwt')
    jwt2 = requests.post('http://localhost:5000/auth', json=user2).json().get('jwt')
    jwt3 = requests.post('http://localhost:5000/auth', json=user3).json().get('jwt')


    course1 = authed_request(requests.post, 'http://localhost:5000/course', course1, jwt1).json()
    course2 = authed_request(requests.post, 'http://localhost:5000/course', course4, jwt1).json()
    print(authed_request(requests.post, 'http://localhost:5000/course', course3, jwt3).json())
    print(authed_request(requests.post, 'http://localhost:5000/course', course2_, jwt2).json())

    authed_request(requests.post, 'http://localhost:5000/course/token/{}'.format(course1['token']), {"action": "join"}, jwt2)
    authed_request(requests.post, 'http://localhost:5000/course/token/{}'.format(course1['token']), {"action": "join"}, jwt3)

    authed_request(requests.post, 'http://localhost:5000/course/token/{}'.format(course2['token']), {"action": "join"}, jwt1)

    with open('dev/problems.json') as f:
        problems = json.loads(f.read())

    for problem in problems:
        authed_request(requests.post, 'http://localhost:5000/problem', problem, jwt1)
        sleep(0.05)

    problems = requests.get('http://localhost:5000/problem').json()

    problem = [x for x in problems if "cores" in x['name']][0]

    payload = {
        "key": problem['key'],
        "token": user1_token,
        "code": "print('Hello Dirlididi!')",
        "tests": [{"id": problem['tests'][i]['id'], 
                        "output": problem['tests'][i]['output']} for i in range(len(problem['tests']))]
    }

    for i in range(3):
        authed_request(requests.post, 'http://localhost:5000/solve', payload, jwt1)

    payload['token'] = user2_token

    for i in range(2):
        authed_request(requests.post, 'http://localhost:5000/solve', payload, jwt3)


    if len(requests.get('http://localhost:5000/problem').json()) == len(problems):
        print("Database populated successfully.")
        print("{} problems loaded".format(len(problems)))

if __name__ == "__main__":
    populate()