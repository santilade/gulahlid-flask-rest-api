from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import Calendar, Shift, Group, Employee, EmployeeInfo, Kid, KidInfo


# Calendar Schema
class CalendarSchema(SQLAlchemySchema):
    class Meta:
        model = Calendar
        load_instance = True

    id = auto_field()
    title = auto_field()
    workday = auto_field()
    rotation_interval = auto_field()
    total_rotations = auto_field()
    kids_infos = auto_field()
    employees_infos = auto_field()
    shifts = auto_field()


# Shift Schema
class ShiftSchema(SQLAlchemySchema):
    class Meta:
        model = Shift
        load_instance = True

    id = auto_field()
    calendar_id = auto_field()
    week = auto_field()
    day = auto_field()
    time = auto_field()
    priority = auto_field()
    employee_id = auto_field()
    kid_id = auto_field()


# Group Schema
class GroupSchema(SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True

    id = auto_field()
    title = auto_field()
    color = auto_field()
    kids = auto_field()


# Employee Schema
class EmployeeSchema(SQLAlchemySchema):
    class Meta:
        model = Employee
        load_instance = True

    id = auto_field()
    name = auto_field()
    compatible_kids = auto_field()
    compatible_employees = auto_field()
    employee_infos = auto_field()
    shifts = auto_field()


# EmployeeInfo Schema
class EmployeeInfoSchema(SQLAlchemySchema):
    class Meta:
        model = EmployeeInfo
        load_instance = True

    id = auto_field()
    employee_id = auto_field()
    attendance = auto_field()
    calendar_id = auto_field()


# Kid Schema
class KidSchema(SQLAlchemySchema):
    class Meta:
        model = Kid
        load_instance = True

    id = auto_field()
    name = auto_field()
    grade = auto_field()
    group_id = auto_field()
    difficulty = auto_field()
    closed_circle = auto_field()
    employees_needed = auto_field()
    compatible_employees = auto_field()
    compatible_kids = auto_field()
    kid_infos = auto_field()
    shifts = auto_field()


# KidInfo Schema
class KidInfoSchema(SQLAlchemySchema):
    class Meta:
        model = KidInfo
        load_instance = True

    id = auto_field()
    kid_id = auto_field()
    attendance = auto_field()
    employee_circle = auto_field()
    calendar_id = auto_field()


# Init schemas
calendar_schema = CalendarSchema()
calendars_schema = CalendarSchema(many=True)

shift_schema = ShiftSchema()
shifts_schema = ShiftSchema(many=True)

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

employee_info_schema = EmployeeInfoSchema()
employees_infos_schema = EmployeeInfoSchema(many=True)

kid_schema = KidSchema()
kids_schema = KidSchema(many=True)

kid_info_schema = KidInfoSchema()
kids_infos_schema = KidInfoSchema(many=True)
