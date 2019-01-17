from db import db
from flask_restful import fields
from util import key_generator

class Course(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user._id'))
    _members = db.relationship('CourseParticipation')
    _problems = db.relationship('Problem')
    token = db.Column(db.String(9), default=key_generator, unique=True)

    @property
    def members(self):
        return [participation.user.email for participation in self._members]

    @property
    def problems(self):
        return [course.key for course in self._problems]

    api_fields = {
        "id": fields.Integer(attribute='_id'),
        "name": fields.String,
        "owner": fields.Integer,
        "members": fields.List(fields.String),
        "token": fields.String,
        "problems": fields.List(fields.String)
    }

    def add_member(self, member):
        participation = CourseParticipation(user_id=member._id, user=member)
        if participation not in self._members:
            self._members.append(participation)
        db.session.add(participation)
        db.session.commit()
    


class CourseParticipation(db.Model):

    _id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'))
    user = db.relationship('User')
    course_id = db.Column(db.Integer, db.ForeignKey('course._id'))
    course = db.relationship('Course')

    def __eq__(self, other):
        return self.user_id == other.user_id