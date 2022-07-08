from flask_restplus import Resource
from ..model.student import api
from ..model.student import StudentDto
from ..service import student_service
from ..service.student_service import get_all_students, save_new_student, get_a_student, update_student, delete_student, \
    sms_students, upload_student_picture
from typing import Tuple, Dict

from flask import request

_student = StudentDto.student
_student_out = StudentDto.student_out


@api.route('/')
class StudentController(Resource):
    @api.doc('list_of_students')
    @api.param(name='fullname')
    @api.param(name='sat_score_from')
    @api.param(name='sat_score_to')
    @api.param(name='birthdate_from')
    @api.param(name='birthdate_to')
    @api.param(name='orderby_field')
    @api.param(name='orderby_direction')
    @api.param(name='page' ,default=1)
    @api.param(name='count' ,default=50)
    # @api.marshal_list_with(_student_out, envelope='data')
    def get(self):
        page = request.args.get("page")
        if page:
            page = int(page)
        count = request.args.get("count")
        if count:
            count = int(count)
        return get_all_students(request.args.get("fullname"),\
                                request.args.get("sat_score_from"),\
                                request.args.get("sat_score_to"), \
                                request.args.get("birthdate_from"),\
                                request.args.get("birthdate_to"), \
                                request.args.get("orderby_field"), \
                                request.args.get("orderby_direction"), \
                                page, \
                                count
                                )

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
        return {'status': 'DELETED'} , 204

@api.route('/sms')
class SmsStudentController(Resource):
    @api.doc('sms students')
    @api.expect(StudentDto.student_list, validate=True)
    def post(self):
        ids = request.json['ids']
        text = request.json['text']
        sms_students(ids, text)
        return {'status' : 'OK'}

@api.route('/picture')
class PictureStudentController(Resource):
    @api.doc('upload profile picture for student')
    @api.expect(StudentDto.upload_parser, validate=True)
    def post(self):
        args = StudentDto.upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        student_id = args['student_id']
        url = upload_student_picture(student_id, uploaded_file)

        return {'url' : url}
