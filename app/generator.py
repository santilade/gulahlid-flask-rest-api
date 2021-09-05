from flask import Blueprint, request, jsonify
from app import db
from . import API_BASE_URL
from .models import Agenda, Shift, Role, Group, Employee, EmployeeInfo, Kid, KidInfo
from .schemas import agenda_schema, agendas_schema, shift_schema, shifts_schema, role_schema, roles_schema, \
    group_schema, groups_schema, employee_schema, employees_schema, employee_info_schema, employees_infos_schema, \
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
        self.unassigned_shifts = {}  # {day 1: [Shift, Shift, Shift, ...]}
        self.serialized_unassigned_shifts = {}
        self.free_employees = {}  # {"week 1": {"Monday": [Employee, Employee, ...],"Tuesday": [], ...}, "week 2": ...}
        self.employees_accumulated_workload = {}  # {employee id (int): accumulated workload (int), ...}
        self.closed_circles = {}  # {kid id: [Employee, Employee, ...], kid id: [Employee, Employee, ...]}

    def run(self):
        response = {
            "get_infos()": {
                "Status": self.get_infos(),
                "employees_infos": employees_infos_schema.dump(self.employees_infos),
                "kids_infos": kids_infos_schema.dump(self.kids_infos)
            },

            "set_unassigned_shifts()": {
                "Status": self.set_unassigned_shifts(),
                "unassigned_shifts": self.serialized_unassigned_shifts
            }
        }
        return response

    def get_infos(self):
        filtered_employees_infos = EmployeeInfo.query.filter_by(agenda_id=self.agenda.id)
        for employee_info in filtered_employees_infos:
            self.employees_infos.append(employee_info)

        filtered_kids_infos = KidInfo.query.filter_by(agenda_id=self.agenda.id)
        for kid_info in filtered_kids_infos:
            self.kids_infos.append(kid_info)

        return "DONE!"

    def set_unassigned_shifts(self):
        if self.agenda.rotation_interval == 'daily rotations':

            if self.agenda.workday == 'part-time':

                for rotation in range(1, self.agenda.total_rotations + 1):
                    key = "day "+str(rotation)
                    day_list = []

                    for kid_info in self.kids_infos:
                        if kid_info.attendance[key]:
                            new_shift = Shift(self.agenda.id, rotation, "afternoon", 0, kid_info.kid_id, 0)

                            db.session.add(new_shift)
                            db.session.commit()

                            day_list.append(new_shift)

                    self.unassigned_shifts[key] = day_list
                    self.serialized_unassigned_shifts[key] = shifts_schema.dump(day_list)

            elif self.agenda.workday == 'full-time':

                for rotation in range(1, self.agenda.total_rotations + 1):
                    key = "day "+str(rotation)
                    morning_list = []
                    afternoon_list = []

                    for kid_info in self.kids_infos:
                        if kid_info.attendance[key]:
                            new_morning_shift = Shift(self.agenda.id, rotation, "morning", 0, kid_info.kid_id, 0)
                            new_afternoon_shift = Shift(self.agenda.id, rotation, "afternoon", 0, kid_info.kid_id, 0)

                            db.session.add(new_morning_shift, new_afternoon_shift)
                            db.session.commit()

                            morning_list.append(new_morning_shift)
                            afternoon_list.append(new_afternoon_shift)

                    self.unassigned_shifts[key] = {"morning": morning_list, "afternoon": afternoon_list}
                    self.serialized_unassigned_shifts[key] = {"morning": shifts_schema.dump(morning_list),
                                                              "afternoon": shifts_schema.dump(afternoon_list)}

        return "DONE!"

    # def set_free_employees(self):

    # def calc_employees_accumulated_workload(self):

    # def set_kids_closed_circles(self):

    # def assign_shifts(self):


# ///////////////// RUN GENERATOR /////////////////

# Create Agenda
@generator.route('/generator', methods=['POST'])
def run_generator():
    agenda_id = request.json['agenda_id']
    new_generator = AgendaGenerator(agenda_id)
    response = new_generator.run()
    return jsonify(response)
