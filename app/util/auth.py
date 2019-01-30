from models.user import UserAuth
from flask import redirect, url_for
from flask_dance.contrib.google import google
from services.user_service import UserService
from db import db

def get_auth_user_id():
    return get_auth_user()._id

def get_auth_user():
    userinfo = google.get("/oauth2/v2/userinfo").json()
    name = userinfo['name']
    email = userinfo['email']
    auth = UserAuth.query.get(email)
    if auth:
        return auth.user
    user = UserService().create_user(name, email)
    auth = UserAuth(email=email, user=user)
    db.session.add(auth)
    db.session.commit()
    return user

def redirect_to_google_login():
    return redirect(url_for('google.login'))