from flask import request
from flask_restful import Resource, marshal_with, fields
from flask_jwt_extended import create_access_token
from models.course import Course
from models.problem import Problem, Solution, PublishRequest
from models.user import User
from services.course_service import CourseService
from services.problem_service import ProblemService
from services.user_service import UserService
from flask_jwt_extended import get_jwt_identity, jwt_required
from exceptions import MissingAttribute, Unauthorized, BadRequest
from config.callbacks import verify_attributes

class ProblemDetail(Resource):

    problem_service = ProblemService()

    @marshal_with(Problem.api_fields)
    def get(self, key):
        return self.problem_service.get_problem_by_key(key)


class ProblemList(Resource):

    user_service = UserService()
    problem_service = ProblemService()

    @marshal_with(Problem.api_fields)
    def get(self):
        name = request.args.get('name')
        return self.problem_service.get_all_public(name)

    @verify_attributes(Course.required_attributes)
    @jwt_required
    @marshal_with(Problem.api_fields)
    def post(self):
        id = get_jwt_identity()
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        tip = data.get('tip')
        tests = data.get('tests')
        publish = data.get('publish')
        tags = data.get('tags')
        return self.user_service.add_problem(id, name, description, tip, publish, tests, tags)


class UserAuth(Resource):

    user_service = UserService()

    @verify_attributes(['email', 'password'])
    def post(self):
        """ Returns the JWT access token if username and password match to a
        registered user or errors if they doesn't
        """
        
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if not email or not password:
            raise MissingAttribute("Missing email or password field")

        authenticated = self.user_service.authenticate_user(email, password)

        if not authenticated:
            raise Unauthorized("Bad username or password")

        user = self.user_service.get_user_by_email(email)
        access_token = create_access_token(identity=user._id)

        return {"message": "User authenticated successfully" ,"jwt" : access_token}

class UserDetail(Resource):

    user_service = UserService()

    @jwt_required
    @marshal_with(User.api_fields)
    def get(self):
        id = get_jwt_identity()
        return self.user_service.get_user_by_id(id)

    @verify_attributes(User.required_attributes)
    @marshal_with(User.api_fields)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        return self.user_service.create_user(name, email, password)


class SolveProblem(Resource):

    user_service = UserService()

    @verify_attributes(Solution.required_attributes)
    @marshal_with(Solution.api_fields)
    def post(self):
        data = request.get_json()
        user_token = data.get('token')
        problem_key = data.get('key')
        code = data.get('code')
        tests = data.get('tests')
        solution = self.user_service.try_solution(user_token, problem_key, code, tests)
        return solution
    
    @jwt_required
    @marshal_with(Solution.api_fields)
    def get(self):
        return Solution.query.all()


class CourseCRUD(Resource):

    course_service = CourseService()

    @verify_attributes(Course.required_attributes)
    @jwt_required
    @marshal_with(Course.api_fields)
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        language = data.get('language')
        problems = data.get('problems')
        return self.course_service.create_course(user_id, name, description, language, problems)

    @marshal_with(Course.api_fields)
    def get(self):
        return self.course_service.get_all()


class UserCourses(Resource):

    course_service = CourseService()

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        return self.course_service.get_all(user_id)


class CourseIdDetail(Resource):

    LEAVE_ACTION = 'leave'
    JOIN_ACTION = 'join'

    user_service = UserService()
    course_service = CourseService()

    @marshal_with(Course.api_fields)
    def get(self, id):
        return self.course_service.get_course_by_id(id)
    
    @verify_attributes(['action'])
    @jwt_required
    @marshal_with(Course.api_fields)
    def post(self, id):
        user_id = get_jwt_identity()
        data = request.get_json()
        action = data.get('action')
        if action == self.JOIN_ACTION:
            return self.course_service.assign_user_to_course(user_id, course_id=id)
        elif action == self.LEAVE_ACTION:
            return self.course_service.remove_user_from_course(user_id, course_id=id)
        else:
            raise BadRequest("'{}' action is not valid".format(action))


class CourseTokenDetail(Resource):

    LEAVE_ACTION = 'leave'
    JOIN_ACTION = 'join'

    course_service = CourseService()

    @marshal_with(Course.api_fields)
    def get(self, token):
        course = self.course_service.get_course_by_token(token)
        return course if course else ({}, 404)
    
    @verify_attributes(['action'])
    @jwt_required
    @marshal_with(Course.api_fields)
    def post(self, token):
        user_id = get_jwt_identity()
        data = request.get_json()
        action = data.get('action')
        if action == self.JOIN_ACTION:
            return self.course_service.assign_user_to_course(user_id, course_token=token)
        elif action == self.LEAVE_ACTION:
            return self.course_service.remove_user_from_course(user_id, course_token=token)
        else:
            raise BadRequest("'{}' action is not valid".format(action))


class Info(Resource):

    FIELDS = {
        "users": fields.Integer,
        "courses": fields.Integer,
        "problems": fields.Integer,
        "solutions": fields.Integer,
        "topUsers": fields.Nested({
            "id": fields.Integer(attribute="_id"),
            "email": fields.String,
            "name": fields.String,
            "solutions": fields.Integer(attribute="solution_qnt")
        }),
        "topCourses": fields.Nested({
            "id": fields.Integer(attribute="_id"),
            "token": fields.String,
            "members": fields.Integer(attribute="member_qnt"),
            "name": fields.String,
            "language": fields.String,
        })
    }

    user_service = UserService()
    course_service = CourseService()
    problem_service = ProblemService()

    @marshal_with(FIELDS)
    def get(self):
        return {
            "users": len(self.user_service.get_all()),
            "courses": len(self.course_service.get_all()),
            "problems": len(self.problem_service.get_all()),
            "solutions": len([s for user in self.user_service.get_all() for s in user.solutions]),
            "topUsers": self.user_service.get_top_users(),
            "topCourses": self.course_service.get_top_courses()
        }


class AdminPublishRequests(Resource):

    ACCEPT_ACTION = 'accept'
    DECLINE_ACTION = 'decline'

    problem_service = ProblemService()
    user_service = UserService()

    @marshal_with(PublishRequest.api_fields)
    def get(self):
        return self.problem_service.get_all_publish_requests()
    
    @jwt_required
    @verify_attributes(["action"])
    @marshal_with(Problem.api_fields)
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        pr_id = data.get('id')
        action = data.get('action')
        
        if self.user_service.check_admin(user_id):
            if action == self.ACCEPT_ACTION:
                return self.problem_service.accept_publish_request(pr_id)
            elif action == self.DECLINE_ACTION:
                return self.problem_service.decline_publish_request(pr_id)
            else:
                raise BadRequest("'{}' action is not valid".format(action))
        else:
            raise Unauthorized("User with id {} is not admin".format(user_id))
