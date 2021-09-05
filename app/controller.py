from flask import Blueprint, request, jsonify
from app import db
from . import API_ENDPOINT
from .models import Agenda, Shift, Role, Group, Employee, EmployeeInfo, Kid, KidInfo
from .schemas import agenda_schema, agendas_schema, shift_schema, shifts_schema, role_schema, roles_schema, group_schema, \
    groups_schema, employee_schema, employees_schema, employee_info_schema, employees_infos_schema, kid_schema, \
    kids_schema, kid_info_schema, kids_infos_schema
import requests


# Defining as a blueprint allows to store routes in different documents or "blueprints"
controller = Blueprint('controller', __name__)


# ///////////////// AGENDA /////////////////

# Create Agenda
@controller.route('/agenda', methods=['POST'])
def add_agenda():
    title = request.json['title']
    workday = request.json['workday']
    rotation_interval = request.json['rotation_interval']
    total_rotations = request.json['total_rotations']
    kids_infos = []
    employees_infos = []
    shifts = []

    new_agenda = Agenda(title, workday, rotation_interval, total_rotations, kids_infos, employees_infos, shifts)

    db.session.add(new_agenda)
    db.session.commit()

    return agenda_schema.dump(new_agenda)


# Get All Agendas
@controller.route('/agenda', methods=['GET'])
def get_agendas():
    all_agendas = Agenda.query.all()
    result = agendas_schema.dump(all_agendas)
    return jsonify(result)


# Get Single Agenda
@controller.route('/agenda/<id>', methods=['GET'])
def get_agenda(id):
    agenda = Agenda.query.get(id)
    return agenda_schema.dump(agenda)


# Update Agenda
@controller.route('/agenda/<id>', methods=['PUT'])
def update_agenda(id):
    agenda = Agenda.query.get(id)

    title = request.json['title']
    agenda.title = title

    employees_infos = request.json['employees_infos']
    for employee_info in employees_infos:
        response = requests.post(API_ENDPOINT + '/employee_info', json=employee_info)
        print(response.text)

    kids_infos = request.json['kids_infos']
    for kid_info in kids_infos:
        response = requests.post(API_ENDPOINT + '/kid_info', json=kid_info)
        print(response.text)

    db.session.commit()

    return agenda_schema.dump(agenda)


# Delete Agenda
@controller.route('/agenda/<id>', methods=['DELETE'])
def delete_agenda(id):
    agenda = Agenda.query.get(id)
    kids_infos = agenda.kids_infos
    employees_infos = agenda.employees_infos
    shifts = agenda.shifts

    for kid_info in kids_infos:
        db.session.delete(kid_info)

    for employee_info in employees_infos:
        db.session.delete(employee_info)

    for shift in shifts:
        db.session.delete(shift)

    db.session.delete(agenda)
    db.session.commit()

    return agenda_schema.dump(agenda)


# ///////////////// SHIFT /////////////////

# Get All Shifts
@controller.route('/shift', methods=['GET'])
def get_shifts():
    all_shifts = Shift.query.all()
    result = shifts_schema.dump(all_shifts)
    return jsonify(result)


# Get Single Shift
@controller.route('/shift/<id>', methods=['GET'])
def get_shift(id):
    shift = Shift.query.get(id)
    return agenda_schema.dump(shift)


# Update Shift
@controller.route('/shift/<id>', methods=['PUT'])
def update_shift(id):
    shift = Shift.query.get(id)

    employee_id = request.json['employee_id']
    kid_id = request.json['kid_id']
    role_id = request.json['role_id']

    shift.employee_id = employee_id
    shift.kid_id = kid_id
    shift.role_id = role_id

    db.session.commit()

    return shift_schema.dump(shift)


# Delete Shift
@controller.route('/shift/<id>', methods=['DELETE'])
def delete_shift(id):
    shift = Shift.query.get(id)

    db.session.delete(shift)
    db.session.commit()

    return agenda_schema.dump(shift)


# ///////////////// ROLE /////////////////

