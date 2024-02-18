import os
import pytest
from selenium.webdriver import Chrome, ChromeOptions

from paralympics_flask import create_app


@pytest.fixture(scope="module")
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


'''
@pytest.fixture(scope='session')
def start_live_server(live_server):
    """
    Fixture to start the live server based on the pytest-flask module.
    Live server has a scope of session by default
    See https://pytest-flask.readthedocs.io/en/latest/features.html#live-server-application-live-server
    :param live_server:
    :return:
    """
    live_server.start()
    time.sleep(3)
    yield live_server
    live_server.stop()
'''

'''
@pytest.fixture(scope='session')
def live_server():
    """Fixture to run the paralympics_flask app as a live server.

    Runs the server in a separate thread, so it can run at the same time as the tests.
    """
    #test_cfg = {"TESTING": True, "WTF_CSRF_ENABLED": False}
    # paralympics = f"paralympics_flask:create_app('test_config={{'TESTING': True, 'WTF_CSRF_ENABLED': False}}')"
    try:
        # server = subprocess.Popen(["flask", "--app", paralympics, "run", "--port", "5000"])
        server = subprocess.Popen(["flask", "--app", "paralympics_flask", "run", "--port", "5000"])
        # Allows time for the app to start
        time.sleep(3)
        yield server
        server.terminate()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask app: {e}")
'''