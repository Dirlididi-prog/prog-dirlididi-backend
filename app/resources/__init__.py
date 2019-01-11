from flask import request
from flask_restful import Resource, marshal_with
from flask_jwt_extended import create_access_token
from models.problem import Problem
from models.user import User
from services.problem_service import ProblemService
from services.user_service import UserService
from flask_jwt_extended import get_jwt_identity, jwt_required

class ProblemDetail(Resource):

    problem_service = ProblemService()

    @marshal_with(Problem.api_fields)
    def get(self, key):
        return self.problem_service.get_exercise_by_key(key)


class ProblemList(Resource):

    user_service = UserService()

    @marshal_with(Problem.api_fields)
    def get(self):
        return self.problem_service.get_all()

    @jwt_required
    @marshal_with(Problem.api_fields)
    def post(self):

        email = get_jwt_identity()
        user = self.user_service.get_user_by_email(email)
        user_id = user._id
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        tip = data.get('tip')
        tests = data.get('tests')
        publish = data.get('publish')

        print(publish)

        return self.user_service.add_problem(user_id, name, description, tip, publish, tests)


class UserAuth(Resource):

    user_service = UserService()

    def post(self):
        """ Returns the JWT access token if username and password match to a
        registered user or errors if they doesn't
        """
        
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if not email or not password:
            return {"message" : "Missing email or password field", "jwt" : None }, 400

        authenticated = self.user_service.authenticate_user(email, password)

        if not authenticated:
            return {"message" : "Bad username or password", "jwt" : None}, 401

        access_token = create_access_token(identity=email)

        return {"message": "User authenticated successfully" ,"jwt" : access_token}

class UserDetail(Resource):

    user_service = UserService()

    @jwt_required
    @marshal_with(User.api_fields)
    def get(self):
        email = get_jwt_identity()
        user = self.user_service.get_user_by_email(email)
        return user

    @marshal_with(User.api_fields)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        return self.user_service.create_user(email, password)