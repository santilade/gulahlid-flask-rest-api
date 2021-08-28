from flask import Blueprint, request, jsonify
from app import db
from . import API_ENDPOINT
from .models import Agenda, Shift, Role, Group, Employee, EmployeeInfo, Kid, KidInfo
from .schemas import agenda_schema, agendas_schema, shift_schema, shifts_schema, role_schema, roles_schema, \
    group_schema, groups_schema, employee_schema, employees_schema, employee_info_schema, employees_infos_schema,\
    kid_schema, kids_schema, kid_info_schema, kids_infos_schema
import requests


# Defining as a blueprint allows to store routes in different documents or "blueprints"
generator = Blueprint('generator', __name__)


# ///////////////// GENERATOR /////////////////


class AgendaGenerator:
    def __init__(self, agenda_id):
        self.agenda = Agenda.query.get(agenda_id)
        self.employees_infos = []  # [EmployeeInfo, EmployeeInfo, EmployeeInfo, ...]
        self.kids_infos = []  # [KidInfo, KidInfo, KidInfo, ...]
        self.unassigned_shifts = []  # [Shift, Shift, Shift, ...]
        self.free_employees = {}  # {"week 1": {"Monday": [Employee, Employee, ...],"Tuesday": [], ...}, "week 2": ...}
        self.employees_accumulated_workload = {}  # {employee id (int): accumulated workload (int), ...}
        self.closed_circles = {}  # {kid id: [Employee, Employee, ...], kid id: [Employee, Employee, ...]}

    def run(self):
        response = {
            "get_infos()":             {
                                        "Status": self.get_infos(),
                                        "employees_infos": employees_infos_schema.dump(self.employees_infos),
                                        "kids_infos": kids_infos_schema.dump(self.kids_infos)
                                       },

            "set_unassigned_shifts()": {
                                        "Status": self.set_unassigned_shifts(),
                                        "unassigned_shifts": shifts_schema.dump(self.unassigned_shifts)
                                       }
        }
        return response

    def get_infos(self):
        # get employees_infos
        filtered_employees_infos = EmployeeInfo.query.filter_by(agenda_id=self.agenda.id)
        for employee_info in filtered_employees_infos:
            self.employees_infos.append(employee_info)

        # get kids_infos
        filtered_kids_infos = KidInfo.query.filter_by(agenda_id=self.agenda.id)
        for kid_info in filtered_kids_infos:
            self.kids_infos.append(kid_info)

        return "SUCCESS"

    def set_unassigned_shifts(self):
        # filtered_kids_infos = KidInfo.query.filter_by(agenda_id=self.agenda.id)
        #
        # if self.agenda.rotation_interval == 'daily rotations':
        #     for day in range(1, self.agenda.total_rotations + 1):
        #         for kid_info in filtered_kids_infos:
        #             if kid_info.attendance["day " + day]:
        #                 print("foo")

        return "SUCCESS"


# ///////////////// RUN GENERATOR /////////////////

# Create Agenda
@generator.route('/generator', methods=['POST'])
def run_generator():
    agenda_id = request.json['agenda_id']
    new_generator = AgendaGenerator(agenda_id)
    response = new_generator.run()
    return jsonify(response)


# Create Agenda
# @generator.route('/generator', methods=['POST'])
# def generate_shifts():
#     agenda_id = request.json['agenda_id']
#     agenda = Agenda.query.get(agenda_id)
#     employees_attendance = {}
#
#     if agenda.rotation_interval == 'weekly rotations':
#         weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
#
#         for rotation in agenda.total_rotations:
#             employees_attendance['week ' + str(rotation)] = {}
#
#             for day in weekdays:
#                 params = {'agenda_id': agenda_id, 'attendance': {'week ' + str(rotation): {day: True}}}
#                 filtered_employees_infos = EmployeeInfo.query.filter_by(params)
#
#                 attending_employees = []
#                 for employee_info in filtered_employees_infos:
#                     attending_employees.append(employee_info.employee_id)
#
#                 employees_attendance['week ' + str(rotation)] = {day: attending_employees}
#
#     elif agenda.rotation_interval == 'daily rotations':
#         for rotation in agenda.total_rotations:
#             employees_attendance['day ' + str(rotation)] = {}
#
#             for day in agenda.total_rotations:
#                 params = {'agenda_id': agenda_id, 'attendance': {'day ' + str(rotation): True}}
#                 filtered_employees_infos = EmployeeInfo.query.filter_by(params)
#
#                 attending_employees = []
#                 for employee_info in filtered_employees_infos:
#                     attending_employees.append(employee_info.employee_id)
#
#                 employees_attendance['day ' + str(rotation)] = attending_employees
#
#
#     return "foo"
