from flask_restx import Namespace

api = Namespace('student', description='student related operations')

from .. import db

class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    fullname = db.Column(db.String(100), unique=False, nullable=False)
    birthdate = db.Column(db.DateTime, nullable=True)
    sat_score = db.Column(db.Integer, nullable=True)
    graduation_score = db.Column(db.Float, nullable=True)
    email = db.Column(db.String(255), unique=False, nullable=True)
    phone = db.Column(db.String(20), unique=False, nullable=True)
    picture = db.Column(db.String(300), unique=False, nullable=True)

    def __repr__(self):
        return "<Student '{}'>".format(self.fullname)

from flask_restx import fields

class StudentDto:
    student = api.model('student', {
        'fullname': fields.String(required=True, description='student name'),
        'birthdate': fields.Date(description='birth date'),
        'sat_score': fields.Integer(description='SAT score'),
        'graduation_score': fields.Float(description='Graduation score'),
        'email': fields.String(description='email'),
        'phone': fields.String(description='phone')
    })
    student_out = api.model('student_out', {
        'id': fields.Integer(required=True, description='student id'),
        'created_at': fields.Date(required=True, description='student created at'),
        'fullname': fields.String(required=True, description='student name'),
        'birthdate': fields.Date(description='birth date'),
        'sat_score': fields.Integer(description='SAT score'),
        'graduation_score': fields.Float(description='Graduation score'),
        'email': fields.String(description='email'),
        'phone': fields.String(description='phone'),
        'picture': fields.String(description='picture')
    })
    student_list = api.model('student_list', {
        'ids': fields.List(required=True, description='student list', cls_or_instance=fields.Integer()),
        'text': fields.String(required=True, description='text to send')
    })

    from werkzeug.datastructures import FileStorage
    upload_parser = api.parser()
    upload_parser.add_argument('student_id', type=int, help='student id', location='args')
    upload_parser.add_argument('file', type=FileStorage, location='files')