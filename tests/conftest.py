# multiprocess for macos, subprocess and socket for Windows
import multiprocessing
import time

# import subprocess
# import socket
import pytest
from paralympics_flask import create_app
from selenium.webdriver import Chrome, ChromeOptions


def run_flask_app(app_name):
    """
    Function to run the Flask app, called in the Process in the live_server fixture.
    """
    app_name.run(port=5000)  # Specify the port here


@pytest.fixture(scope='session')
def app():
    """Fixture to create the Flask app and configure for testing"""
    test_cfg = {"TESTING": True, }
    # app = create_app(test_config=test_cfg)
    app = create_app()
    yield app


@pytest.fixture(scope="session")
def live_server(app):
    """Fixture to run the Flask app as a live server.

     For MacOS.

     Sets multiprocessing to fork once per session. If already set once then on subsequent calls a runtime error
     will be raised which should be ignored. Needed in Python 3.8 and later.
     """
    try:
        multiprocessing.set_start_method("fork")
    except RuntimeError:
        pass
    process = multiprocessing.Process(target=run_flask_app, args=(app,))
    start_time = time.time()
    process.start()
    process.join(timeout=15)
    elapsed = time.time() - start_time
    print(f'elapsed time: {elapsed}')
    yield process
    process.terminate()


#  The followong are commented out as I use MacOS.
#  Windows users should uncomment this and instead comment out the live_server fixture on lines 17-26
'''
@pytest.fixture(scope="session")
def flask_port():
    """Ask the operating system for a free port.

    Solution from https://github.com/pytest-dev/pytest-flask/issues/54
    For Windows users only.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


@pytest.fixture(scope="session")
def live_server(flask_port):
    """Runs the Flask app as a live server

    Solution from https://github.com/pytest-dev/pytest-flask/issues/54
    For Windows users only.
    """
    server = subprocess.Popen(["flask", "--app",
                               "paralympics_flask",
                               "run", "--port", str(flask_port)])
    try:
        yield server
    finally:
        server.terminate()
'''


@pytest.fixture(scope="session")
def chrome_driver():
    options = ChromeOptions()
    # Make the window large enough that all the dashboard appears
    options.add_argument("--window-size=1920,1080")
    driver = Chrome(options=options)
    yield driver
    driver.quit()
