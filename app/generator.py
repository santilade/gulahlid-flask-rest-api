from flask import Blueprint, request, jsonify
from app import db
from .models import Agenda, Shift, Role, Group, Employee, EmployeeInfo, Kid, KidInfo
from .schemas import agenda_schema, agendas_schema, shift_schema, role_schema, roles_schema, group_schema, \
    groups_schema, employee_schema, employees_schema, employee_info_schema, employees_infos_schema, kid_schema, \
    kids_schema, kid_info_schema, kids_infos_schema


# Defining as a blueprint allows to store routes in different documents or "blueprints"
generator = Blueprint('generator', __name__)


# ///////////////// AGENDA /////////////////

# Create Agenda
@generator.route('/generator', methods=['POST'])
def generate_agenda():
    # get agenda id
    # get all employees
    # get all kids

    # create employees info
    # create kids info

    # get dictionary of employees per day
    # get dictionary of kids per day

    # get dictionary of difficult kids and their circle of employees
    # get dictionary of kids with two employees

    # create shifts

    return "foo"
