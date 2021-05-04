from . import db
from datetime import datetime


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    course_start = db.Column(db.DateTime(), default=datetime.utcnow)
    course_end = db.Column(db.DateTime(), default=datetime.utcnow)
    amount = db.Column(db.Integer)

    def to_json(self):
        json_course = {
            'name': self.name,
            'course_start': self.course_start,
            'course_end': self.course_end,
            'amount': self.amount
        }
        return json_course

    def __repr__(self):
        return f'Course name {self.name}, course start - end [{self.course_start} - ' \
               f'{self.course_end}], amount {self.amount}. '
