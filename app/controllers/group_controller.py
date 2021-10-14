from flask import Blueprint, request, jsonify
from app import db
from app.models import Group
from app.schemas import group_schema, groups_schema

group_controller = Blueprint('group_controller', __name__)


# ///////////////// GROUP /////////////////
# Add Group
@group_controller.route('/group', methods=['POST'])
def add_group():
    title = request.json['title']
    color = request.json['color']
    kids = []

    new_group = Group(title, color, kids)

    db.session.add(new_group)
    db.session.commit()

    return group_schema.dump(new_group)


# Get All Groups
@group_controller.route('/group', methods=['GET'])
def get_groups():
    all_groups = Group.query.all()
    result = groups_schema.dump(all_groups)
    return jsonify(result)


# Get Single Group
@group_controller.route('/group/<id>', methods=['GET'])
def get_group(id):
    group = Group.query.get(id)
    return group_schema.dump(group)


# Update Group
@group_controller.route('/group/<id>', methods=['PUT'])
def update_group(id):
    group = Group.query.get(id)

    title = request.json['title']
    color = request.json['color']

    if title:
        group.title = title
    if color:
        group.color = color

    db.session.commit()

    return group_schema.dump(group)


# Delete Group
@group_controller.route('/group/<id>', methods=['DELETE'])
def delete_group(id):
    group = Group.query.get(id)
    kids = group.kids

    for kid in kids:
        db.session.delete(kid)

    db.session.delete(group)
    db.session.commit()

    return group_schema.dump(group)

