from flask import Flask, abort
from flask_httpauth import HTTPBasicAuth
from os import environ
import api_helper as ah

app = Flask(__name__)
auth = HTTPBasicAuth()

CREDS = {
    "username": environ.get("APP_USERNAME"),
    "password": environ.get("APP_PASSWORD")
}

@auth.verify_password
def verify_password(username, password):
    if username == CREDS['username'] and password == CREDS['password']:
        return username

@app.route("/export/<int:annotation_id>")
@auth.login_required
def export(annotation_id):
    auth_key = ah.get_auth_key()
    xml = ah.get_annotation_xml(annotation_id, auth_key)

    return f'<h1>Authenticated as {auth.current_user()}</h1>' + '<textarea rows="40" cols="140">' + xml + '</textarea>'