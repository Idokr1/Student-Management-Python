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