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
