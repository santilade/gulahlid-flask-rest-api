from flask import Blueprint, request, jsonify
from app import db
from app.models import Shift
from app.schemas import shift_schema, shifts_schema

shift_controller = Blueprint('shift_controller', __name__)


# ///////////////// SHIFT /////////////////
# Get All Shifts
@shift_controller.route('/shift', methods=['GET'])
def get_shifts():
    all_shifts = Shift.query.all()
    result = shifts_schema.dump(all_shifts)

    return jsonify(result)


# Get Single Shift
@shift_controller.route('/shift/<id>', methods=['GET'])
def get_shift(id):
    shift = Shift.query.get(id)

    return shift_schema.dump(shift)


# Update Shift
@shift_controller.route('/shift/<id>', methods=['PUT'])
def update_shift(id):
    shift = Shift.query.get(id)

    employee_id = request.json['employee_id']
    kid_id = request.json['kid_id']

    if employee_id:
        shift.employee_id = employee_id
    if kid_id:
        shift.kid_id = kid_id

    db.session.commit()

    return shift_schema.dump(shift)


# Delete Shift
@shift_controller.route('/shift/<id>', methods=['DELETE'])
def delete_shift(id):
    shift = Shift.query.get(id)

    db.session.delete(shift)
    db.session.commit()

    return shift_schema.dump(shift)


# Delete all Shifts
@shift_controller.route('/shift/all', methods=['DELETE'])
def delete_all_shifts():
    response = Shift.query.delete()
    db.session.commit()

    return jsonify("Deleted " + str(response) + " shifts")

