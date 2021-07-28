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
    # shifts = db.relationship('Shift', backref='agenda', lazy=True)

    def __init__(self, title, workday, rotation_interval, total_rotations):
        self.title = title
        self.workday = workday
        self.rotation_interval = rotation_interval
        self.total_rotations = total_rotations
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


# Kid Model
class Kid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __init__(self, name, grade, group_id):
        self.name = name
        self.grade = grade
        self.group_id = group_id


# KidInfo Model
# class KidInfo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     kid_id = db.Column(db.Integer, db.ForeignKey('kid.id'))
#     important = db.Column(db.String(100))
#     arrival_time = db.Column(db.String(100), nullable=False)
#     departure_time = db.Column(db.String(100), nullable=False)
#     medication_time = db.Column(db.String(100))
#     transport = db.Column(db.String(100), nullable=False)
#     wheelchair = db.Column(db.Boolean, nullable=False)
#     difficulty = db.Column(db.String(100), nullable=False)
#     staff_needed = db.Column(db.Integer, nullable=False)
#     other_info = db.Column(db.String(1000))
#     attendance = db.Column(db.String(100), nullable=False)
#     agenda_id = db.Column(db.Integer, db.ForeignKey('agenda.id'))
#
#     def __init__(self, kid_id, important, arrival_time, departure_time, medication_time, transport, wheelchair,
#                  difficulty, staff_needed, other_info, attendance, agenda_id):
#         self.kid_id = kid_id
#         self.important = important
#         self.arrival_time = arrival_time
#         self.departure_time = departure_time
#         self.medication_time = medication_time
#         self.transport = transport
#         self.wheelchair = wheelchair
#         self.difficulty = difficulty
#         self.staff_needed = staff_needed
#         self.other_info = other_info
#         self.attendance = attendance
#         self.agenda_id = agenda_id


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


# Group Schema
class GroupSchema(SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True

    id = auto_field()
    title = auto_field()
    color = auto_field()
    kids = auto_field()


# Kid Schema
class KidSchema(SQLAlchemySchema):
    class Meta:
        model = Kid
        load_instance = True

    id = auto_field()
    name = auto_field()
    grade = auto_field()
    group_id = auto_field()


# Init schemas
agenda_schema = AgendaSchema()
agendas_schema = AgendaSchema(many=True)

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)

kid_schema = KidSchema()
kids_schema = KidSchema(many=True)


# -------------------------------------------------

# Create a Agenda
@app.route('/agenda', methods=['POST'])
def add_agenda():
    title = request.json['title']
    workday = request.json['workday']
    rotation_interval = ['rotation_interval']
    total_rotations = ['total_rotations']

    new_agenda = Agenda(title, workday, rotation_interval, total_rotations)

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
    # shifts = agenda.shifts
    #
    # for shift in shifts:
    #     db.session.delete(shift)

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


# Create a Kid
@app.route('/kid', methods=['POST'])
def add_kid():
    name = request.json['name']
    grade = request.json['grade']
    group_id = request.json['group_id']

    new_kid = Kid(name, grade, group_id)

    db.session.add(new_kid)
    db.session.commit()

    return kid_schema.dump(new_kid)


# Get All Kids
@app.route('/kid', methods=['GET'])
def get_kids():
    all_kids = Kid.query.all()
    result = kids_schema.dump(all_kids)
    return jsonify(result)


# Get Single Kids
@app.route('/kid/<id>', methods=['GET'])
def get_kid(id):
    kid = Kid.query.get(id)
    return kid_schema.dump(kid)


# Update a Kid
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
    db.session.delete(kid)
    db.session.commit()

    return kid_schema.dump(kid)


# -------------------------------------------------


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
