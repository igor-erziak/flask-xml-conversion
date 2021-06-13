from flask import Blueprint
import sys
from os import environ
from flask_httpauth import HTTPBasicAuth
from . import api_helper as ah
from . import xml_convertor as xc

auth = HTTPBasicAuth()

export_bp = Blueprint('export', __name__)

try:
    CREDS = {
        "username": environ["APP_USERNAME"],
        "password": environ["APP_PASSWORD"]
    }
except KeyError as e:
    print(f'KeyError: the environment variable {e} is not set.')
    sys.exit('Terminating...')

@auth.verify_password
def verify_password(username, password):
    if username == CREDS['username'] and password == CREDS['password']:
        return username

@export_bp.route("/export/<int:annotation_id>")
@auth.login_required
def export(annotation_id):
    try:
        auth_key = ah.get_auth_key()
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