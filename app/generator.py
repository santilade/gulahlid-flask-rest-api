from flask import Blueprint, request, jsonify
from app import db
from . import API_BASE_URL
from .models import Calendar, Shift, Group, Employee, EmployeeInfo, Kid, KidInfo
from .schemas import calendar_schema, calendars_schema, shift_schema, shifts_schema, group_schema, groups_schema, \
    employee_schema, employees_schema, employee_info_schema, employees_infos_schema, kid_schema, kids_schema, \
    kid_info_schema, kids_infos_schema
import requests

# Defining as a blueprint allows to store routes in different documents or "blueprints"
generator = Blueprint('generator', __name__)


# ///////////////// GENERATOR /////////////////


class CalendarGenerator:
    def __init__(self, calendar_id):
        self.calendar = Calendar.query.get(calendar_id)
        self.employees_infos = []  # [EmployeeInfo, EmployeeInfo, EmployeeInfo, ...]
        self.kids_infos = []  # [KidInfo, KidInfo, KidInfo, ...]
        self.unassigned_shifts = {}  # {day 1: [Shift, Shift, Shift, ...]}
        self.serialized_unassigned_shifts = {}
        self.free_employees = {}  # {"week 1": {"Monday": [Employee, Employee, ...],"Tuesday": [], ...}, "week 2": ...}
        self.serialized_free_employees = {}
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
            },

            "set_free_employees()": {
                "Status": self.set_free_employees(),
                "unassigned_shifts": self.serialized_free_employees
            }
        }
        return response

    def get_infos(self):
        filtered_employees_infos = EmployeeInfo.query.filter_by(calendar_id=self.calendar.id)
        for employee_info in filtered_employees_infos:
            self.employees_infos.append(employee_info)

        filtered_kids_infos = KidInfo.query.filter_by(calendar_id=self.calendar.id)
        for kid_info in filtered_kids_infos:
            self.kids_infos.append(kid_info)

        return "DONE!"

    def set_unassigned_shifts(self):
        # DAILY ROTATIONS
        if self.calendar.rotation_interval == 'daily rotations':
            for rotation in range(1, self.calendar.total_rotations + 1):
                day = "day " + str(rotation)
                self.unassigned_shifts[day] = {}
                self.serialized_unassigned_shifts[day] = {}

                # part-time
                if self.calendar.workday == 'part-time':
                    self.unassigned_shifts[day]["afternoon"] = []
                    self.serialized_unassigned_shifts[day]["afternoon"] = []

                    for kid_info in self.kids_infos:
                        if kid_info.attendance[day]["afternoon"]:
                            new_shift = Shift(self.calendar.id, rotation, 0, "afternoon", 0, kid_info.kid_id)
                            db.session.add(new_shift)

                            self.unassigned_shifts[day]["afternoon"].append(new_shift)

                    db.session.commit()

                    self.serialized_unassigned_shifts[day]["afternoon"] = \
                        shifts_schema.dump(self.unassigned_shifts[day]["afternoon"])

                # full-time
                elif self.calendar.workday == 'full-time':
                    self.unassigned_shifts[day]["morning"] = []
                    self.unassigned_shifts[day]["afternoon"] = []
                    self.serialized_unassigned_shifts[day]["morning"] = []
                    self.serialized_unassigned_shifts[day]["afternoon"] = []

                    for kid_info in self.kids_infos:
                        if kid_info.attendance[day]["morning"]:
                            new_morning_shift = Shift(self.calendar.id, rotation, 0, "morning", 0, kid_info.kid_id)
                            db.session.add(new_morning_shift)
                            self.unassigned_shifts[day]["morning"].append(new_morning_shift)

                        if kid_info.attendance[day]["afternoon"]:
                            new_afternoon_shift = Shift(self.calendar.id, rotation, 0, "afternoon", 0, kid_info.kid_id)
                            db.session.add(new_afternoon_shift)
                            self.unassigned_shifts[day]["afternoon"].append(new_afternoon_shift)

                    db.session.commit()

                    self.serialized_unassigned_shifts[day]["morning"] = \
                        shifts_schema.dump(self.unassigned_shifts[day]["morning"])
                    self.serialized_unassigned_shifts[day]["afternoon"] = \
                        shifts_schema.dump(self.unassigned_shifts[day]["afternoon"])

        # WEEKLY ROTATIONS
        elif self.calendar.rotation_interval == 'weekly rotations':
            for rotation in range(1, self.calendar.total_rotations + 1):
                week = "week " + str(rotation)
                self.unassigned_shifts[week] = {}
                self.serialized_unassigned_shifts[week] = {}

                for weekday in range(1, 6):
                    day = "day " + str(weekday)
                    self.unassigned_shifts[week][day] = {}
                    self.serialized_unassigned_shifts[week][day] = {}

                    # part-time
                    if self.calendar.workday == 'part-time':
                        self.unassigned_shifts[week][day]["afternoon"] = []
                        self.serialized_unassigned_shifts[week][day]["afternoon"] = []

                        for kid_info in self.kids_infos:
                            if kid_info.attendance[week][day]["afternoon"]:
                                new_shift = Shift(self.calendar.id, rotation, weekday, "afternoon", 0, kid_info.kid_id)
                                db.session.add(new_shift)

                                self.unassigned_shifts[week][day]["afternoon"].append(new_shift)

                        db.session.commit()

                        self.serialized_unassigned_shifts[week][day]["afternoon"] = \
                            shifts_schema.dump(self.unassigned_shifts[week][day]["afternoon"])

                    # full-time
                    elif self.calendar.workday == 'full-time':
                        self.unassigned_shifts[week][day]["morning"] = []
                        self.unassigned_shifts[week][day]["afternoon"] = []
                        self.serialized_unassigned_shifts[week][day]["morning"] = []
                        self.serialized_unassigned_shifts[week][day]["afternoon"] = []

                        for kid_info in self.kids_infos:
                            if kid_info.attendance[week][day]["morning"]:
                                new_morning_shift = Shift(self.calendar.id, rotation, weekday, "morning", 0,
                                                          kid_info.kid_id)
                                db.session.add(new_morning_shift)
                                self.unassigned_shifts[week][day]["morning"].append(new_morning_shift)

                            if kid_info.attendance[week][day]["afternoon"]:
                                new_afternoon_shift = Shift(self.calendar.id, rotation, weekday, "afternoon", 0,
                                                            kid_info.kid_id)
                                db.session.add(new_afternoon_shift)
                                self.unassigned_shifts[week][day]["afternoon"].append(new_afternoon_shift)

                        db.session.commit()

                        self.serialized_unassigned_shifts[week][day]["morning"] = \
                            shifts_schema.dump(self.unassigned_shifts[week][day]["morning"])
                        self.serialized_unassigned_shifts[week][day]["afternoon"] = \
                            shifts_schema.dump(self.unassigned_shifts[week][day]["afternoon"])

        return "DONE!"

    def set_free_employees(self):
        # DAILY ROTATIONS
        if self.calendar.rotation_interval == 'daily rotations':
            for rotation in range(1, self.calendar.total_rotations + 1):
                day = "day " + str(rotation)
                self.free_employees[day] = {}
                self.serialized_free_employees[day] = {}

                # part-time
                if self.calendar.workday == 'part-time':
                    self.free_employees[day]["afternoon"] = []
                    self.serialized_free_employees[day]["afternoon"] = []

                    for employee_info in self.employees_infos:
                        if employee_info.attendance[day]["afternoon"]:
                            employee = Employee.query.get(employee_info.employee_id)
                            self.free_employees[day]["afternoon"].append(employee)

                    self.serialized_free_employees[day]["afternoon"] = \
                        employees_schema.dump(self.free_employees[day]["afternoon"])

                # full-time
                elif self.calendar.workday == 'full-time':
                    self.free_employees[day]["morning"] = []
                    self.free_employees[day]["afternoon"] = []
                    self.serialized_free_employees[day]["morning"] = []
                    self.serialized_free_employees[day]["afternoon"] = []

                    for employee_info in self.employees_infos:
                        if employee_info.attendance[day]["morning"]:
                            employee = Employee.query.get(employee_info.employee_id)
                            self.free_employees[day]["morning"].append(employee)

                        if employee_info.attendance[day]["afternoon"]:
                            employee = Employee.query.get(employee_info.employee_id)
                            self.free_employees[day]["afternoon"].append(employee)

                    self.serialized_free_employees[day]["morning"] = \
                        employees_schema.dump(self.free_employees[day]["morning"])
                    self.serialized_free_employees[day]["afternoon"] = \
                        employees_schema.dump(self.free_employees[day]["afternoon"])

        # WEEKLY ROTATIONS
        elif self.calendar.rotation_interval == 'weekly rotations':
            for rotation in range(1, self.calendar.total_rotations + 1):
                week = "week " + str(rotation)
                self.free_employees[week] = {}
                self.serialized_free_employees[week] = {}

                for weekday in range(1, 6):
                    day = "day " + str(weekday)
                    self.free_employees[week][day] = {}
                    self.serialized_free_employees[week][day] = {}

                    # part-time
                    if self.calendar.workday == 'part-time':
                        self.free_employees[week][day]["afternoon"] = []
                        self.serialized_free_employees[week][day]["afternoon"] = []

                        for employee_info in self.employees_infos:
                            if employee_info.attendance[week][day]["afternoon"]:
                                employee = Employee.query.get(employee_info.employee_id)
                                self.free_employees[week][day]["afternoon"].append(employee)

                        self.serialized_free_employees[week][day]["afternoon"] = \
                            employees_schema.dump(self.free_employees[week][day]["afternoon"])

                    # full-time
                    elif self.calendar.workday == 'full-time':
                        self.free_employees[week][day]["morning"] = []
                        self.free_employees[week][day]["afternoon"] = []
                        self.serialized_free_employees[week][day]["morning"] = []
                        self.serialized_free_employees[week][day]["afternoon"] = []

                        for employee_info in self.employees_infos:
                            if employee_info.attendance[week][day]["morning"]:
                                employee = Employee.query.get(employee_info.employee_id)
                                self.free_employees[week][day]["morning"].append(employee)

                            if employee_info.attendance[week][day]["afternoon"]:
                                employee = Employee.query.get(employee_info.employee_id)
                                self.free_employees[week][day]["afternoon"].append(employee)

                        self.serialized_free_employees[week][day]["morning"] = \
                            employees_schema.dump(self.free_employees[week][day]["morning"])
                        self.serialized_free_employees[week][day]["afternoon"] = \
                            employees_schema.dump(self.free_employees[week][day]["afternoon"])

        return "DONE!"

    # def calc_employees_accumulated_workload(self):

    # def set_kids_closed_circles(self):

    # def assign_shifts(self):


# ///////////////// RUN GENERATOR /////////////////

@generator.route('/generator', methods=['POST'])
def run_generator():
    calendar_id = request.json['calendar_id']
    new_generator = CalendarGenerator(calendar_id)
    response = new_generator.run()
    return jsonify(response)
