from flask_restplus import Resource
from ..model.student import api

@api.route('/')
class StudentController(Resource):
    @api.doc('Hello world')
    def get(self):
        return "Hello world"