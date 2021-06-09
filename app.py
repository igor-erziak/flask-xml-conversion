from flask import Flask, abort
from flask_httpauth import HTTPBasicAuth
from os import environ

app = Flask(__name__)
auth = HTTPBasicAuth()

creds = {
    "username": environ.get("ROSSUM_USERNAME"),
    "password": environ.get("ROSSUM_PASSWORD")
}

@auth.verify_password
def verify_password(username, password):
    if username == creds['username'] and password == creds['password']:
        return username

@app.route("/export")
@auth.login_required
def export():
    return f"XML file for user {auth.current_user()}"

