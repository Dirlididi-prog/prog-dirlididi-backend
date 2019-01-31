from models.user import UserAuth
from flask_jwt_extended import create_access_token
from google.auth.transport import requests
from google.oauth2 import id_token
from services.user_service import UserService
from db import db
from flask_jwt_extended import create_access_token
from os import environ
from exceptions import BadRequest

def get_jwt_user(token):
    CLIENT_ID = environ['CLIENT_ID']
    try:
        userinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    except Exception as e:
        raise BadRequest(str(e))
    name = userinfo['name']
    email = userinfo['email']
    auth = UserAuth.query.get(email)
    if not auth:
        user = UserService().create_user(name, email)
        auth = UserAuth(email=email, user=user)
        db.session.add(auth)
        db.session.commit()
    else:
        user = UserService().get_user_by_email(email)
    print(user._id is None)
    return create_access_token(identity=user._id)
