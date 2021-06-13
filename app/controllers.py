from flask import Blueprint
from flask import current_app as app
import sys
from os import environ
from flask_httpauth import HTTPBasicAuth
from . import api_helper as ah
from . import xml_convertor as xc

export_bp = Blueprint('export', __name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username == app.config['APP_USERNAME'] and password == app.config['APP_PASSWORD']:
        return username

@export_bp.route("/export/<int:annotation_id>")
@auth.login_required
def export(annotation_id):
    try:
        auth_key = ah.get_auth_key(app.config['ROSSUM_USERNAME'], app.config['ROSSUM_PASSWORD'])
    except Exception as e:
        print(repr(e))
        return f"Not able to log into Rossum API", 403

    try:
        xml = ah.get_annotation_xml(annotation_id, auth_key)
    except Exception as e:
        print(repr(e))
        return f"Not able to retrieve the requested annotation", 404

    converted_xml = xc.convert_xml(xml)

    try:
        result = ah.submit_xml(annotation_id, converted_xml)
    except Exception as e:
        print(repr(e))
        result = False

    return {"success": result}


@export_bp.route("/")
@export_bp.route("/export/")
def index():
    return 'Go to <a href="/export/6439416">/export/6439416</a>'