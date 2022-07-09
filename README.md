use this structure:
```
├── app
│   ├── __init__.py
│   ├── main
│   │   ├── controller
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   └── test
│       └── __init__.py
└── requirements.txt
```
use python 3.9 <br>

requirements.txt
```python
alembic==0.9.8
aniso8601==3.0.0
bcrypt==3.1.4
cffi==1.15.0
click==6.7
Flask==0.12.2
Flask-Bcrypt==0.7.1
Flask-Migrate==2.1.1
flask-restplus==0.10.1
flask-restx==0.5.1
Flask-Script==2.0.6
Flask-SQLAlchemy==2.3.2
Flask-Testing==0.7.1
itsdangerous==0.24
Jinja2==2.10
jsonschema==2.6.0
Mako==1.0.7
MarkupSafe==2.0.1
pycparser==2.18
PyJWT==1.6.0
python-dateutil==2.7.0
python-editor==1.0.3
pytz==2018.3
six==1.11.0
SQLAlchemy==1.4.39
Werkzeug==0.14.1
psycopg2-binary==2.9.3
```
install requirements <br>
model/student.py
```python
from flask_restx import Namespace

api = Namespace('student', description='student related operations')
```
main/__init__.py
```python
from flask import Flask


def create_app():
    app = Flask(__name__)
    return app
```
controller/student_controller.py
```python
from flask_restplus import Resource
from ..model.student import api

@api.route('/')
class StudentController(Resource):
    @api.doc('Hello world')
    def get(self):
        return "Hello world"
```
app/__init__.py
```python
from flask_restx import Api
from flask import Blueprint

from .main.controller.student_controller import api as students_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='STUDENTS APP',
          version='1.0',
          description='flask restplus web service for students and grades'
          )

api.add_namespace(students_ns, path='/student')
```
manage.py
```python
import os
from flask_script import Manager
import unittest
from app import blueprint
from app.main import create_app


app = create_app()
app.register_blueprint(blueprint)

app.app_context().push()
manager = Manager(app)


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
```
commit - hello world
### START DOCKER
```
docker run -d -p 5432:5432 -v postgresdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres postgres
docker ps
docker logs [containerid]
```
### DB
main/config.py
```python
import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@postgres:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
```
main/__init__.py
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

```
main/model/student.py
```python
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
```
manage.py
```python
from flask_migrate import Migrate, MigrateCommand
from app.main import db
from app.main.model import student
.
.
.

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


```
run the following
```
python manage.py db init
python manage.py db migrate --message 'initial database migration'
python manage.py db upgrade
```
check with tableplus that table has been created<br>
commit - with db
### REST API
model/student.py
```python
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
```
service/student_service.py
```python
import datetime
from app.main import db
from app.main.model.student import Student
from typing import Dict, Tuple


def save_new_student(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    student = Student.query.filter_by(email=data['email']).first()
    if not student:
        new_student = Student(
            created_at=datetime.datetime.utcnow(),
            fullname=data['fullname'],
            birthdate=data['birthdate'],
            sat_score=data['sat_score'],
            graduation_score=data['graduation_score'],
            phone=data['phone'],
            email=data['email']
        )
        return save_changes(new_student), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Student already exists',
        }
        return response_object, 409


def update_student(id: int, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    student = db.session.query(Student).filter_by(id=id).first()
    if student:
        student.fullname = data['fullname']
        student.birthdate = data['birthdate']
        student.sat_score = data['sat_score']
        student.graduation_score = data['graduation_score']
        student.phone = data['phone']
        student.email = data['email']
        db.session.commit()
        return student, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Student not found',
        }
        return response_object, 409


def get_all_students():
    return Student.query.all()


def get_a_student(id):
    return db.session.query(Student).filter(Student.id == id).first()


def delete_student(id: int) -> Tuple[Dict[str, str], int]:
    student = db.session.query(Student).filter(Student.id == id).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        return {'status': 'DELETED'}, 204
    else:
        response_object = {
            'status': 'fail',
            'message': 'Student not found',
        }
        return response_object, 409


def save_changes(data: Student) -> Student:
    db.session.add(data)
    db.session.commit()
    db.session.refresh(data)
    return data

```
controller/student_controller.py

```python
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
```
commit - with student CRUD
### ONE TO MANY
model/student_grade.py
```python
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
```
manage.py
```python
from app.main.model import student_grade
```
run
```
python manage.py db migrate --message 'student grades'
python manage.py db upgrade
```
service/student_grade_service.py
```python
import datetime
from app.main import db
from app.main.model.student import Student
from typing import Dict, Tuple

from app.main.model.student_grade import StudentGrade


