import os
import pytest
from selenium.webdriver import Chrome, ChromeOptions
import subprocess
import time


@pytest.fixture(scope="session")
def chrome_driver():
    """
    Fixture to create a Chrome driver.

    On GitHub or other container it needs to run headless, i.e. the browser doesn't open and display on screen.
    Running locally you may want to display the tests in a large window to visibly check the behaviour.
    """
    options = ChromeOptions()
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
    else:
        options.add_argument("start-maximized")
    driver = Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def run_rest_api():
    """Runs the Flask REST API app as a live server

    """
    command = """flask --app 'paralympics_rest:create_app()' run --port 5001"""
    try:
        server = subprocess.Popen(command, shell=True)
        # Allow time for the app to start
        time.sleep(3)
        yield server
        server.terminate()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask REST API app: {e}")


@pytest.fixture(scope="session", autouse=True)
def run_main_flask_app(run_rest_api):
    """Runs the example Flask app that itself uses the Flask REST app
    """
    command = """flask --app flask_app_uses_rest run --port 5000"""
    try:
        server = subprocess.Popen(command, shell=True)
        # Allow time for the app to start
        time.sleep(3)
        yield server
        server.terminate()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask app: {e}")
