import pytest
import subprocess
import time


@pytest.fixture(scope="session", autouse=True)
def run_rest_api():
    """Runs the Flask REST API app as a live server on port 5001

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
