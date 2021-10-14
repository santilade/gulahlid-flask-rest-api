from flask import Blueprint, request, jsonify
from app import db
from app.models import Employee, Kid
from app.schemas import employee_schema, employees_schema

employee_controller = Blueprint('employee_controller', __name__)


# ///////////////// EMPLOYEE /////////////////
# Add Employee
@employee_controller.route('/employee', methods=['POST'])
def add_employee():
    name = request.json['name']
    compatible_kids = []
    incompatible_kids = []
    compatible_employees = []
    incompatible_employees = []
    employee_infos = []
    shifts = []

    new_employee = Employee(name, compatible_kids, incompatible_kids, compatible_employees, incompatible_employees,
                            employee_infos, shifts)

    db.session.add(new_employee)
    db.session.flush()

    compatible_kids = request.json['compatible_kids']
    incompatible_kids = request.json['incompatible_kids']
    compatible_employees = request.json['compatible_employees']
    incompatible_employees = request.json['incompatible_employees']

    if compatible_kids:
        for kid_id in compatible_kids:
            kid = Kid.query.get(kid_id)
            new_employee.compatible_kids.append(kid)
            db.session.flush()

    if incompatible_kids:
        for kid_id in incompatible_kids:
            kid = Kid.query.get(kid_id)
            new_employee.incompatible_kids.append(kid)
            db.session.flush()

    if compatible_employees:
        for employee_id in compatible_employees:
            compatible_employee = Employee.query.get(employee_id)
            new_employee.compatible_employees.append(compatible_employee)
            compatible_employee.compatible_employees.append(new_employee)
            db.session.flush()

    if incompatible_employees:
        for employee_id in incompatible_employees:
            incompatible_employee = Employee.query.get(employee_id)
            new_employee.incompatible_employees.append(incompatible_employee)
            incompatible_employee.incompatible_employees.append(new_employee)
            db.session.flush()

    db.session.commit()

    return employee_schema.dump(new_employee)


# Get All Employees
@employee_controller.route('/employee', methods=['GET'])
def get_employees():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)

    return jsonify(result)


# Get Single Employee
@employee_controller.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)

    return employee_schema.dump(employee)


# Update Employee
@employee_controller.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)

    name = request.json['name']
    compatible_kids = request.json['compatible_kids']
    incompatible_kids = request.json['incompatible_kids']
    compatible_employees = request.json['compatible_employees']
    incompatible_employees = request.json['incompatible_employees']

    if name != "":
        employee.name = name
        db.session.flush()

    if compatible_kids:
        employee.compatible_kids = []
        db.session.flush()
        for kid_id in compatible_kids:
            kid = Kid.query.get(kid_id)
            employee.compatible_kids.append(kid)
            db.session.flush()
    elif compatible_kids is None:
        employee.compatible_kids = []
        db.session.flush()

    if incompatible_kids:
        employee.incompatible_kids = []
        db.session.flush()
        for kid_id in incompatible_kids:
            kid = Kid.query.get(kid_id)
            employee.incompatible_kids.append(kid)
            db.session.flush()
    elif incompatible_kids is None:
        employee.incompatible_kids = []
        db.session.flush()

    if compatible_employees:
        for old_compatible_employee in employee.compatible_employees:
            old_compatible_employee.compatible_employees.remove(employee)
            db.session.flush()
        employee.compatible_employees = []
        db.session.flush()
        for employee_id in compatible_employees:
            compatible_employee = Employee.query.get(employee_id)
            employee.compatible_employees.append(compatible_employee)
            compatible_employee.compatible_employees.append(employee)
            db.session.flush()
    elif compatible_employees is None:
        for old_compatible_employee in employee.compatible_employees:
            old_compatible_employee.compatible_employees.remove(employee)
            db.session.flush()
        employee.compatible_employees = []
        db.session.flush()

    if incompatible_employees:
        for old_incompatible_employee in employee.incompatible_employees:
            old_incompatible_employee.incompatible_employees.remove(employee)
            db.session.flush()
        employee.incompatible_employees = []
        db.session.flush()
        for employee_id in incompatible_employees:
            incompatible_employee = Employee.query.get(employee_id)
            employee.incompatible_employees.append(incompatible_employee)
            incompatible_employee.incompatible_employees.append(employee)
            db.session.flush()
    elif incompatible_employees is None:
        for old_incompatible_employee in employee.incompatible_employees:
            old_incompatible_employee.incompatible_employees.remove(employee)
            db.session.flush()
        employee.incompatible_employees = []
        db.session.flush()

    db.session.commit()

    return employee_schema.dump(employee)


# Delete Employee
@employee_controller.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)

    compatible_kids = employee.compatible_kids
    incompatible_kids = employee.incompatible_kids
    compatible_employees = employee.compatible_employees
    incompatible_employees = employee.incompatible_employees
    employee_infos = employee.employee_infos
    shifts = employee.shifts


    for compatible_kid in compatible_kids:
        compatible_kid.compatible_employees.remove(employee)
        db.session.flush()

    for incompatible_kid in incompatible_kids:
        incompatible_kid.incompatible_employees.remove(employee)
        db.session.flush()

    for compatible_employee in compatible_employees:
        compatible_employee.compatible_employees.remove(employee)
        db.session.flush()

    for incompatible_employee in incompatible_employees:
        incompatible_employee.incompatible_employees.remove(employee)
        db.session.flush()

    for employee_info in employee_infos:
        db.session.delete(employee_info)

    for shift in shifts:
        db.session.delete(shift)

    db.session.delete(employee)
    db.session.commit()

    return employee_schema.dump(employee)

