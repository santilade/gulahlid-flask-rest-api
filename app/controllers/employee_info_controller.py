from flask import Blueprint, request, jsonify
from app import db
from app.models import EmployeeInfo
from app.schemas import employee_info_schema, employees_infos_schema

employee_info_controller = Blueprint('employee_info_controller', __name__)


# ///////////////// EMPLOYEE INFO /////////////////
# Add EmployeeInfo
@employee_info_controller.route('/employee_info', methods=['POST'])
def add_employee_info():
    employee_id = request.json['employee_id']
    attendance = request.json['attendance']
    agenda_id = request.json['agenda_id']

    new_employee_info = EmployeeInfo(employee_id, attendance, agenda_id)

    db.session.add(new_employee_info)
    db.session.commit()

    return employee_info_schema.dump(new_employee_info)


# Get All Employees Infos
@employee_info_controller.route('/employee_info', methods=['GET'])
def get_employee_infos():
    all_employee_infos = EmployeeInfo.query.all()
    result = employees_infos_schema.dump(all_employee_infos)

    return jsonify(result)


# Get Single Employee Info
@employee_info_controller.route('/employee_info/<id>', methods=['GET'])
def get_employee_info(id):
    employee_info = EmployeeInfo.query.get(id)

    return employee_info_schema.dump(employee_info)


# Update Employee Info
@employee_info_controller.route('/employee_info/<id>', methods=['PUT'])
def update_employee_info(id):
    employee_info = EmployeeInfo.query.get(id)

    attendance = request.json['attendance']

    if attendance:
        employee_info.attendance = attendance

    db.session.commit()

    return employee_info_schema.dump(employee_info)


# Delete Employee Info
@employee_info_controller.route('/employee_info/<id>', methods=['DELETE'])
def delete_employee_info(id):
    employee_info = EmployeeInfo.query.get(id)

    db.session.delete(employee_info)
    db.session.commit()

    return employee_info_schema.dump(employee_info)
