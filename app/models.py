from app import db

# Employee / Kid
employee_kid_compatible = db.Table('employee_kid_compatible',
                                   db.Column('kid_id', db.Integer, db.ForeignKey('kid.id')),
                                   db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'))
                                   )
# Employee / Employee
employee_employee_compatible = db.Table('employee_employee_compatible',
                                        db.Column('compatible_id', db.Integer, db.ForeignKey('employee.id')),
                                        db.Column('self_id', db.Integer, db.ForeignKey('employee.id'))
                                        )
# Kid / Kid
kid_kid_compatible = db.Table('kid_kid_compatible',
                              db.Column('compatible_id', db.Integer, db.ForeignKey('kid.id')),
                              db.Column('self_id', db.Integer, db.ForeignKey('kid.id'))
                              )


# Calendar Model
class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    workday = db.Column(db.String(100), nullable=False)  # part-time / full-time
    rotation_interval = db.Column(db.String(100), nullable=False)  # daily rotations / weekly rotations
    total_rotations = db.Column(db.Integer, nullable=False)
    kids_infos = db.relationship('KidInfo', backref='calendar', lazy=True)
    employees_infos = db.relationship('EmployeeInfo', backref='calendar', lazy=True)
    shifts = db.relationship('Shift', backref='calendar', lazy=True)

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
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'))
    week = db.Column(db.String(100))
    day = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)  # morning / afternoon
    priority = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    kid_id = db.Column(db.Integer, db.ForeignKey('kid.id'))

    def __init__(self, calendar_id, week, day, time, priority, employee_id, kid_id):
        self.calendar_id = calendar_id
        self.week = week
        self.day = day
        self.time = time
        self.priority = priority
        self.employee_id = employee_id
        self.kid_id = kid_id


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

    compatible_kids = db.relationship("Kid",
                                      secondary=employee_kid_compatible,
                                      back_populates="compatible_employees")
    compatible_employees = db.relationship('Employee',
                                           secondary=employee_employee_compatible,
                                           primaryjoin=(employee_employee_compatible.c.compatible_id == id),
                                           secondaryjoin=(employee_employee_compatible.c.self_id == id),
                                           back_populates="compatible_employees",
                                           lazy='dynamic')

    employee_infos = db.relationship('EmployeeInfo', backref='employee', lazy=True)
    shifts = db.relationship('Shift', backref='employee', lazy=True)

    def __init__(self, name, compatible_kids, compatible_employees, employee_infos, shifts):
        self.name = name
        self.compatible_kids = compatible_kids
        self.compatible_employees = compatible_employees
        self.employee_infos = employee_infos
        self.shifts = shifts


# EmployeeInfo Model
class EmployeeInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    attendance = db.Column(db.JSON)
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'))

    def __init__(self, employee_id, attendance, calendar_id):
        self.employee_id = employee_id
        self.attendance = attendance
        self.calendar_id = calendar_id


# Kid Model
class Kid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    difficulty = db.Column(db.String(100), nullable=False)  # challenging / average / easy-going
    employees_needed = db.Column(db.Integer, nullable=False)
    closed_circle = db.Column(db.Boolean, nullable=False)

    compatible_employees = db.relationship("Employee",
                                           secondary=employee_kid_compatible,
                                           back_populates="compatible_kids")
    compatible_kids = db.relationship('Kid',
                                      secondary=kid_kid_compatible,
                                      primaryjoin=(kid_kid_compatible.c.compatible_id == id),
                                      secondaryjoin=(kid_kid_compatible.c.self_id == id),
                                      back_populates="compatible_kids",
                                      lazy='dynamic')

    kid_infos = db.relationship('KidInfo', backref='kid', lazy=True)
    shifts = db.relationship('Shift', backref='kid', lazy=True)

    def __init__(self, name, grade, group_id, difficulty, closed_circle, employees_needed, compatible_employees,
                 compatible_kids, kid_infos, shifts):
        self.name = name
        self.grade = grade
        self.group_id = group_id
        self.difficulty = difficulty
        self.closed_circle = closed_circle
        self.employees_needed = employees_needed
        self.compatible_employees = compatible_employees
        self.compatible_kids = compatible_kids
        self.kid_infos = kid_infos
        self.shifts = shifts


# KidInfo Model
class KidInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kid_id = db.Column(db.Integer, db.ForeignKey('kid.id'))
    attendance = db.Column(db.JSON)
    closed_circle_list = db.Column(db.JSON)
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'))

    def __init__(self, kid_id, attendance, closed_circle_list, calendar_id):
        self.kid_id = kid_id
        self.attendance = attendance
        self.closed_circle_list = closed_circle_list
        self.calendar_id = calendar_id
