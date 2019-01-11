import requests
import json

user_payload = {
    "email": "matheus@mat.com",
    "password": "010101"
}

requests.post('http://localhost:5000/user', json=user_payload)

jwt = requests.post('http://localhost:5000/auth', json=user_payload).json().get('jwt')

with open('populate_data.json') as f:
    problems = json.loads(f.read())



for key in [problem['key'] for problem in problems]:
    problem_data = requests.get('http://dirlididi.com/api/problem/{}'.format(key)).json()
    print(key)
    requests.post('http://localhost:5000/problem', headers={"Authorization": "Bearer {}".format(jwt)},
        json=problem_data)

if len(requests.get('http://localhost:5000/problem').json()) == len(problems):
    print("Database populated successfully.")
    print("{} problems loaded".format(len(problems)))