# Create Role
@controller.route('/role', methods=['POST'])
def add_role():
    title = request.json['title']
    description = request.json['description']
    employees_needed = request.json['employees_needed']
    employee_proportion = request.json['employee_proportion']
    shifts = []

    new_role = Role(title, description, employees_needed, employee_proportion, shifts)

    db.session.add(new_role)
    db.session.commit()

    return role_schema.dump(new_role)


# Get All Roles
@controller.route('/role', methods=['GET'])
def get_roles():
    all_roles = Role.query.all()
    result = roles_schema.dump(all_roles)
    return jsonify(result)


# Get Single Role
@controller.route('/role/<id>', methods=['GET'])
def get_role(id):
    role = Role.query.get(id)
    return role_schema.dump(role)


# Update Role
@controller.route('/role/<id>', methods=['PUT'])
def update_role(id):
    role = Role.query.get(id)

    title = request.json['title']
    description = request.json['description']
    employees_needed = request.json['employees_needed']
    employee_proportion = request.json['employee_proportion']

    role.title = title
    role.description = description
    role.employees_needed = employees_needed
    role.employee_proportion = employee_proportion

    db.session.commit()

    return role_schema.dump(role)


# Delete Role
@controller.route('/role/<id>', methods=['DELETE'])
def delete_role(id):
    role = Role.query.get(id)

    db.session.delete(role)
    db.session.commit()

    return role_schema.dump(role)


# ///////////////// GROUP /////////////////

# Create Group
@controller.route('/group', methods=['POST'])
def add_group():
    title = request.json['title']
    color = request.json['color']
    kids = []

    new_group = Group(title, color, kids)

    db.session.add(new_group)
    db.session.commit()

    return group_schema.dump(new_group)


# Get All Groups
@controller.route('/group', methods=['GET'])
def get_groups():
    all_groups = Group.query.all()
    result = groups_schema.dump(all_groups)
    return jsonify(result)


# Get Single Group
@controller.route('/group/<id>', methods=['GET'])
def get_group(id):
    group = Group.query.get(id)
    return group_schema.dump(group)


# Update Group
@controller.route('/group/<id>', methods=['PUT'])
def update_group(id):
    group = Group.query.get(id)

    title = request.json['title']
    color = request.json['color']

    group.title = title
    group.color = color

    db.session.commit()

    return group_schema.dump(group)


# Delete Group
@controller.route('/group/<id>', methods=['DELETE'])
def delete_group(id):
    group = Group.query.get(id)
    kids = group.kids

    for kid in kids:
        db.session.delete(kid)

    db.session.delete(group)
    db.session.commit()

    return group_schema.dump(group)


# ///////////////// EMPLOYEE /////////////////

# Create Employee
@controller.route('/employee', methods=['POST'])
def add_employee():
    name = request.json['name']
    compatible_kids = []
    incompatible_kids = []
    employee_infos = []
    shifts = []

    new_employee = Employee(name, compatible_kids, incompatible_kids, employee_infos, shifts)

    db.session.add(new_employee)
    db.session.flush()

    compatible_kids = request.json['compatible_kids']
    for compatible_kid in compatible_kids:
        kid = Kid.query.get(compatible_kid)
        kid.compatible_employees.append(new_employee)
        db.session.flush()

    incompatible_kids = request.json['incompatible_kids']
    for incompatible_kid in incompatible_kids:
        kid = Kid.query.get(incompatible_kid)
        kid.incompatible_employees.append(new_employee)
        db.session.flush()

    db.session.commit()

    return employee_schema.dump(new_employee)


# Get All Employees
@controller.route('/employee', methods=['GET'])
def get_employees():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result)


# Get Single Employee
@controller.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return employee_schema.dump(employee)


# Update Employee
@controller.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)

    name = request.json['name']

    employee.name = name
    employee.compatible_kids = []
    employee.incompatible_kids = []
    db.session.flush()

    compatible_kids = request.json['compatible_kids']
    for kid_id in compatible_kids:
        kid = Kid.query.get(kid_id)
        kid.compatible_employees.append(employee)
        db.session.flush()

    incompatible_kids = request.json['incompatible_kids']
    for kid_id in incompatible_kids:
        kid = Kid.query.get(kid_id)
        kid.incompatible_employees.append(employee)
        db.session.flush()

    db.session.commit()

    return employee_schema.dump(employee)


