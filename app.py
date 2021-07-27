from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
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


# Group Class/Model
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    color = db.Column(db.String(200))

    def __init__(self, title, color):
        self.title = title
        self.color = color


# Group Schema
class GroupSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'color')


# Init schema
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)


# Create a Group
@app.route('/group', methods=['POST'])
def add_group():
    title = request.json['title']
    color = request.json['color']

    new_group = Group(title, color)

    db.session.add(new_group)
    db.session.commit()

    return group_schema.jsonify(new_group)


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
    return group_schema.jsonify(group)


# Update a Group
@app.route('/group/<id>', methods=['PUT'])
def update_group(id):
    group = Group.query.get(id)

    title = request.json['title']
    color = request.json['color']

    group.title = title
    group.color = color

    db.session.commit()

    return group_schema.jsonify(group)


# Delete Group
@app.route('/group/<id>', methods=['DELETE'])
def delete_group(id):
    group = Group.query.get(id)
    db.session.delete(group)
    db.session.commit()

    return group_schema.jsonify(group)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
