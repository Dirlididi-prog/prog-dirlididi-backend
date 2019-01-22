from models.course import Course
from services.user_service import UserService
from services.problem_service import ProblemService

class CourseService(object):

    user_service = UserService()
    problem_service = ProblemService()

    def get_course_by_id(self, id):
        return Course.query.get(id)
    
    def get_course_by_token(self, token):
        return Course.query.filter_by(token=token).first()

    def assign_user_to_course(self, user_id, course_id=None, course_token=None):
        if course_id:
            course = self.get_course_by_id(course_id)
        elif course_token:
            course = self.get_course_by_token(course_token)
        user = self.user_service.get_user_by_id(user_id)
        course.add_member(user)
        return course

    def remove_user_from_course(self, user_id, course_id=None, course_token=None):
        if course_id:
            course = self.get_course_by_id(course_id)
        elif course_token:
            course = self.get_course_by_token(course_token)
        user = self.user_service.get_user_by_id(user_id)
        course.remove_member(user)
        return course

    def create_course(self, user_id, name, language, problems):
        if problems:
            problems = [self.problem_service.get_problem_by_key(key) for key in problems]
        user = self.user_service.get_user_by_id(user_id)
        return user.create_course(name, language, problems)
    
    def get_all(self, user_id=None):
        if user_id:
            user = self.user_service.get_user_by_id(user_id)
            return user.courses
        else:
            return Course.query.all()

    def get_top_courses(self, num=4):
        top_courses = sorted(Course.query.all(), key=lambda x: len(x.members), reverse=True)
        num = min(len(top_courses), num)
        return top_courses[:num]
