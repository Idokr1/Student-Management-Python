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