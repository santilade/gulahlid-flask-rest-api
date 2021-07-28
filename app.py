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

# Group Class/Model
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    color = db.Column(db.String(200))
    kids = db.relationship('Kid', backref='group', lazy=True)

    def __init__(self, title, color, kids):
        self.title = title
        self.color = color
        self.kids = kids


# Kid Class/Model
class Kid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    grade = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __init__(self, name, grade, group_id):
        self.name = name
        self.grade = grade
        self.group_id = group_id


# -------------------------------------------------

# Group Schema
class GroupSchema(SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True  # Optional: deserialize to model instances

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
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
kid_schema = KidSchema()
kids_schema = KidSchema(many=True)


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
