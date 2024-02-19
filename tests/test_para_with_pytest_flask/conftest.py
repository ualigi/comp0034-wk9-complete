import json
import os
import socket
import subprocess
import time
import pytest
from selenium.webdriver import Chrome, ChromeOptions

from paralympics_flask import create_app


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
def app():
    """Fixture to create the paralympics_flask app and configure it for testing

    Required by the pytest-flask library; must be called 'app'
    See https://pytest-flask.readthedocs.io/en/latest/
    """
    test_cfg = {
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    }
    app = create_app(test_config=test_cfg)
    yield app
