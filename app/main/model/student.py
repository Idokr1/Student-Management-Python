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