# Delete Employee
@controller.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    compatible_kids = employee.compatible_kids
    incompatible_kids = employee.incompatible_kids
    employee_infos = employee.employee_infos
    shifts = employee.shifts

    for compatible_kid in compatible_kids:
        kid = Kid.query.get(compatible_kid)
        kid.compatible_employees.remove(employee)
        db.session.flush()

    for incompatible_kid in incompatible_kids:
        kid = Kid.query.get(incompatible_kid)
        kid.incompatible_employees.remove(employee)
        db.session.flush()

    for employee_info in employee_infos:
        db.session.delete(employee_info)

    for shift in shifts:
        db.session.delete(shift)

    db.session.delete(employee)
    db.session.commit()

    return employee_schema.dump(employee)


# ///////////////// EMPLOYEE INFO /////////////////

# Create Employee Info
@controller.route('/employee_info', methods=['POST'])
def add_employee_info():
    employee_id = request.json['employee_id']
    comments = request.json['comments']
    attendance = request.json['attendance']
    agenda_id = request.json['agenda_id']

    new_employee_info = EmployeeInfo(employee_id, comments, attendance, agenda_id)

    db.session.add(new_employee_info)
    db.session.commit()

    return employee_info_schema.dump(new_employee_info)


# Get All Employees Infos
@controller.route('/employee_info', methods=['GET'])
def get_employee_infos():
    all_employee_infos = EmployeeInfo.query.all()
    result = employees_infos_schema.dump(all_employee_infos)
    return jsonify(result)


# Get Single Employee Info
@controller.route('/employee_info/<id>', methods=['GET'])
def get_employee_info(id):
    employee_info = EmployeeInfo.query.get(id)
    return employee_info_schema.dump(employee_info)


# Update Employee Info
@controller.route('/employee_info/<id>', methods=['PUT'])
def update_employee_info(id):
    employee_info = EmployeeInfo.query.get(id)

    comments = request.json['comments']
    attendance = request.json['attendance']

    employee_info.comments = comments
    employee_info.attendance = attendance

    db.session.commit()

    return employee_info_schema.dump(employee_info)


# Delete Employee Info
@controller.route('/employee_info/<id>', methods=['DELETE'])
def delete_employee_info(id):
    employee_info = EmployeeInfo.query.get(id)

    db.session.delete(employee_info)
    db.session.commit()

    return employee_info_schema.dump(employee_info)


# ///////////////// KID /////////////////

# Create Kid
@controller.route('/kid', methods=['POST'])
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
    for compatible_employee in compatible_employees:
        kid = Kid.query.get(compatible_employee)
        kid.compatible_employees.append(new_kid)
        db.session.flush()

    incompatible_employees = request.json['incompatible_employees']
    for incompatible_employee in incompatible_employees:
        kid = Kid.query.get(incompatible_employee)
        kid.incompatible_employees.append(new_kid)
        db.session.flush()

    db.session.commit()

    return kid_schema.dump(new_kid)


# Get All Kids
@controller.route('/kid', methods=['GET'])
def get_kids():
    all_kids = Kid.query.all()
    result = kids_schema.dump(all_kids)
    return jsonify(result)


# Get Single Kid
@controller.route('/kid/<id>', methods=['GET'])
def get_kid(id):
    kid = Kid.query.get(id)
    return kid_schema.dump(kid)


