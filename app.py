from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# -------------------------------------------------

# Agenda Model
class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    workday = db.Column(db.String(100), nullable=False)  # part-time / full-time
    rotation_interval = db.Column(db.String(100), nullable=False)  # daily rotations / weekly rotations
    total_rotations = db.Column(db.Integer, nullable=False)
    kid_infos = db.relationship('KidInfo', backref='agenda', lazy=True)
    employees_infos = db.relationship('EmployeeInfo', backref='agenda', lazy=True)
    # shifts = db.relationship('Shift', backref='agenda', lazy=True)

    def __init__(self, title, workday, rotation_interval, total_rotations, kid_infos):
        self.title = title
        self.workday = workday
        self.rotation_interval = rotation_interval
        self.total_rotations = total_rotations
        self.kid_infos = kid_infos
        # self.shifts = shifts


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
    employee_infos = db.relationship('StaffInfo', backref='employee', lazy=True)

    def __init__(self, name, employee_infos):
        self.name = name
        self.employee_infos = employee_infos


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
    kid_infos = db.relationship('KidInfo', backref='kid', lazy=True)

    def __init__(self, name, grade, group_id, kid_infos):
        self.name = name
        self.grade = grade
        self.group_id = group_id
        self.kid_infos = kid_infos


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


# -------------------------------------------------

# Agenda Schema
class AgendaSchema(SQLAlchemySchema):
    class Meta:
        model = Agenda
        load_instance = True

    id = auto_field()
    title = auto_field()
    workday = auto_field()
    rotation_interval = auto_field()
    total_rotations = auto_field()
    kids_infos = auto_field()
    employees_infos = auto_field()
    # shifts = auto_field()


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
    employee_infos = auto_field()


# Employee Schema
class EmployeeInfoSchema(SQLAlchemySchema):
    class Meta:
        model = EmployeeInfo
        load_instance = True

    id = auto_field()
    employee_id = auto_field()
    comments = auto_field()
    attendance = auto_field()
    agenda_id = auto_field()


# Kid Schema
class KidSchema(SQLAlchemySchema):
    class Meta:
        model = Kid
        load_instance = True

    id = auto_field()
    name = auto_field()
    grade = auto_field()
    group_id = auto_field()
    kid_infos = auto_field()


# KidInfo Schema
class KidInfoSchema(SQLAlchemySchema):
    class Meta:
        model = KidInfo
        load_instance = True

    id = auto_field()
    kid_id = auto_field()
    important = auto_field()
    arrival_time = auto_field()
    departure_time = auto_field()
    medication_time = auto_field()
    transport = auto_field()
    wheelchair = auto_field()
    difficulty = auto_field()
    employees_needed = auto_field()
    other_info = auto_field()
    attendance = auto_field()
    agenda_id = auto_field()


# Init schemas
agenda_schema = AgendaSchema()
agendas_schema = AgendaSchema(many=True)

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

employee_info_schema = EmployeeSchema()
employees_infos_schema = EmployeeSchema(many=True)

kid_schema = KidSchema()
kids_schema = KidSchema(many=True)

kid_info_schema = KidInfoSchema()
kids_infos_schema = KidInfoSchema(many=True)


# -------------------------------------------------

# Create a Agenda
@app.route('/agenda', methods=['POST'])
def add_agenda():
    title = request.json['title']
    workday = request.json['workday']
    rotation_interval = request.json['rotation_interval']
    total_rotations = request.json['total_rotations']
    kids_infos = []
    employees_infos = []

    new_agenda = Agenda(title, workday, rotation_interval, total_rotations, kids_infos, employees_infos)

    db.session.add(new_agenda)
    db.session.commit()

    return agenda_schema.dump(new_agenda)


# Get All Agendas
@app.route('/agenda', methods=['GET'])
def get_agendas():
    all_agendas = Agenda.query.all()
    result = agendas_schema.dump(all_agendas)
    return jsonify(result)


# Get Single Agendas
@app.route('/agenda/<id>', methods=['GET'])
def get_agenda(id):
    agenda = Agenda.query.get(id)
    return agenda_schema.dump(agenda)


