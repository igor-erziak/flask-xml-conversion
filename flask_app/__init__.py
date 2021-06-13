from flask import Flask
from flask_httpauth import HTTPBasicAuth
from os import environ
import flask_app.api_helper as ah
import flask_app.xml_convertor as xc
import sys

try:
    CREDS = {
        "username": environ["APP_USERNAME"],
        "password": environ["APP_PASSWORD"]
    }
except KeyError as e:
    print(f'KeyError: the environment variable {e} is not set.')
    sys.exit('Terminating...')

def create_app():
    app = Flask(__name__)
    auth = HTTPBasicAuth()

    @auth.verify_password
    def verify_password(username, password):
        if username == CREDS['username'] and password == CREDS['password']:
            return username

    @app.route("/export/<int:annotation_id>")
    @auth.login_required
    def export(annotation_id):
        try:
            auth_key = ah.get_auth_key()
        except Exception as e:
            print(e)
            return f"Not able to log into Rossum API", 403

        try:
            xml = ah.get_annotation_xml(annotation_id, auth_key)
        except Exception as e:
            print(e)
            return f"Not able to retrieve the requested annotation", 404

        converted_xml = xc.convert_xml(xml)

        try:
            result = ah.submit_xml(annotation_id, converted_xml)
        except Exception as e:
            print(e)
            result = False

        return {"success": result}

    @app.route("/")
    @app.route("/export/")
    def index():
        return 'Go to <a href="/export/6439416">/export/6439416</a>'

    return app