# Update Kid
@controller.route('/kid/<id>', methods=['PUT'])
def update_kid(id):
    kid = Kid.query.get(id)

    name = request.json['name']
    grade = request.json['grade']
    group_id = request.json['group_id']

    kid.name = name
    kid.grade = grade
    kid.group_id = group_id
    kid.compatible_employees = []
    kid.incompatible_employees = []
    db.session.flush()

    compatible_employees = request.json['compatible_employees']
    for compatible_employee in compatible_employees:
        employee = Employee.query.get(compatible_employee)
        employee.compatible_kids.append(kid)
        db.session.flush()

    incompatible_employees = request.json['incompatible_employees']
    for incompatible_employee in incompatible_employees:
        employee = Employee.query.get(incompatible_employee)
        employee.incompatible_kids.append(kid)
        db.session.flush()

    db.session.commit()

    return kid_schema.dump(kid)


# Delete Kid
@controller.route('/kid/<id>', methods=['DELETE'])
def delete_kid(id):
    kid = Kid.query.get(id)
    compatible_employees = kid.compatible_kids
    incompatible_employees = kid.incompatible_kids
    kid_infos = kid.kid_infos
    shifts = kid.shifts

    for compatible_employee in compatible_employees:
        employee = Employee.query.get(compatible_employee)
        employee.compatible_kids.remove(kid)
        db.session.flush()

    for incompatible_employee in incompatible_employees:
        employee = Employee.query.get(incompatible_employee)
        employee.incompatible_kids.remove(kid)
        db.session.flush()

    for kid_info in kid_infos:
        db.session.delete(kid_info)

    for shift in shifts:
        db.session.delete(shift)

    db.session.delete(kid)
    db.session.commit()

    return kid_schema.dump(kid)


# ///////////////// KID INFO /////////////////

# Create Kid Info
@controller.route('/kid_info', methods=['POST'])
def add_kid_info():
    kid_id = request.json['kid_id']
    important = request.json['important']
    arrival_time = request.json['arrival_time']
    departure_time = request.json['departure_time']
    medication_time = request.json['medication_time']
    transport = request.json['transport']
    wheelchair = request.json['wheelchair']
    difficulty = request.json['difficulty']
    employees_needed = request.json['employees_needed']
    other_info = request.json['other_info']
    attendance = request.json['attendance']
    agenda_id = request.json['agenda_id']

    new_kid_info = KidInfo(kid_id, important, arrival_time, departure_time, medication_time, transport, wheelchair,
                           difficulty, employees_needed, other_info, attendance, agenda_id)

    db.session.add(new_kid_info)
    db.session.commit()

    return kid_info_schema.dump(new_kid_info)


# Get All Kids Infos
@controller.route('/kid_info', methods=['GET'])
def get_kids_info():
    all_kids_info = KidInfo.query.all()
    result = kids_infos_schema.dump(all_kids_info)
    return jsonify(result)


# Get Single Kid Info
@controller.route('/kid_info/<id>', methods=['GET'])
def get_kid_info(id):
    kid_info = KidInfo.query.get(id)
    return kid_info_schema.dump(kid_info)


# Update Kid Info
@controller.route('/kid_info/<id>', methods=['PUT'])
def update_kid_info(id):
    kid_info = KidInfo.query.get(id)

    important = request.json['important']
    arrival_time = request.json['arrival_time']
    departure_time = request.json['departure_time']
    medication_time = request.json['medication_time']
    transport = request.json['transport']
    wheelchair = request.json['wheelchair']
    difficulty = request.json['difficulty']
    employees_needed = request.json['employees_needed']
    other_info = request.json['other_info']
    attendance = request.json['attendance']

    kid_info.important = important
    kid_info.arrival_time = arrival_time
    kid_info.departure_time = departure_time
    kid_info.medication_time = medication_time
    kid_info.transport = transport
    kid_info.wheelchair = wheelchair
    kid_info.difficulty = difficulty
    kid_info.employees_needed = employees_needed
    kid_info.other_info = other_info
    kid_info.attendance = attendance

    db.session.commit()

    return kid_info_schema.dump(kid_info)


# Delete Kid Info
@controller.route('/kid_info/<id>', methods=['DELETE'])
def delete_kid_info(id):
    kid_info = KidInfo.query.get(id)

    db.session.delete(kid_info)
    db.session.commit()

    return kid_info_schema.dump(kid_info)