# Update a Agenda
@app.route('/agenda/<id>', methods=['PUT'])
def update_agenda(id):
    agenda = Agenda.query.get(id)

    title = request.json['title']
    workday = request.json['workday']
    rotation_interval = request.json['rotation_interval']
    total_rotations = request.json['total_rotations']

    agenda.title = title
    agenda.workday = workday
    agenda.rotation_interval = rotation_interval
    agenda.total_rotations = total_rotations

    db.session.commit()

    return group_schema.dump(agenda)


# Delete Agenda
@app.route('/agenda/<id>', methods=['DELETE'])
def delete_agenda(id):
    agenda = Agenda.query.get(id)
    kids_infos = agenda.kids_infos
    employees_infos = agenda.employees_infos

    for kid_info in kids_infos:
        db.session.delete(kid_info)

    for employee_info in employees_infos:
        db.session.delete(employee_info)

    # shifts = agenda.shifts
    #     #
    #     # for shift in shifts:
    #     #     db.session.delete(shift)

    db.session.delete(agenda)
    db.session.commit()

    return agenda_schema.dump(agenda)


# -------------------------------------------------


# Create a Group
@app.route('/group', methods=['POST'])
def add_group():
    title = request.json['title']
    color = request.json['color']
    kids = []

    new_group = Group(title, color, kids)

    db.session.add(new_group)
    db.session.commit()

    return group_schema.dump(new_group)


# Get All Groups
@app.route('/group', methods=['GET'])
def get_groups():
    all_groups = Group.query.all()
    result = groups_schema.dump(all_groups)
    return jsonify(result)


# Get Single Groups
@app.route('/group/<id>', methods=['GET'])
def get_group(id):
    group = Group.query.get(id)
    return group_schema.dump(group)


# Update a Group
@app.route('/group/<id>', methods=['PUT'])
def update_group(id):
    group = Group.query.get(id)

    title = request.json['title']
    color = request.json['color']

    group.title = title
    group.color = color

    db.session.commit()

    return group_schema.dump(group)


# Delete Group
@app.route('/group/<id>', methods=['DELETE'])
def delete_group(id):
    group = Group.query.get(id)
    kids = group.kids

    for kid in kids:
        db.session.delete(kid)

    db.session.delete(group)
    db.session.commit()

    return group_schema.dump(group)


# -------------------------------------------------


# Create a Employee
@app.route('/employee', methods=['POST'])
def add_employee():
    name = request.json['name']
    employee_infos = []

    new_employee = Employee(name, employee_infos)

    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.dump(new_employee)


# Get All Employees
@app.route('/employee', methods=['GET'])
def get_employees():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result)


# Get Single Employees
@app.route('/employee/<id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return employee_schema.dump(employee)


# Update a Employee
@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)

    name = request.json['name']

    employee.name = name

    db.session.commit()

    return employee_schema.dump(employee)


# Delete Employee
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    employee_infos = employee.employee_infos

    for employee_info in employee_infos:
        db.session.delete(employee_info)

    db.session.delete(employee)
    db.session.commit()

    return employee_schema.dump(employee)


# -------------------------------------------------


# Create Employee Info
@app.route('/employee_info', methods=['POST'])
def add_employee_info():
    employee_id = request.json['employee_id']
    comments = request.json['comments']
    attendance = request.json['attendance']
    agenda_id = request.json['agenda_id']

    new_employee_info = EmployeeInfo(employee_id, comments, attendance, agenda_id)

    db.session.add(new_employee_info)
    db.session.commit()

    return employee_info_schema.dump(new_employee_info)


# Get All Employees Infos
@app.route('/employee_info', methods=['GET'])
def get_employee_infos():
    all_employee_infos = EmployeeInfo.query.all()
    result = employees_infos_schema.dump(all_employee_infos)
    return jsonify(result)


# Get Single Employee Info
@app.route('/employee_info/<id>', methods=['GET'])
def get_employee_info(id):
    employee_info = EmployeeInfo.query.get(id)
    return employee_info_schema.dump(employee_info)


# Update Employee Info
@app.route('/employee_info/<id>', methods=['PUT'])
def update_employee_info(id):
    employee_info = EmployeeInfo.query.get(id)

    comments = request.json['comments']
    attendance = request.json['attendance']

    employee_info.grade = comments
    employee_info.group_id = attendance

    db.session.commit()

    return employee_info_schema.dump(employee_info)


