#coding: utf-8
import requests

def authed_request(action, url, data, jwt):
    return action(url, headers={"Authorization": "Bearer {}".format(jwt)},
        json=data)

# user_payload = {
#     "email": "charlle_gatinho@hotmail.com",
#     "password": "oioi"
# }

# jwt = requests.post('http://localhost:5000/auth', json=user_payload).json().get('jwt')
# user = authed_request(requests.get, 'http://localhost:5000/user', None, jwt).json()

problems = requests.get('http://localhost:5000/problem').json()

problem = [x for x in problems if "cores" in x['name']][0]

payload = {
    "key": problem['key'],
    "token": "z7kdx5dXJ",
    "code": "print('Hello Dirlididi!')",
    "tests": [{"id": problem['tests'][i]['id'], 
                    "output": problem['tests'][i]['output']} for i in range(len(problem['tests']))]
}
print (payload)
print(authed_request(requests.post, 'http://localhost:5000/solve', payload, None).json())
# print(problem['key'])
