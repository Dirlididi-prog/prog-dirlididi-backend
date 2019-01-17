#coding: utf-8
import requests

def authed_request(action, url, data, jwt):
    return action(url, headers={"Authorization": "Bearer {}".format(jwt)},
        json=data)

user_payload = {
    "email": "matheus@mat.com",
    "password": "010101"
}

jwt = requests.post('http://localhost:5000/auth', json=user_payload).json().get('jwt')
user = authed_request(requests.get, 'http://localhost:5000/user', None, jwt).json()

problems = requests.get('http://localhost:5000/problem').json()

problem = [x for x in problems if "cores" in x['name']][0]

payload = {
    "key": problem['key'],
    "token": user['token'],
    "code": "print('Hello Dirlididi!')",
    "tests": [{"key": problem['tests'][i]['key'], 
                    "output": problem['tests'][i]['output']} for i in range(len(problem['tests']))]
}
print (payload)
print(authed_request(requests.post, 'http://localhost:5000/solve', payload, jwt).json())
# print(problem['key'])
