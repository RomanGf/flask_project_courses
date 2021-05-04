from flask import jsonify, request, flash
from ..models import Course
from .. import db
from . import main
from datetime import datetime


@main.route('/courses', methods=['POST'])
def post():
    name = request.json.get('name')
    course_start = datetime.strptime(request.json.get('course_start'), '%d/%m/%y')
    course_end = datetime.strptime(request.json.get('course_end'), '%d/%m/%y')
    amount = request.json.get('amount')
    course = Course(name=name, course_start=course_start, course_end=course_end, amount=amount)
    db.session.add(course)
    db.session.commit()
    flash('Your course has been added')
    return jsonify(name=name, course_start=course_start, course_end=course_end, amount=amount)
    # return jsonify(name="Roman")


@main.route('/courses/<int:id_>', methods=['PUT'])
def put(id_):
    c = Course.query.filter_by(id=id_).first()
    if c is None:
        return jsonify({'message': 'Not found'}), 404
    c.name = request.json.get('name')
    c.amount = request.json.get('amount')
    c.course_start = datetime.strptime(request.json.get('course_start'), '%d/%m/%y')
    c.course_end = datetime.strptime(request.json.get('course_end'), '%d/%m/%y')
    db.session.commit()
    return jsonify({'message': 'The course updated'})


@main.route('/courses/<int:id_>', methods=['DELETE'])
def delete(id_):
    try:
        c = Course.query.filter_by(id=id_).first()
        db.session.delete(c)
        db.session.commit()
        return jsonify({'message': 'Course deleted'})
    except:
        return jsonify({'message': 'Something went wrong'}), 400


@main.route('/courses', methods=['GET'])
def get_all():
    courses = [{'id': c.id, 'name': c.name,
                'course_start': c.course_start, 'course_end': c.course_end, 'amount': c.amount}
                for c in Course.query.all()]
    return jsonify(courses)


@main.route('/courses/<int:id_>', methods=['GET'])
def get(id_):
    c = Course.query.filter_by(id=id_).first()
    if c is None:
        return jsonify({'message': 'Not found'})
    return jsonify({'id': c.id, 'name': c.name,
                    'course_start': c.course_start, 'course_end': c.course_end, 'amount': c.amount})


@main.route('/courses/search', methods=['GET'])
def search():
    name = request.args.get('name')
    start_date = datetime.strptime(request.args.get('course_start'), '%d/%m/%Y') or None
    end_date = datetime.strptime(request.args.get('course_end'), '%d/%m/%Y') or None
    c = Course.query.filter_by(name=name).all()
    if start_date:
        c = list(filter(lambda x: x.course_start >= start_date, c))
    if end_date:
        c = list(filter(lambda x: x.course_end <= end_date, c))
    courses = [{
                    'id': i.id, 'name': i.name,
                    'course_start': i.course_start,
                    'course_end': i.course_end,
                    'amount': i.amount
                } for i in c]
    return jsonify(courses)
