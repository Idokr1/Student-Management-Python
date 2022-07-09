from flask_restx import Api
from flask import Blueprint

from .main.controller.student_controller import api as students_ns
from .main.controller.student_grade_controller import api as students_grades_ns
from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='STUDENTS APP',
    version='1.0',
    description='flask restplus web service for students and grades',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(students_ns, path='/student')
api.add_namespace(students_grades_ns, path='/student')
api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)