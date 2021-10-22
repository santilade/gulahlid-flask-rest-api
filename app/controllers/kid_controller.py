from flask import Blueprint, request, jsonify
from app import db
from app.models import Employee, Kid
from app.schemas import kid_schema, kids_schema

kid_controller = Blueprint('kid_controller', __name__)


# ///////////////// KID /////////////////
# Add Kid
@kid_controller.route('/kid', methods=['POST'])
def add_kid():
    name = request.json['name']
    grade = request.json['grade']
    group_id = request.json['group_id']
    difficulty = request.json['difficulty']
    closed_circle = request.json['closed_circle']
    employees_needed = request.json['employees_needed']
    compatible_employees = []
    compatible_kids = []
    kid_infos = []
    shifts = []

    new_kid = Kid(name, grade, group_id, difficulty, closed_circle, employees_needed, compatible_employees,
                  compatible_kids, kid_infos, shifts)

    db.session.add(new_kid)
    db.session.flush()

    compatible_employees = request.json['compatible_employees']
    compatible_kids = request.json['compatible_kids']

    if compatible_employees:
        for compatible_employee in compatible_employees:
            employee = Employee.query.get(compatible_employee)
            new_kid.compatible_employees.append(employee)
            db.session.flush()

    if compatible_kids:
        for kid_id in compatible_kids:
            compatible_kid = Kid.query.get(kid_id)
            new_kid.compatible_kids.append(compatible_kid)
            compatible_kid.compatible_kids.append(new_kid)
            db.session.flush()

    db.session.commit()

    return kid_schema.dump(new_kid)


# Get All Kids
@kid_controller.route('/kid', methods=['GET'])
def get_kids():
    all_kids = Kid.query.all()
    result = kids_schema.dump(all_kids)
    return jsonify(result)


# Get Single Kid
@kid_controller.route('/kid/<id>', methods=['GET'])
def get_kid(id):
    kid = Kid.query.get(id)
    return kid_schema.dump(kid)


# Update Kid
@kid_controller.route('/kid/<id>', methods=['PUT'])
def update_kid(id):
    kid = Kid.query.get(id)

    name = request.json['name']
    grade = request.json['grade']
    group_id = request.json['group_id']
    difficulty = request.json['difficulty']
    closed_circle = request.json['closed_circle']
    employees_needed = request.json['employees_needed']
    compatible_employees = request.json['compatible_employees']
    compatible_kids = request.json['compatible_kids']

    if name != "":
        kid.name = name
        db.session.flush()
    if grade != "":
        kid.grade = grade
        db.session.flush()
    if group_id != "":
        kid.group_id = group_id
        db.session.flush()
    if difficulty != "":
        kid.difficulty = difficulty
        db.session.flush()
    if closed_circle != "":
        kid.closed_circle = closed_circle
        db.session.flush()
    if employees_needed != "":
        kid.employees_needed = employees_needed
        db.session.flush()

    if compatible_employees:
        for compatible_employee in compatible_employees:
            employee = Employee.query.get(compatible_employee)
            kid.compatible_employees.append(employee)
            db.session.flush()
    elif compatible_employees is None:
        kid.compatible_employees = []
        db.session.flush()

    if compatible_kids:
        for old_compatible_kid in kid.compatible_kids:
            old_compatible_kid.compatible_kids.remove(kid)
            db.session.flush()
        kid.compatible_kids = []
        db.session.flush()
        for kid_id in compatible_kids:
            compatible_kid = Kid.query.get(kid_id)
            kid.compatible_kids.append(compatible_kid)
            compatible_kid.compatible_kids.append(kid)
            db.session.flush()
    elif compatible_kids is None:
        for old_compatible_employee in kid.compatible_kids:
            old_compatible_employee.compatible_kids.remove(kid)
            db.session.flush()
        kid.compatible_kids = []
        db.session.flush()

    db.session.commit()

    return kid_schema.dump(kid)


# Delete Kid
@kid_controller.route('/kid/<id>', methods=['DELETE'])
def delete_kid(id):
    kid = Kid.query.get(id)

    compatible_employees = kid.compatible_employees
    compatible_kids = kid.compatible_kids
    kid_infos = kid.kid_infos
    shifts = kid.shifts

    for compatible_employee in compatible_employees:
        compatible_employee.compatible_kids.remove(kid)
        db.session.flush()

    for compatible_kid in compatible_kids:
        compatible_kid.compatible_kids.remove(kid)
        db.session.flush()

    for kid_info in kid_infos:
        db.session.delete(kid_info)

    for shift in shifts:
        db.session.delete(shift)

    db.session.delete(kid)
    db.session.commit()

    return kid_schema.dump(kid)
