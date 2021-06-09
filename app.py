from flask import Flask

app = Flask(__name__)

@app.route("/export")
def export():
    return "XML file here"