def save_new_student_grade(student_id, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    student = Student.query.filter_by(id=student_id).first()
    if student:
        new_student_grade = StudentGrade(
            created_at=datetime.datetime.utcnow(),
            student_id=student_id,
            course_name=data['course_name'],
            course_score=data['course_score']
        )
        return save_changes(new_student_grade), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Student does not exist',
        }
        return response_object, 409


def update_student_grade(id: int, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    student_grade = db.session.query(StudentGrade).filter_by(id=id).first()
    if student_grade:
        student_grade.course_name = data['course_name']
        student_grade.course_score = data['course_score']
        db.session.commit()
        return student_grade, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Student grade not found',
        }
        return response_object, 409


def get_all_grades_for_student(student_id: int):
    return StudentGrade.query.filter(StudentGrade.student_id == student_id).all()


def delete_student_grade(id: int) -> Tuple[Dict[str, str], int]:
    student_grade = db.session.query(StudentGrade).filter(StudentGrade.id == id).first()
    if student_grade:
        db.session.delete(student_grade)
        db.session.commit()
        return {'status': 'DELETED'}, 204
    else:
        response_object = {
            'status': 'fail',
            'message': 'Student grade not found',
        }
        return response_object, 409


def save_changes(data: StudentGrade) -> StudentGrade:
    db.session.add(data)
    db.session.commit()
    db.session.refresh(data)
    return data
```
controller/student_grade_controller.py
```python
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
```
app/__init__.py
```python
from .main.controller.student_grade_controller import api as students_grades_ns
api.add_namespace(students_grades_ns, path='/student')
```
commit - with one to many
### FPS
util/fps.py
```python
from sqlalchemy import text

from app.main import db

def get_json_value(x):
    if 'date' in  str(type(x)):
        return str(x)
    elif 'Decimal' in  str(type(x)):
        return float(x)
    return x

def get_paginated(fields, from_str, where_str, orderby_field, orderby_direction, page, count, params ):
    select_str = 'select ' + ','.join(map(lambda x: x[0] + " " + x[1] ,fields)) + ' ' + from_str + ' '
    ob = list(filter(lambda x: x[1] == orderby_field, fields))
    orderby_str = ""
    if (len(ob) > 0):
        orderby_str = " order by " + ob[0][0] + " " + orderby_direction + " "

    if page and  count:
        orderby_str = orderby_str + " limit " +str(count)
        orderby_str = orderby_str + " offset " + str((page - 1) * count)

    sql = select_str + where_str + orderby_str
    print("running:" + sql)
    fetchall = db.session.execute(text(sql), params).fetchall()
    rowcount = db.session.execute(text("select count(*) cnt from (" + select_str + where_str + ") as a"), params).fetchall()

    res = {}
    total = rowcount[0]["cnt"]
    res['count'] = total
    if count > total:
        count = total
    if page and count:
        res['page'] = page
        last = 1
        if total % count == 0:
            last = 0
        res['of_page'] = (total / count) + last
    res['data'] =  [dict(zip(row._fields, map(lambda x: get_json_value(x), row._data))) for row in fetchall]
    return res
```
service/student_service.py
```python
def get_all_students(fullname, sat_score_from, sat_score_to, birthdate_from, birthdate_to, \
                     orderby_field, orderby_direction, page, count):

    fields = [
        ("s.id", "id"),
        ("s.created_at", "created_at"),
        ("s.fullname", "fullname"),
        ("s.sat_score", "sat_score"),
        ("s.graduation_score", "graduation_score"),
        ("s.phone", "phone"),
        ("s.email", "email"),
        ("s.picture", "picture"),
        ("(select avg(sg.course_score) avg_score from  student_grade sg where sg.student_id = s.id ) " ,"avg_score")
    ]
    from_str = " from student s "

    where_str = """ where (1=1) """
    if fullname is not None:
        where_str = where_str + " and (lower(fullname) LIKE   CONCAT('%', :fullname, '%'))"
    if sat_score_from is not None:
        where_str = where_str + " and (sat_score  >=  :sat_score_from)"
    if sat_score_to is not None:
        where_str = where_str + " and (sat_score  <=  :sat_score_to)"
    if birthdate_from is not None:
        where_str = where_str + " and (birthdate  >=  :birthdate_from)"
    if birthdate_to is not None:
        where_str = where_str + " and (birthdate  <=  :birthdate_to)"

    params = {"fullname": fullname, "sat_score_from": sat_score_from, "sat_score_to": sat_score_to,
           "birthdate_from": birthdate_from, "birthdate_to": birthdate_to}
    return get_paginated(fields=fields, from_str=from_str, where_str=where_str, params=params, orderby_field=orderby_field, orderby_direction=orderby_direction , page=page, count=count)
