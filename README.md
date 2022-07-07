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
use python 3.8 <br>

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
SQLAlchemy==1.2.5
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
        return {'status': 'DELETED'} , 204
```
commit - with student CRUD