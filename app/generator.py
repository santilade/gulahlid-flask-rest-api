from flask import Blueprint, request, jsonify
import itertools
from app import db
from .models import Calendar, Shift, Group, Employee, EmployeeInfo, Kid, KidInfo
from .schemas import calendar_schema, calendars_schema, shift_schema, shifts_schema, group_schema, groups_schema, \
    employee_schema, employees_schema, employee_info_schema, employees_infos_schema, kid_schema, kids_schema, \
    kid_info_schema, kids_infos_schema

# Defining as a blueprint allows to store routes in different documents or "blueprints"
generator = Blueprint('generator', __name__)


# ///////////////// GENERATOR /////////////////


class Generator:
    def __init__(self, calendar_id):
        self.calendar = Calendar.query.get(calendar_id)
        self.employees_infos = []  # [EmployeeInfo, EmployeeInfo, EmployeeInfo, ...]
        self.kids_infos = []  # [KidInfo, KidInfo, KidInfo, ...]
        self.unassigned_shifts = {}  # {day 1: [Shift, Shift, Shift, ...]}
        self.assigned_shifts = {}  # {day 1: [Shift, Shift, Shift, ...]}
        self.serialized_unassigned_shifts = {}
        self.free_employees = {}  # {"week 1": {"Monday": [Employee, Employee, ...],"Tuesday": [], ...}, "week 2": ...}
        self.serialized_free_employees = {}
        self.suggested_employees = {}
        self.switcher = {
            "daily rotations": {
                "part-time": self.case1,
                "full-time": self.case2
            },
            "weekly rotations": {
                "part-time": self.case3,
                "full-time": self.case4
            }
        }

    def run(self):
        self.get_infos()
        self.switcher[self.calendar.rotation_interval][self.calendar.workday]()

        response = {
            "employees_infos": employees_infos_schema.dump(self.employees_infos),
            "kids_infos": kids_infos_schema.dump(self.kids_infos),
            "unassigned_shifts": self.serialized_unassigned_shifts,
            "free_employees": self.serialized_free_employees
        }
        return response

    def get_infos(self):
        filtered_employees_infos = EmployeeInfo.query.filter_by(calendar_id=self.calendar.id)
        filtered_kids_infos = KidInfo.query.filter_by(calendar_id=self.calendar.id)

        for kid_info in filtered_kids_infos:
            self.kids_infos.append(kid_info)

        for employee_info in filtered_employees_infos:
            self.employees_infos.append(employee_info)

    def case1(self):
        for rotation in range(1, self.calendar.total_rotations + 1):
            day = "day " + str(rotation)
            self.unassigned_shifts[day] = {"afternoon": {1: [], 2: [], 3: [], 4: [], 5: []}}
            self.serialized_unassigned_shifts[day] = {"afternoon": {1: [], 2: [], 3: [], 4: [], 5: []}}
            self.free_employees[day] = {"afternoon": []}
            self.serialized_free_employees[day] = {"afternoon": []}

            for kid_info in self.kids_infos:
                if kid_info.attendance[day]["afternoon"]:
                    self.add_unassigned_shift(kid_info.kid_id, "", day, "afternoon")

            for employee_info in self.employees_infos:
                if employee_info.attendance[day]["afternoon"]:
                    self.add_free_employee(employee_info.employee_id, "", day, "afternoon")

            self.assign_shifts(self.unassigned_shifts[day], rotation)

    def case2(self):
        for rotation in range(1, self.calendar.total_rotations + 1):
            day = "day " + str(rotation)
            self.unassigned_shifts[day] = {"morning": {1: [], 2: [], 3: [], 4: [], 5: []},
                                           "afternoon": {1: [], 2: [], 3: [], 4: [], 5: []}}
            self.serialized_unassigned_shifts[day] = {"morning": {1: [], 2: [], 3: [], 4: [], 5: []},
                                                      "afternoon": {1: [], 2: [], 3: [], 4: [], 5: []}}
            self.free_employees[day] = {"morning": [],
                                        "afternoon": []}
            self.serialized_free_employees[day] = {"morning": [],
                                                   "afternoon": []}

            for kid_info in self.kids_infos:
                if kid_info.attendance[day]["morning"]:
                    self.add_unassigned_shift(kid_info.kid_id, "", day, "morning")

                if kid_info.attendance[day]["afternoon"]:
                    self.add_unassigned_shift(kid_info.kid_id, "", day, "afternoon")

            for employee_info in self.employees_infos:
                if employee_info.attendance[day]["morning"]:
                    self.add_free_employee(employee_info.employee_id, "", day, "morning")
                if employee_info.attendance[day]["afternoon"]:
                    self.add_free_employee(employee_info.employee_id, "", day, "afternoon")

            self.assign_shifts(self.unassigned_shifts[day], rotation)

    def case3(self):
        for rotation in range(1, self.calendar.total_rotations + 1):
            week = "week " + str(rotation)
            self.unassigned_shifts[week] = {}
            self.serialized_unassigned_shifts[week] = {}
            self.free_employees[week] = {}
            self.serialized_free_employees[week] = {}
            for weekday in range(1, 6):
                day = "day " + str(weekday)
                self.unassigned_shifts[week][day] = {"afternoon": {1: [], 2: [], 3: [], 4: [], 5: []}}
                self.serialized_unassigned_shifts[week][day] = {"afternoon": {1: [], 2: [], 3: [], 4: [], 5: []}}
                self.free_employees[week][day] = {"afternoon": []}
                self.serialized_free_employees[week][day] = {"afternoon": []}

                for kid_info in self.kids_infos:
                    if kid_info.attendance[week][day]["afternoon"]:
                        self.add_unassigned_shift(kid_info.kid_id, week, day, "afternoon")

                for employee_info in self.employees_infos:
                    if employee_info.attendance[week][day]["afternoon"]:
                        self.add_free_employee(employee_info.employee_id, week, day, "afternoon")

                self.assign_shifts(self.unassigned_shifts[week][day], rotation)

    def case4(self):
        for rotation in range(1, self.calendar.total_rotations + 1):
            week = "week " + str(rotation)
            self.unassigned_shifts[week] = {}
            self.serialized_unassigned_shifts[week] = {}
            self.free_employees[week] = {}
            self.serialized_free_employees[week] = {}
            for weekday in range(1, 6):
                day = "day " + str(weekday)
                self.unassigned_shifts[week][day] = {"morning": {1: [], 2: [], 3: [], 4: [], 5: []},
                                                     "afternoon": {1: [], 2: [], 3: [], 4: [], 5: []}}
                self.serialized_unassigned_shifts[week][day] = {"morning": {1: [], 2: [], 3: [], 4: [], 5: []},
                                                                "afternoon": {1: [], 2: [], 3: [], 4: [], 5: []}}
                self.free_employees[week][day] = {"morning": [],
                                                  "afternoon": []}
                self.serialized_free_employees[week][day] = {"morning": [],
                                                             "afternoon": []}

                for kid_info in self.kids_infos:
                    if kid_info.attendance[week][day]["morning"]:
                        self.add_unassigned_shift(kid_info.kid_id, week, day, "morning")

                    if kid_info.attendance[week][day]["afternoon"]:
                        self.add_unassigned_shift(kid_info.kid_id, week, day, "afternoon")

                for employee_info in self.employees_infos:
                    if employee_info.attendance[week][day]["morning"]:
                        self.add_free_employee(employee_info.employee_id, week, day, "morning")
                    if employee_info.attendance[week][day]["afternoon"]:
                        self.add_free_employee(employee_info.employee_id, week, day, "afternoon")

                self.assign_shifts(self.unassigned_shifts[week][day], rotation)

    def add_unassigned_shift(self, kid_id, week, day, time):
        kid = Kid.query.get(kid_id)

        shift_priority = 1
        if not kid.closed_circle:
            shift_priority = shift_priority + 2
        if kid.difficulty != "challenging":
            shift_priority = shift_priority + 1
        if kid.employees_needed == 1:
            shift_priority = shift_priority + 1

        new_shift = Shift(self.calendar.id, week, day, time, shift_priority, 0, kid_id)
        db.session.add(new_shift)
        db.session.commit()

        if self.calendar.rotation_interval == 'daily rotations':
            self.unassigned_shifts[day][time][shift_priority].append(new_shift)
            self.serialized_unassigned_shifts[day][time][shift_priority].append(shift_schema.dump(new_shift))
        elif self.calendar.rotation_interval == 'weekly rotations':
            self.unassigned_shifts[week][day][time][shift_priority].append(new_shift)
            self.serialized_unassigned_shifts[week][day][time][shift_priority].append(shift_schema.dump(new_shift))

    def add_free_employee(self, employee_id, week, day, time):
        if self.calendar.rotation_interval == 'daily rotations':
            self.free_employees[day][time].append(employee_id)
            self.serialized_free_employees[day][time].append(employee_id)
        elif self.calendar.rotation_interval == 'weekly rotations':
            self.free_employees[week][day][time].append(employee_id)
            self.serialized_free_employees[week][day][time].append(employee_id)

    def assign_shifts(self, unassigned_shifts, rotation):
        for time in unassigned_shifts.keys():
            self.suggested_employees[time] = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
            free_employees = []
            for shift in unassigned_shifts[time][1]:
                self.suggested_employees[time][1] = {shift.id: []}
                # challenging / closed circle / 2 employees
                closed_circle_list = KidInfo.query.filter_by(calendar_id=self.calendar.id,
                                                             kid_id=shift.kid_id)[0].closed_circle_list
                if self.calendar.rotation_interval == "daily rotations":
                    free_employees = self.free_employees[shift.day][shift.time]
                elif self.calendar.rotation_interval == "weekly rotations":
                    free_employees = self.free_employees[shift.week][shift.day][shift.time]

                print("kid: " + str(shift.kid_id) + " rotation: " + str(rotation))
                print(closed_circle_list)
                print(free_employees)

                if rotation == 1:
                    for pair in closed_circle_list:
                        if all(x in free_employees for x in pair):
                            print(pair)

                            shift.employee_id = pair[0]
                            new_shift = Shift(self.calendar.id, shift.week, shift.day, shift.time, shift.priority,
                                              pair[1], shift.kid_id)
                            db.session.add(new_shift)
                            db.session.commit()

                            free_employees.remove(pair[0])
                            free_employees.remove(pair[1])
                            break

                elif rotation > 1:
                    repeated = {}
                    for i in range(1, rotation+1, 1):
                        repeated["rotation " + str(i)] = []
                        for pair in closed_circle_list:
                            if self.calendar.rotation_interval == "daily rotations":
                                repeated_shifts_employee_1 = Shift.query.filter_by(calendar_id=self.calendar.id,
                                                                                   day=i,
                                                                                   kid_id=shift.kid_id,
                                                                                   employee_id=pair[0]
                                                                                   )
                                repeated_shifts_employee_2 = Shift.query.filter_by(calendar_id=self.calendar.id,
                                                                                   day=i,
                                                                                   kid_id=shift.kid_id,
                                                                                   employee_id=pair[1]
                                                                                   )


            for shift in unassigned_shifts[time][2]:
                # challenging / closed circle / 1 employees
                return ""
            for shift in unassigned_shifts[time][3]:
                # challenging / 2 employees
                return ""
            for shift in unassigned_shifts[time][4]:
                # average or easy-going / 2 employees
                return ""
            for shift in unassigned_shifts[time][5]:
                # average or easy-going / 1 employees
                # list(itertools.product(unassigned_shifts["morning"][1], []))
                return ""


# ///////////////// RUN GENERATOR /////////////////

@generator.route('/generator', methods=['POST'])
def run_generator():
    calendar_id = request.json['calendar_id']
    new_generator = Generator(calendar_id)
    response = new_generator.run()
    return jsonify(response)