```
controller/student_controller.py
```python
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
```
commit - with fps
### SMS API
Config.py
```python
    SMS4FREE_KEY = 'J2IX1eEa9'
    SMS4FREE_USER = '0525236451'
    SMS4FREE_PASSWORD = '66534228'
```
requirments.txt
```python
requests==2.28.1
``` 
pip install -r requirements.txt 
<br>
service/sms_service.py
```python
import requests
from app.main import Config


def send_one_sms(phone, text):
  account_key = Config.SMS4FREE_KEY
  account_user = Config.SMS4FREE_USER
  account_pass = Config.SMS4FREE_PASSWORD

  url = "https://www.sms4free.co.il/ApiSMS/SendSMS"

  payload={'key' : account_key, 'user' : account_user, 'pass' : account_pass, 'sender' : "HANDSON", 'recipient': phone, 'msg': text}
  headers = {
    'content-type': 'application/json',
    'accept-language': 'en-US,en;q=0.9,he;q=0.8'
  }

  requests.request("POST", url, headers=headers, data=payload)
```
service/student_service.py
```python

def sms_students(ids, text):
    for id in ids:
        student = db.session.query(Student).filter_by(id=id).first()
        if student:
            send_one_sms(student.phone, text)
```
model/student.py
```python
    student_list = api.model('student_list', {
        'ids': fields.List(required=True, description='student list', cls_or_instance=fields.Integer()),
        'text': fields.String(required=True, description='text to send')
    })
```
controller/student_controller.py
```python
@api.route('/sms')
class SmsStudentController(Resource):
    @api.doc('sms students')
    @api.expect(StudentDto.student_list, validate=True)
    def post(self):
        ids = request.json['ids']
        text = request.json['text']
        sms_students(ids, text)
        return {'status' : 'OK'}
```
commit - with sms
### AWS presigned link
config.py
```python
    AWS_ACCESSKEY = 'AKIA6PS436XZW5V5FE5P'
    AWS_SECRETKEY= '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'
    BUCKET_URL = 'files.handson.academy'
```
requirements.txt
```python
boto3==1.24.25
```
pip install -r requirements.txt 
<br>
service/aws_service.py
```python
from app.main import Config
import logging
import boto3
from botocore.exceptions import ClientError

def upload_file(file , path):
  account_key = Config.AWS_ACCESSKEY
  account_secret = Config.AWS_SECRETKEY
  bucket_url = Config.BUCKET_URL

  s3_resource = boto3.resource(
    's3',
    aws_access_key_id=account_key,
    aws_secret_access_key=account_secret)

  bucket = s3_resource.Bucket(bucket_url)

  bucket.Object(path).put(Body=file.read())


def create_presigned_url(object_name, expiration=3600):
    account_key = Config.AWS_ACCESSKEY
    account_secret = Config.AWS_SECRETKEY
    bucket_name = Config.BUCKET_URL

    s3_client = boto3.client('s3',
                             region_name='eu-central-1',
                             aws_access_key_id=account_key,
                             aws_secret_access_key=account_secret)
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response
```
model/student.py
```python
    from werkzeug.datastructures import FileStorage
    upload_parser = api.parser()
    upload_parser.add_argument('student_id', type=int, help='student id', location='args')
    upload_parser.add_argument('file', type=FileStorage, location='files')
```
service/student_service.py
```python
def upload_student_picture(student_id, uploaded_file):
    student = db.session.query(Student).filter_by(id=student_id).first()
    if student:
        student.picture =  "apps/python/student-" +  str(student_id) + ".png"
        upload_file(uploaded_file, student.picture)
        db.session.commit()

def get_a_student(id):
    student =  db.session.query(Student).filter(Student.id == id).first()
    if student.picture:
        student.picture = create_presigned_url(student.picture)
    return student
```
controller/student_controller.py
```python
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
```
commit - with profile in s3
### JWT - authentication
apply patch jwt-authentication<br>
manage.py
```python
from app.main.model import user
```
run
```python
python manage.py db migrate --message 'users'
python manage.py db upgrade
```
config/config.py
```python
key = "MyJwtLovelyKey1234567890!!1234567890"
```
main/__init__.py
```python
from flask_bcrypt import Bcrypt
flask_bcrypt = Bcrypt()
.
.
    flask_bcrypt.init_app(app)
```
app/__init.py
```python
from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns


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


api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
```
commit - with jwt authentication
### DOCKER
Dockerfile
```python
FROM python:3.9.13-bullseye
RUN mkdir /p
RUN mkdir /p/app
ADD ./app /p/app
ADD ./manage.py /p
ADD ./requirements.txt /p
WORKDIR /p
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "manage.py", "run" ]
```
manage.py
```python
    app.run(host="0.0.0.0")
```
docker build . -t basic_python
<br>
commit - with docker