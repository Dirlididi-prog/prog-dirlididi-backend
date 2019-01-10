from db import db
from models.user import User
from util import hash_password


class UserService(object):

    def create_user(self, email, password):
        password = hash_password(password)
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user
    
    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)
        if user:
            return user.password == hash_password(password)
        return False
    
    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def add_problem(self, id, name, description, tip, tests):
        user = User.query.get(id)
        return user.add_problem(name, description, tip, tests)
