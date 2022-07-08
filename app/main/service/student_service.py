import datetime

from flask import jsonify

from app.main import db
from sqlalchemy import text
from app.main.model.student import Student
from typing import Dict, Tuple

from app.main.service.aws_service import upload_file, create_presigned_url
from app.main.service.sms_service import send_one_sms
from app.main.util.fps import get_paginated


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


def get_a_student(id):
    student =  db.session.query(Student).filter(Student.id == id).first()
    if student.picture:
        student.picture = create_presigned_url(student.picture)
    return student


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

def sms_students(ids, text):
    for id in ids:
        student = db.session.query(Student).filter_by(id=id).first()
        if student:
            send_one_sms(student.phone, text)


def upload_student_picture(student_id, uploaded_file):
    student = db.session.query(Student).filter_by(id=student_id).first()
    if student:
        student.picture =  "apps/python/student-" +  str(student_id) + ".png"
        upload_file(uploaded_file, student.picture)
        db.session.commit()
