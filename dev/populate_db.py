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


for problem in problems:
    print(problem['key'])
    requests.post('http://localhost:5000/problem', headers={"Authorization": "Bearer {}".format(jwt)},
        json=problem)

if len(requests.get('http://localhost:5000/problem').json()) == len(problems):
    print("Database populated successfully.")
    print("{} problems loaded".format(len(problems)))
