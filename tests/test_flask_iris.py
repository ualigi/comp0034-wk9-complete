import subprocess
import time

import pytest
import requests
from flask import url_for
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


# Fixtures are in the file as they supersede the versions in conftest.py.
# Another approach would be to have subdirectories and multiple conftest.py.
@pytest.fixture(scope='session')
def live_server_iris():
    """Fixture to run the Flask app as a live server."""

    # Use subprocess to run the Flask app using the command line runner
    try:
        # You can customize the command based on your Flask app structure
        server = subprocess.Popen(
            ["flask", "--app", "flask_iris:create_app('test')", "run", "--port=5000"])
        # wait for the server to start
        time.sleep(2)
        yield server
        # Teardown: Stop the Flask server
        server.terminate()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask app: {e}")


def test_server_is_up_and_running(live_server_iris):
    """Check the app is running"""
    # Chrome_driver navigates to the page, whereas requests.get makes an HTTP request and returns an HTTP response
    response = requests.get("http://127.0.0.1:5000")
    assert response.status_code == 200


def test_prediction_returns_value(live_server, chrome_driver):
    iris = {"sepal_length": 4.8, "sepal_width": 3.0, "petal_length": 1.4, "petal_width": 0.1, "species": "iris-setosa"}
    # Go to the home page (uses Flask url_for)
    chrome_driver.get("http://127.0.0.1:5000/")
    sep_len = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.NAME, "sepal_length")
    )
    # Complete the fields in the form
    # sep_len = chrome_driver.find_element(By.NAME, "sepal_length")
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
