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
    compatible_employees = []
    incompatible_employees = []
    kid_infos = []
    shifts = []

    new_kid = Kid(name, grade, group_id, compatible_employees, incompatible_employees, kid_infos, shifts)

    db.session.add(new_kid)
    db.session.flush()

    compatible_employees = request.json['compatible_employees']
    incompatible_employees = request.json['incompatible_employees']

    if compatible_employees:
        for compatible_employee in compatible_employees:
            employee = Employee.query.get(compatible_employee)
            new_kid.compatible_employees.append(employee)
            db.session.flush()

    if incompatible_employees:
        for incompatible_employee in incompatible_employees:
            employee = Employee.query.get(incompatible_employee)
            new_kid.incompatible_employees.append(employee)
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
    compatible_employees = request.json['compatible_employees']
    incompatible_employees = request.json['incompatible_employees']

    if name != "":
        kid.name = name
        db.session.flush()
    if grade != "":
        kid.grade = grade
        db.session.flush()
    if group_id != "":
        kid.group_id = group_id
        db.session.flush()

    if compatible_employees:
        for compatible_employee in compatible_employees:
            employee = Employee.query.get(compatible_employee)
            kid.compatible_employees.append(employee)
            db.session.flush()
    elif compatible_employees is None:
        kid.compatible_kids = []
        db.session.flush()

    if incompatible_employees:
        for incompatible_employee in incompatible_employees:
            employee = Employee.query.get(incompatible_employee)
            kid.incompatible_employees.append(employee)
            db.session.flush()
    elif incompatible_employees is None:
        kid.incompatible_kids = []
        db.session.flush()

    db.session.commit()

    return kid_schema.dump(kid)


# Delete Kid
@kid_controller.route('/kid/<id>', methods=['DELETE'])
def delete_kid(id):
    kid = Kid.query.get(id)

    compatible_employees = kid.compatible_employees
    incompatible_employees = kid.incompatible_employees
    kid_infos = kid.kid_infos
    shifts = kid.shifts

    for compatible_employee in compatible_employees:
        compatible_employee.compatible_kids.remove(kid)
        db.session.flush()

    for incompatible_employee in incompatible_employees:
        incompatible_employee.incompatible_kids.remove(kid)
        db.session.flush()

    for kid_info in kid_infos:
        db.session.delete(kid_info)

    for shift in shifts:
        db.session.delete(shift)

    db.session.delete(kid)
    db.session.commit()

    return kid_schema.dump(kid)
