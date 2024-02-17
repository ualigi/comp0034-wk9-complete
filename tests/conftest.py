import time

import pytest

from paralympics_flask import create_app
from selenium.webdriver import Chrome, ChromeOptions


@pytest.fixture(scope='session')
def app():
    """Fixture to create the Flask app and configure for testing"""
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
    """Fixture to
    run the Flask app as a live server."""

    server = app.test_cli_runner().invoke(args=['run', '--no-reload', '--port=5000'])
    # server = app.cli.invoke(args=['run', '--no-reload', '--port=5000'])

    time.sleep(2)

    # Ensure the server is up and running
    # assert server.exit_code == 0
    yield server

    # Teardown: Stop the Flask server
    server.terminate()


@pytest.fixture(scope="session")
def chrome_driver():
    options = ChromeOptions()
    # Make the window large enough that all the dashboard appears
    options.add_argument("start-maximized")
    options.add_argument('--proxy-server=localhost:8080')
    # options.add_argument("--window-size=1920,1080")
    driver = Chrome(options=options)
    yield driver
    driver.quit()
