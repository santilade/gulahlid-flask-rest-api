from flask import Blueprint, request, jsonify
from app import db, API_BASE_URL
from app.models import Agenda
from app.schemas import agenda_schema, agendas_schema
import requests

agenda_controller = Blueprint('agenda_controller', __name__)


# ///////////////// AGENDA /////////////////
# Add Agenda
@agenda_controller.route('/agenda', methods=['POST'])
def add_agenda():
    title = request.json['title']
    workday = request.json['workday']
    rotation_interval = request.json['rotation_interval']
    total_rotations = request.json['total_rotations']
    kids_infos = []
    employees_infos = []
    shifts = []

    new_agenda = Agenda(title, workday, rotation_interval, total_rotations, kids_infos, employees_infos, shifts)

    db.session.add(new_agenda)
    db.session.commit()

    return agenda_schema.dump(new_agenda)


# Get All Agendas
@agenda_controller.route('/agenda', methods=['GET'])
def get_agendas():
    all_agendas = Agenda.query.all()
    result = agendas_schema.dump(all_agendas)
    return jsonify(result)


# Get Single Agenda
@agenda_controller.route('/agenda/<id>', methods=['GET'])
def get_agenda(id):
    agenda = Agenda.query.get(id)
    return agenda_schema.dump(agenda)


# Update Agenda
@agenda_controller.route('/agenda/<id>', methods=['PUT'])
def update_agenda(id):
    agenda = Agenda.query.get(id)

    title = request.json['title']
    if title != "":
        agenda.title = title

    employees_infos = request.json['employees_infos']
    if employees_infos:
        for employee_info in employees_infos:
            response = requests.post(API_BASE_URL + '/employee_info', json=employee_info)
            print(response.text)

    kids_infos = request.json['kids_infos']
    if kids_infos:
        for kid_info in kids_infos:
            response = requests.post(API_BASE_URL + '/kid_info', json=kid_info)
            print(response.text)

    db.session.commit()

    return agenda_schema.dump(agenda)


# Delete Agenda
@agenda_controller.route('/agenda/<id>', methods=['DELETE'])
def delete_agenda(id):
    agenda = Agenda.query.get(id)
    kids_infos = agenda.kids_infos
    employees_infos = agenda.employees_infos
    shifts = agenda.shifts

    for kid_info in kids_infos:
        db.session.delete(kid_info)

    for employee_info in employees_infos:
        db.session.delete(employee_info)

    for shift in shifts:
        db.session.delete(shift)

    db.session.delete(agenda)
    db.session.commit()

    return agenda_schema.dump(agenda)

