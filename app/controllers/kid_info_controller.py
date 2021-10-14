from flask import Blueprint, request, jsonify
from app import db
from app.models import KidInfo
from app.schemas import kid_info_schema, kids_infos_schema

kid_info_controller = Blueprint('kid_info_controller', __name__)


# ///////////////// KID INFO /////////////////
# Add KidInfo
@kid_info_controller.route('/kid_info', methods=['POST'])
def add_kid_info():
    kid_id = request.json['kid_id']
    difficulty = request.json['difficulty']
    employees_needed = request.json['employees_needed']
    attendance = request.json['attendance']
    agenda_id = request.json['agenda_id']

    new_kid_info = KidInfo(kid_id, difficulty, employees_needed, attendance, agenda_id)

    db.session.add(new_kid_info)
    db.session.commit()

    return kid_info_schema.dump(new_kid_info)


# Get All Kids Infos
@kid_info_controller.route('/kid_info', methods=['GET'])
def get_kids_info():
    all_kids_info = KidInfo.query.all()
    result = kids_infos_schema.dump(all_kids_info)

    return jsonify(result)


# Get Single Kid Info
@kid_info_controller.route('/kid_info/<id>', methods=['GET'])
def get_kid_info(id):
    kid_info = KidInfo.query.get(id)

    return kid_info_schema.dump(kid_info)


# Update Kid Info
@kid_info_controller.route('/kid_info/<id>', methods=['PUT'])
def update_kid_info(id):
    kid_info = KidInfo.query.get(id)

    difficulty = request.json['difficulty']
    employees_needed = request.json['employees_needed']
    attendance = request.json['attendance']

    if difficulty:
        kid_info.difficulty = difficulty
    if employees_needed:
        kid_info.employees_needed = employees_needed
    if attendance:
        kid_info.attendance = attendance

    db.session.commit()

    return kid_info_schema.dump(kid_info)


# Delete Kid Info
@kid_info_controller.route('/kid_info/<id>', methods=['DELETE'])
def delete_kid_info(id):
    kid_info = KidInfo.query.get(id)

    db.session.delete(kid_info)
    db.session.commit()

    return kid_info_schema.dump(kid_info)