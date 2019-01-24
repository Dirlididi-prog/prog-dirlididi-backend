from abc import ABCMeta, abstractmethod
from flask import jsonify

class DirlididiBaseException(Exception):
    __metaclass__ = ABCMeta

    def __init__(self, message):
        self.message = message

    @property
    @abstractmethod
    def status_code(self):
        pass


class NotFound(DirlididiBaseException):
    status_code = 404
    

class Unauthorized(DirlididiBaseException):
    status_code = 401


class MissingAttribute(DirlididiBaseException):
    status_code = 400


class BadRequest(DirlididiBaseException):
    status_code = 400