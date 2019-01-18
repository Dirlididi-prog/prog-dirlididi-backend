from models.course import Course
from services.user_service import UserService


class CourseService(object):

    user_service = UserService()

    def get_course_by_id(self, id):
        return Course.query.get(id)
    
    def get_course_by_token(self, token):
        return Course.query.filter_by(token=token)

    def assign_user_to_course(self, user_id, course_id):
        user = self.user_service.get_user_by_id(user_id)
        course = self.get_course_by_id(course_id)
        course.add_member(user)
        return course

    def remove_user_from_course(self, user_id, course_id):
        user = self.user_service.get_user_by_id(user_id)
        course = self.get_course_by_id(course_id)
        course.remove_member(user)
        return course

    def create_course(self, user_id, name):
        user = self.user_service.get_user_by_id(user_id)
        return user.create_course(name)
    
    def get_all(self, user_id=None):
        if user_id:
            user = self.user_service.get_user_by_id(user_id)
            return user.courses
        else:
            return Course.query.all()
