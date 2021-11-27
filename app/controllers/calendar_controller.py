from flask import Blueprint, request, jsonify
from app import db, API_BASE_URL
from app.models import Calendar
from app.schemas import calendar_schema, calendars_schema
import requests

calendar_controller = Blueprint('calendar_controller', __name__)


# ///////////////// CALENDAR /////////////////
# Add Calendar
@calendar_controller.route('/calendar', methods=['POST'])
def add_calendar():
    title = request.json['title']
    workday = request.json['workday']
    rotation_interval = request.json['rotation_interval']
    total_rotations = request.json['total_rotations']
    kids_infos = []
    employees_infos = []
    shifts = []

    new_calendar = Calendar(title, workday, rotation_interval, total_rotations, kids_infos, employees_infos, shifts)

    db.session.add(new_calendar)
    db.session.commit()

    return calendar_schema.dump(new_calendar)


# Get All Calendars
@calendar_controller.route('/calendar', methods=['GET'])
def get_calendars():
    all_calendars = Calendar.query.all()
    result = calendars_schema.dump(all_calendars)

    return jsonify(result)


# Get Single Calendar
@calendar_controller.route('/calendar/<id>', methods=['GET'])
def get_calendar(id):
    calendar = Calendar.query.get(id)

    return calendar_schema.dump(calendar)


# Update Calendar
@calendar_controller.route('/calendar/<id>', methods=['PUT'])
def update_calendar(id):
    calendar = Calendar.query.get(id)

    title = request.json['title']
    employees_infos = request.json['employees_infos']
    kids_infos = request.json['kids_infos']

    if title != "":
        calendar.title = title

    if employees_infos:
        for employee_info in employees_infos:
            response = requests.post(API_BASE_URL + '/employee_info', json=employee_info)
            print(response.text)

    if kids_infos:
        for kid_info in kids_infos:
            response = requests.post(API_BASE_URL + '/kid_info', json=kid_info)
            print(response.text)

    db.session.commit()

    return calendar_schema.dump(calendar)


# Delete Calendar
@calendar_controller.route('/calendar/<id>', methods=['DELETE'])
def delete_calendar(id):
    calendar = Calendar.query.get(id)
    kids_infos = calendar.kids_infos
    employees_infos = calendar.employees_infos
    shifts = calendar.shifts

    for kid_info in kids_infos:
        db.session.delete(kid_info)

    for employee_info in employees_infos:
        db.session.delete(employee_info)

    for shift in shifts:
        db.session.delete(shift)

    db.session.delete(calendar)
    db.session.commit()

    return calendar_schema.dump(calendar)

