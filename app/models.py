from app import db


compatible = db.Table('compatible',
                      db.Column('kid_id', db.Integer, db.ForeignKey('kid.id'), primary_key=True),
                      db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True)
                      )

incompatible = db.Table('incompatible',
                        db.Column('kid_id', db.Integer, db.ForeignKey('kid.id'), primary_key=True),
                        db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True)
                        )


# Agenda Model
class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    workday = db.Column(db.String(100), nullable=False)  # part-time / full-time
    rotation_interval = db.Column(db.String(100), nullable=False)  # daily rotations / weekly rotations
    total_rotations = db.Column(db.Integer, nullable=False)
    kids_infos = db.relationship('KidInfo', backref='agenda', lazy=True)
    employees_infos = db.relationship('EmployeeInfo', backref='agenda', lazy=True)
    # active_roles = db.relationship('EmployeeInfo', backref='agenda', lazy=True)
    shifts = db.relationship('Shift', backref='agenda', lazy=True)

    def __init__(self, title, workday, rotation_interval, total_rotations, kid_infos, employees_infos, shifts):
        self.title = title
        self.workday = workday
        self.rotation_interval = rotation_interval
        self.total_rotations = total_rotations
        self.kid_infos = kid_infos
        self.employees_infos = employees_infos
        self.shifts = shifts


# Shift Model
class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agenda_id = db.Column(db.Integer, db.ForeignKey('agenda.id'))
    rotation = db.Column(db.Integer, nullable=False)
    # weekday = db.Column(db.String(100))
    shift = db.Column(db.String(100), nullable=False)  # morning / afternoon
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    kid_id = db.Column(db.Integer, db.ForeignKey('kid.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, agenda_id, rotation, shift, employee_id, kid_id, role_id):
        self.agenda_id = agenda_id
        self.rotation = rotation
        self.shift = shift
        self.employee_id = employee_id
        self.kid_id = kid_id
        self.role_id = role_id


# Role Model
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    employees_needed = db.Column(db.Integer, nullable=False)
    employee_proportion = db.Column(db.String(100), nullable=False)  # total / per group
    shifts = db.relationship('Shift', backref='role', lazy=True)

    def __init__(self, title, description, employees_needed, employee_proportion, shifts):
        self.title = title
        self.description = description
        self.employees_needed = employees_needed
        self.employee_proportion = employee_proportion
        self.shifts = shifts


# Group Model
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    color = db.Column(db.String(200), nullable=False)
    kids = db.relationship('Kid', backref='group', lazy=True)

    def __init__(self, title, color, kids):
        self.title = title
        self.color = color
        self.kids = kids


# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    compatible_kids = db.relationship("Kid", secondary=compatible, back_populates="compatible_employees")
    incompatible_kids = db.relationship("Kid", secondary=incompatible, back_populates="incompatible_employees")
    employee_infos = db.relationship('EmployeeInfo', backref='employee', lazy=True)
    shifts = db.relationship('Shift', backref='employee', lazy=True)

    def __init__(self, name, compatible_kids, incompatible_kids, employee_infos, shifts):
        self.name = name
        self.compatible_kids = compatible_kids
        self.incompatible_kids = incompatible_kids
        self.employee_infos = employee_infos
        self.shifts = shifts


# EmployeeInfo Model
class EmployeeInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    comments = db.Column(db.String(1000))
    attendance = db.Column(db.JSON)
    agenda_id = db.Column(db.Integer, db.ForeignKey('agenda.id'))

    def __init__(self, employee_id, comments, attendance, agenda_id):
        self.employee_id = employee_id
        self.comments = comments
        self.attendance = attendance
        self.agenda_id = agenda_id


# Kid Model
class Kid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    compatible_employees = db.relationship("Employee", secondary=compatible, back_populates="compatible_kids")
    incompatible_employees = db.relationship("Employee", secondary=incompatible, back_populates="incompatible_kids")
    kid_infos = db.relationship('KidInfo', backref='kid', lazy=True)
    shifts = db.relationship('Shift', backref='kid', lazy=True)

    def __init__(self, name, grade, group_id, compatible_employees, incompatible_employees, kid_infos, shifts):
        self.name = name
        self.grade = grade
        self.group_id = group_id
        self.compatible_employees = compatible_employees
        self.incompatible_employees = incompatible_employees
        self.kid_infos = kid_infos
        self.shifts = shifts


# KidInfo Model
class KidInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kid_id = db.Column(db.Integer, db.ForeignKey('kid.id'))
    important = db.Column(db.String(100))
    arrival_time = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.String(100), nullable=False)
    medication_time = db.Column(db.String(100))
    transport = db.Column(db.String(100), nullable=False)
    wheelchair = db.Column(db.Boolean, nullable=False)
    difficulty = db.Column(db.String(100), nullable=False)
    employees_needed = db.Column(db.Integer, nullable=False)
    other_info = db.Column(db.String(1000))
    attendance = db.Column(db.JSON)
    agenda_id = db.Column(db.Integer, db.ForeignKey('agenda.id'))

    def __init__(self, kid_id, important, arrival_time, departure_time, medication_time, transport, wheelchair,
                 difficulty, employees_needed, other_info, attendance, agenda_id):
        self.kid_id = kid_id
        self.important = important
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.medication_time = medication_time
        self.transport = transport
        self.wheelchair = wheelchair
        self.difficulty = difficulty
        self.employees_needed = employees_needed
        self.other_info = other_info
        self.attendance = attendance
        self.agenda_id = agenda_id
