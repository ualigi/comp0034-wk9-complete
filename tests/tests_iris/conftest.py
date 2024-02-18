import os
import subprocess
import time
import pytest
from selenium.webdriver import Chrome, ChromeOptions


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


@pytest.fixture(scope='module')
def live_server_iris():
    """Fixture to run the Flask app as a live server."""

    # Use subprocess to run the Flask app using the command line runner
    try:
        # You can customize the command based on your Flask app structure
        server_process = subprocess.Popen(
            ["flask", "--app", "flask_iris:create_app('test')", "run", "--port", "5000"])
        # wait for the server to start
        time.sleep(2)
        yield server_process
        # Teardown: Stop the Flask server
        server_process.terminate()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask app: {e}")
