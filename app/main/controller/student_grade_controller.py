from flask_restplus import Resource
from ..model.student_grade import api
from ..model.student_grade import StudentGradeDto
from ..service.student_grade_service import *
from typing import Tuple, Dict

from flask import request

_student_grade = StudentGradeDto.student_grade
_student_grade_out = StudentGradeDto.student_grade_out


@api.route('/<student_id>/grade')
@api.param('student_id', 'The Student identifier')
class StudentGradeController(Resource):
    @api.doc('list_of_student_grades')
    @api.marshal_list_with(_student_grade_out, envelope='data')
    def get(self, student_id):
        return get_all_grades_for_student(student_id)

    @api.expect(_student_grade, validate=True)
    @api.response(201, 'Student grade successfully created.')
    @api.marshal_with(_student_grade_out)
    @api.doc('create a new Student Grade')
    def post(self, student_id) -> Tuple[Dict[str, str], int]:
        data = request.json
        return save_new_student_grade(student_id=student_id, data=data)


@api.route('/<student_id>/grade/<id>')
@api.param('id', 'The Student Grade identifier')
@api.param('student_id', 'The Student identifier')
@api.response(404, 'Student not found.')
class OneStudentGradeController(Resource):
    @api.expect(_student_grade, validate=True)
    @api.response(201, 'Student successfully updated.')
    @api.marshal_with(_student_grade_out)
    @api.doc('update a Student grade')
    def put(self, student_id, id) -> Tuple[Dict[str, str], int]:
        data = request.json
        return update_student_grade(id, data)

    @api.response(204, 'Student successfully deleted.')
    @api.doc('delete a Student Grade')
    def delete(self, student_id, id) -> Tuple[Dict[str, str], int]:
        delete_student_grade(id)
        return {'status': 'DELETED'} , 204
