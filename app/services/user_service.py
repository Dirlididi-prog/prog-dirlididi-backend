from db import db
from models.user import User
from util import hash_password
from exceptions import NotFound

class UserService(object):

    def get_all(self):
        return User.query.all()

    def create_user(self, name, email, password, admin=False):
        password = hash_password(password)
        user = User(name=name, email=email, password=password, admin=admin)
        db.session.add(user)
        db.session.commit()
        return user
    
    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)
        if user:
            return user.password == hash_password(password)
        return False
    
    def get_user_by_email(self, email):
        user =  User.query.filter_by(email=email).first()
        if user:
            return user
        else:
            raise NotFound("User with email {} was not found".format(email))
    
    def get_user_by_token(self, token):
        user = User.query.filter_by(token=token).first()
        if user:
            return user
        else:
            raise NotFound("User with token {} was not found".format(token))
    
    def get_user_by_id(self, id):
        user = User.query.get(id)
        if user:
            return user
        else:
            raise NotFound("User with id {} was not found".format(id))
    
    def add_problem(self, id, name, description, tip, publish, tests, tags=None):
        user = self.get_user_by_id(id)
        return user.add_problem(name, description, tip, publish, tests, tags)

    def try_solution(self, user_token, problem_key, code, tests):
        ''' Registers and returns a solution '''
        user = self.get_user_by_token(user_token)
        return user.try_solution(problem_key, code, tests)

    def get_top_users(self, num=3):
        top_users = sorted(self.get_all(), key=lambda x: x.solution_qnt, reverse=True)
        num = min(len(top_users), num)
        return top_users[:num]

    def check_admin(self, id):
        user = self.get_user_by_id(id)
        return user.admin