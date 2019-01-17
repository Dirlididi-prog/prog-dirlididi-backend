import requests

import requests

def authed_request(action, url, data, jwt):
    return action(url, headers={"Authorization": "Bearer {}".format(jwt)},
        json=data)

user_payload = {
    "email": "matheus@mat.com",
    "password": "010101"
}

requests.post('http://localhost:5000/user', json=user_payload)

jwt = requests.post('http://localhost:5000/auth', json=user_payload).json().get('jwt')
user = authed_request(requests.get, 'http://localhost:5000/user', None, jwt).json()

course_payload = {
    "name": "Algoritmo"
}

print(authed_request(requests.post, 'http://localhost:5000/course', course_payload, jwt).json())