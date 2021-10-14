from app import db

# Employee / Kid
employee_kid_compatible = db.Table('employee_kid_compatible',
                                   db.Column('kid_id', db.Integer, db.ForeignKey('kid.id')),
                                   db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'))
                                   )

employee_kid_incompatible = db.Table('employee_kid_incompatible',
                                     db.Column('kid_id', db.Integer, db.ForeignKey('kid.id')),
                                     db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'))
                                     )
# Employee / Employee
employee_employee_compatible = db.Table('employee_employee_compatible',
                                        db.Column('compatible_id', db.Integer, db.ForeignKey('employee.id')),
                                        db.Column('self_id', db.Integer, db.ForeignKey('employee.id'))
                                        )
employee_employee_incompatible = db.Table('employee_employee_incompatible',
                                          db.Column('incompatible_id', db.Integer, db.ForeignKey('employee.id')),
                                          db.Column('self_id', db.Integer, db.ForeignKey('employee.id'))
                                          )
# Kid / Kid
kid_kid_compatible = db.Table('kid_kid_compatible',
                              db.Column('compatible_id', db.Integer, db.ForeignKey('kid.id')),
                              db.Column('self_id', db.Integer, db.ForeignKey('kid.id'))
                              )
kid_kid_incompatible = db.Table('kid_kid_incompatible',
                                db.Column('incompatible_id', db.Integer, db.ForeignKey('kid.id')),
                                db.Column('self_id', db.Integer, db.ForeignKey('kid.id'))
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
    weekday = db.Column(db.Integer)  # when relational agenda.rotation_interval is "weekly rotations" a number from
    #                                  1 to 5 will be the weekday / 0 for "daily rotations"
    shift = db.Column(db.String(100), nullable=False)  # morning / afternoon
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    kid_id = db.Column(db.Integer, db.ForeignKey('kid.id'))

    def __init__(self, agenda_id, rotation, weekday, shift, employee_id, kid_id):
        self.agenda_id = agenda_id
        self.rotation = rotation
        self.weekday = weekday
        self.shift = shift
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
    incompatible_kids = db.relationship("Kid",
                                        secondary=employee_kid_incompatible,
                                        back_populates="incompatible_employees")
    compatible_employees = db.relationship('Employee',
                                           secondary=employee_employee_compatible,
                                           primaryjoin=(employee_employee_compatible.c.compatible_id == id),
                                           secondaryjoin=(employee_employee_compatible.c.self_id == id),
                                           back_populates="compatible_employees",
                                           lazy='dynamic')
    incompatible_employees = db.relationship('Employee',
                                             secondary=employee_employee_incompatible,
                                             primaryjoin=(employee_employee_incompatible.c.incompatible_id == id),
                                             secondaryjoin=(employee_employee_incompatible.c.self_id == id),
                                             back_populates="incompatible_employees",
                                             lazy='dynamic')

    employee_infos = db.relationship('EmployeeInfo', backref='employee', lazy=True)
    shifts = db.relationship('Shift', backref='employee', lazy=True)

    def __init__(self, name, compatible_kids, incompatible_kids, compatible_employees, incompatible_employees,
                 employee_infos, shifts):
        self.name = name
        self.compatible_kids = compatible_kids
        self.incompatible_kids = incompatible_kids
        self.compatible_employees = compatible_employees
        self.incompatible_employees = incompatible_employees
        self.employee_infos = employee_infos
        self.shifts = shifts


# EmployeeInfo Model
class EmployeeInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    attendance = db.Column(db.JSON)
    agenda_id = db.Column(db.Integer, db.ForeignKey('agenda.id'))

    def __init__(self, employee_id, attendance, agenda_id):
        self.employee_id = employee_id
        self.attendance = attendance
        self.agenda_id = agenda_id


# Kid Model
class Kid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    compatible_employees = db.relationship("Employee",
                                           secondary=employee_kid_compatible,
                                           back_populates="compatible_kids")
    incompatible_employees = db.relationship("Employee",
                                             secondary=employee_kid_incompatible,
                                             back_populates="incompatible_kids")
    compatible_kids = db.relationship('Kid',
                                      secondary=kid_kid_compatible,
                                      primaryjoin=(kid_kid_compatible.c.compatible_id == id),
                                      secondaryjoin=(kid_kid_compatible.c.self_id == id),
                                      back_populates="compatible_kids",
                                      lazy='dynamic')
    incompatible_kids = db.relationship('Kid',
                                        secondary=kid_kid_incompatible,
                                        primaryjoin=(kid_kid_incompatible.c.incompatible_id == id),
                                        secondaryjoin=(kid_kid_incompatible.c.self_id == id),
                                        back_populates="incompatible_kids",
                                        lazy='dynamic')

    kid_infos = db.relationship('KidInfo', backref='kid', lazy=True)
    shifts = db.relationship('Shift', backref='kid', lazy=True)

    def __init__(self, name, grade, group_id, compatible_employees, incompatible_employees, compatible_kids,
                 incompatible_kids, kid_infos, shifts):
        self.name = name
        self.grade = grade
        self.group_id = group_id
        self.compatible_employees = compatible_employees
        self.incompatible_employees = incompatible_employees
        self.compatible_kids = compatible_kids
        self.incompatible_kids = incompatible_kids
        self.kid_infos = kid_infos
        self.shifts = shifts


# KidInfo Model
class KidInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kid_id = db.Column(db.Integer, db.ForeignKey('kid.id'))
    difficulty = db.Column(db.String(100), nullable=False)
    employees_needed = db.Column(db.Integer, nullable=False)
    attendance = db.Column(db.JSON)
    agenda_id = db.Column(db.Integer, db.ForeignKey('agenda.id'))

    def __init__(self, kid_id, difficulty, employees_needed, attendance, agenda_id):
        self.kid_id = kid_id
        self.difficulty = difficulty
        self.employees_needed = employees_needed
        self.attendance = attendance
        self.agenda_id = agenda_id
