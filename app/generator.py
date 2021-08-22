from flask import Blueprint, request, jsonify
from app import db
from . import API_ENDPOINT
from .models import Agenda, Shift, Role, Group, Employee, EmployeeInfo, Kid, KidInfo
from .schemas import agenda_schema, agendas_schema, shift_schema, role_schema, roles_schema, group_schema, \
    groups_schema, employee_schema, employees_schema, employee_info_schema, employees_infos_schema, kid_schema, \
    kids_schema, kid_info_schema, kids_infos_schema
import requests


# Defining as a blueprint allows to store routes in different documents or "blueprints"
generator = Blueprint('generator', __name__)


# ///////////////// AGENDA /////////////////

# Create Agenda
@generator.route('/generator', methods=['POST'])
def generate_shifts():
    # get agenda id
    agenda_id = request.json['agenda_id']
    agenda = Agenda.query.get(agenda_id)
    # get dictionary of employees attendance
    employees_attendance = {}

    if agenda.rotation_interval == 'weekly rotations':
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

        for rotation in agenda.total_rotations:
            employees_attendance['week ' + str(rotation)] = {}

            for day in weekdays:
                params = {'agenda_id': agenda_id, 'attendance': {'week ' + str(rotation): {day: True}}}
                filtered_employees_infos = EmployeeInfo.query.filter_by(params)

                attending_employees = []
                for employee_info in filtered_employees_infos:
                    attending_employees.append(employee_info.employee_id)

                employees_attendance['week ' + str(rotation)] = {day: attending_employees}

    elif agenda.rotation_interval == 'daily rotations':
        for rotation in agenda.total_rotations:
            employees_attendance['day ' + str(rotation)] = {}

            for day in agenda.total_rotations:
                params = {'agenda_id': agenda_id, 'attendance': {'day ' + str(rotation): True}}
                filtered_employees_infos = EmployeeInfo.query.filter_by(params)

                attending_employees = []
                for employee_info in filtered_employees_infos:
                    attending_employees.append(employee_info.employee_id)

                employees_attendance['day ' + str(rotation)] = attending_employees

    # get dictionary of kids per day

    # get dictionary of difficult kids and their circle of employees
    # get dictionary of kids with two employees

    # create shifts

    return "foo"
