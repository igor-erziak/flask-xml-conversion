from flask import Flask
from . import controllers

def create_app():
    app = Flask(__name__)

    app.register_blueprint(controllers.export_bp)
    app.config.from_object('config')

    return app