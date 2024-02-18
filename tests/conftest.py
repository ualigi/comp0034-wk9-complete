import os
import subprocess
import time
import pytest
from selenium.webdriver import Chrome, ChromeOptions

from paralympics_flask import create_app


@pytest.fixture(scope="session")
def chrome_driver():
    """
    Fixture to create a Chrome driver. Running locally this needs to be in a large window; on GitHub it needs to be headless
    """
    options = ChromeOptions()
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--headless")
    else:
        options.add_argument("start-maximized")
    driver = Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def app():
    """Fixture to create the paralympics_flask app and configure it for testing"""
    test_cfg = {
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    }

    app = create_app(test_config=test_cfg)

    yield app


@pytest.fixture(scope='session')
def client(app):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='session')
def live_server(app):
    """Fixture to run the paralympics_flask app as a live server.

    Runs the server in a separate thread, so it can run at the same time as the tests.
    """
    try:
        server = subprocess.Popen(["flask", "--app", "paralympics_flask", "run", "--port", "5000"])
        # Allows time for the app to start
        time.sleep(3)
        yield server
        server.terminate()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask app: {e}")
