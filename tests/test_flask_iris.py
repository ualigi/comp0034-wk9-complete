import time

import pytest
from flask import url_for
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from flask_iris import create_app
from flask_iris.config import TestConfig


# Fixtures are in the file as they supersede the versions in conftest.py.
# Another approach would be to have subdirectories and multiple conftest.py.
@pytest.fixture(scope='session')
def app():
    """Fixture to create the Flask app and configure for testing"""

    app = create_app(TestConfig)

    yield app


@pytest.fixture(scope='session')
def live_server(app):
    """Fixture to
    run the Flask app as a live server."""

    server = app.test_cli_runner().invoke(args=['run', '--no-reload', '--port=5000'])

    time.sleep(10)

    # Ensure the server is up and running
    # assert server.exit_code == 0
    yield 'http://localhost:5000'

    # Teardown: Stop the Flask server
    server.terminate()


def test_prediction_returns_value(live_server, chrome_driver):
    iris = {"sepal_length": 4.8, "sepal_width": 3.0, "petal_length": 1.4, "petal_width": 0.1, "species": "iris-setosa"}
    # Go to the home page (uses Flask url_for)
    chrome_driver.get(url_for("index", _external=True))
    # Complete the fields in the form
    sep_len = chrome_driver.find_element(By.NAME, "sepal_length")
    sep_len.send_keys(iris["sepal_length"])
    sep_wid = chrome_driver.find_element(By.NAME, "sepal_width")
    sep_wid.send_keys(iris["sepal_width"])
    pet_len = chrome_driver.find_element(By.NAME, "petal_length")
    pet_len.send_keys(iris["petal_length"])
    pet_wid = chrome_driver.find_element(By.NAME, "petal_width")
    pet_wid.send_keys(iris["petal_width"])
    # Click the submit button
    chrome_driver.find_element(By.ID, "btn-predict").click()
    # Wait for the prediction text to appear on the page and then get the <p> with the id=“prediction-text”
    pt = WebDriverWait(chrome_driver, timeout=3).until(lambda d: d.find_element(By.ID, "prediction-text"))
    # Assert that 'setosa' is in the text value of the <p> element.
    assert iris["species"] in pt.text
