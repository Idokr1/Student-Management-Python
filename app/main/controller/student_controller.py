from flask_restplus import Resource
from ..model.student import api
from ..model.student import StudentDto
from ..service.student_service import get_all_students, save_new_student, get_a_student, update_student, delete_student
from typing import Tuple, Dict

from flask import request

_student = StudentDto.student
_student_out = StudentDto.student_out


@api.route('/')
class StudentController(Resource):
    @api.doc('list_of_students')
    @api.marshal_list_with(_student_out, envelope='data')
    def get(self):
        return get_all_students()

    @api.expect(_student, validate=True)
    @api.response(201, 'Student successfully created.')
    @api.marshal_with(_student_out)
    @api.doc('create a new Student')
    def post(self) -> Tuple[Dict[str, str], int]:
        data = request.json
        return save_new_student(data=data)


@api.route('/<id>')
@api.param('id', 'The Student identifier')
@api.response(404, 'Student not found.')
class OneStudentController(Resource):
    @api.doc('get a student')
    @api.marshal_with(_student_out)
    def get(self, id):
        student = get_a_student(id)
        print(student)
        if not student:
            api.abort(404)
        else:
            return student

    @api.expect(_student, validate=True)
    @api.response(201, 'Student successfully updated.')
    @api.marshal_with(_student_out)
    @api.doc('update a Student')
    def put(self, id) -> Tuple[Dict[str, str], int]:
        data = request.json
        return update_student(id, data)

    @api.response(204, 'Student successfully deleted.')
    @api.doc('delete a new Student')
    def delete(self, id) -> Tuple[Dict[str, str], int]:
        delete_student(id)
        return {'status': 'DELETED'}, 204