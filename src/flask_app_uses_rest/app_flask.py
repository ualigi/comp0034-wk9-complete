from flask import Blueprint, url_for
import requests

main = Blueprint('main', __name__)


@main.route("/")
def index():
    html = '<a id="main-link" href="' + url_for('main.get_rest') + '">Go to rest api page</a>'
    return html


@main.route("/rest")
def get_rest():
    """
    Simple example to allow a test that shows how you can run the Flask app that uses the REST App for testing
    """
    response = requests.get("http://127.0.0.1:5001/events/1")
    json = response.json()
    return json