# Delete Employee Info
@app.route('/employee_info/<id>', methods=['DELETE'])
def delete_employee_info(id):
    employee_info = EmployeeInfo.query.get(id)

    db.session.delete(employee_info)
    db.session.commit()

    return employee_info_schema.dump(employee_info)


# -------------------------------------------------


# Create Kid
@app.route('/kid', methods=['POST'])
def add_kid():
    name = request.json['name']
    grade = request.json['grade']
    group_id = request.json['group_id']
    kid_infos = []

    new_kid = Kid(name, grade, group_id, kid_infos)

    db.session.add(new_kid)
    db.session.commit()

    return kid_schema.dump(new_kid)


# Get All Kids
@app.route('/kid', methods=['GET'])
def get_kids():
    all_kids = Kid.query.all()
    result = kids_schema.dump(all_kids)
    return jsonify(result)


# Get Single Kid
@app.route('/kid/<id>', methods=['GET'])
def get_kid(id):
    kid = Kid.query.get(id)
    return kid_schema.dump(kid)


# Update Kid
@app.route('/kid/<id>', methods=['PUT'])
def update_kid(id):
    kid = Kid.query.get(id)

    name = request.json['name']
    grade = request.json['grade']
    group_id = request.json['group_id']

    kid.name = name
    kid.grade = grade
    kid.group_id = group_id

    db.session.commit()

    return kid_schema.dump(kid)


# Delete Kid
@app.route('/kid/<id>', methods=['DELETE'])
def delete_kid(id):
    kid = Kid.query.get(id)
    kid_infos = kid.kid_infos

    for kid_info in kid_infos:
        db.session.delete(kid_info)

    db.session.delete(kid)
    db.session.commit()

    return kid_schema.dump(kid)


# -------------------------------------------------


# Create Kid Info
@app.route('/kid_info', methods=['POST'])
def add_kid_info():
    kid_id = request.json['kid_id']
    important = request.json['important']
    arrival_time = request.json['arrival_time']
    departure_time = request.json['departure_time']
    medication_time = request.json['medication_time']
    transport = request.json['transport']
    wheelchair = request.json['wheelchair']
    difficulty = request.json['difficulty']
    employees_needed = request.json['employees_needed']
    other_info = request.json['other_info']
    attendance = request.json['attendance']
    agenda_id = request.json['agenda_id']

    new_kid_info = KidInfo(kid_id, important, arrival_time, departure_time, medication_time, transport, wheelchair,
                           difficulty, employees_needed, other_info, attendance, agenda_id)

    db.session.add(new_kid_info)
    db.session.commit()

    return kid_info_schema.dump(new_kid_info)


# Get All Kids Infos
@app.route('/kid_info', methods=['GET'])
def get_kids_info():
    all_kids_info = KidInfo.query.all()
    result = kids_infos_schema.dump(all_kids_info)
    return jsonify(result)


# Get Single Kid Info
@app.route('/kid_info/<id>', methods=['GET'])
def get_kid_info(id):
    kid_info = KidInfo.query.get(id)
    return kid_info_schema.dump(kid_info)


# Update Kid Info
@app.route('/kid_info/<id>', methods=['PUT'])
def update_kid_info(id):
    kid_info = KidInfo.query.get(id)

    important = request.json['important']
    arrival_time = request.json['arrival_time']
    departure_time = request.json['departure_time']
    medication_time = request.json['medication_time']
    transport = request.json['transport']
    wheelchair = request.json['wheelchair']
    difficulty = request.json['difficulty']
    employees_needed = request.json['employees_needed']
    other_info = request.json['other_info']
    attendance = request.json['attendance']

    kid_info.important = important
    kid_info.arrival_time = arrival_time
    kid_info.departure_time = departure_time
    kid_info.medication_time = medication_time
    kid_info.transport = transport
    kid_info.wheelchair = wheelchair
    kid_info.difficulty = difficulty
    kid_info.employees_needed = employees_needed
    kid_info.other_info = other_info
    kid_info.attendance = attendance

    db.session.commit()

    return kid_info_schema.dump(kid_info)


# Delete Kid Info
@app.route('/kid_info/<id>', methods=['DELETE'])
def delete_kid_info(id):
    kid_info = KidInfo.query.get(id)

    db.session.delete(kid_info)
    db.session.commit()

    return kid_info_schema.dump(kid_info)


# -------------------------------------------------


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
