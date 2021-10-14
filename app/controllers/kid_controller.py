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
    compatible_kids = []
    incompatible_kids = []
    kid_infos = []
    shifts = []

    new_kid = Kid(name, grade, group_id, compatible_employees, incompatible_employees, compatible_kids,
                  incompatible_kids, kid_infos, shifts)

    db.session.add(new_kid)
    db.session.flush()

    compatible_employees = request.json['compatible_employees']
    incompatible_employees = request.json['incompatible_employees']
    compatible_kids = request.json['compatible_kids']
    incompatible_kids = request.json['incompatible_kids']

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

    if compatible_kids:
        for kid_id in compatible_kids:
            compatible_kid = Kid.query.get(kid_id)
            new_kid.compatible_kids.append(compatible_kid)
            compatible_kid.compatible_kids.append(new_kid)
            db.session.flush()

    if incompatible_kids:
        for kid_id in incompatible_kids:
            incompatible_kid = Kid.query.get(kid_id)
            new_kid.incompatible_kids.append(incompatible_kid)
            incompatible_kid.incompatible_kids.append(new_kid)
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
    compatible_kids = request.json['compatible_kids']
    incompatible_kids = request.json['incompatible_kids']

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
        kid.compatible_employees = []
        db.session.flush()

    if incompatible_employees:
        for incompatible_employee in incompatible_employees:
            employee = Employee.query.get(incompatible_employee)
            kid.incompatible_employees.append(employee)
            db.session.flush()
    elif incompatible_employees is None:
        kid.incompatible_employees = []
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

    if incompatible_kids:
        for old_incompatible_kid in kid.incompatible_kids:
            old_incompatible_kid.incompatible_kids.remove(kid)
            db.session.flush()
        kid.incompatible_kids = []
        db.session.flush()
        for kid_id in incompatible_kids:
            incompatible_kid = Kid.query.get(kid_id)
            kid.incompatible_kids.append(incompatible_kid)
            incompatible_kid.incompatible_kids.append(kid)
            db.session.flush()
    elif incompatible_kids is None:
        for old_incompatible_employee in kid.incompatible_kids:
            old_incompatible_employee.incompatible_kids.remove(kid)
            db.session.flush()
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
    compatible_kids = kid.compatible_kids
    incompatible_kids = kid.incompatible_kids
    kid_infos = kid.kid_infos
    shifts = kid.shifts

    for compatible_employee in compatible_employees:
        compatible_employee.compatible_kids.remove(kid)
        db.session.flush()

    for incompatible_employee in incompatible_employees:
        incompatible_employee.incompatible_kids.remove(kid)
        db.session.flush()

    for compatible_kid in compatible_kids:
        compatible_kid.compatible_kids.remove(kid)
        db.session.flush()

    for incompatible_kid in incompatible_kids:
        incompatible_kid.incompatible_kids.remove(kid)
        db.session.flush()

    for kid_info in kid_infos:
        db.session.delete(kid_info)

    for shift in shifts:
        db.session.delete(shift)

    db.session.delete(kid)
    db.session.commit()

    return kid_schema.dump(kid)
