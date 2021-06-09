from flask import Flask, abort
from flask_httpauth import HTTPBasicAuth
from os import environ

app = Flask(__name__)
auth = HTTPBasicAuth()

CREDS = {
    "username": environ.get("ROSSUM_USERNAME"),
    "password": environ.get("ROSSUM_PASSWORD")
}
ANNOTATION_ID = 123456

@auth.verify_password
def verify_password(username, password):
    if username == CREDS['username'] and password == CREDS['password']:
        return username

@app.route("/export/<int:annotation_id>")
@auth.login_required
def export(annotation_id):
    if annotation_id == ANNOTATION_ID:
        return f"Success for user {auth.current_user()} and annotation ID {annotation_id}"
    else:
        return f"Wrong annotation id for user {auth.current_user()}"

