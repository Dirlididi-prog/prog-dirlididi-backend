from db import db
from models.user import User
from util import hash_password


class UserService(object):

    def get_all(self):
        return User.query.all()

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
    
    def get_user_by_token(self, token):
        return User.query.filter_by(token=token).first()
    
    def get_user_by_id(self, id):
        return User.query.get(id)
    
    def add_problem(self, id, name, description, tip, publish, tests):
        user = User.query.get(id)
        return user.add_problem(name, description, tip, publish, tests)

    def try_solution(self, user_token, problem_key, code, tests):
        ''' Registers and returns a solution '''
        user = self.get_user_by_token(user_token)
        return user.try_solution(problem_key, code, tests)
