from flask_restx import Namespace

api = Namespace('student_grade', description='student grade related operations')

from .. import db

class StudentGrade(db.Model):
    __tablename__ = "student_grade"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    course_name = db.Column(db.String(100), unique=False, nullable=False)
    course_score = db.Column(db.Integer, nullable=True)
    def __repr__(self):
        return "<Student Grade'{} {}'>".format(self.student_id, self.course_name)

from flask_restx import fields

class StudentGradeDto:
    student_grade = api.model('student_grade', {
        'course_name': fields.String(required=True, description='course name'),
        'course_score': fields.Integer(description='Course score')
    })
    student_grade_out = api.model('student_grade_out', {
        'id': fields.Integer(required=True, description='student id'),
        'created_at': fields.Date(required=True, description='student created at'),
        'student_id': fields.Integer(required=True, description='student id'),
        'course_name': fields.String(description='course name'),
        'course_score': fields.Integer(description='Course score')
    })
