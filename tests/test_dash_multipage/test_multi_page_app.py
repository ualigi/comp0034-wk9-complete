# A basic test to check that a multipage app can be accessed using dash_duo
import time

import requests
from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By


def test_server_live(dash_duo):
    """
    GIVEN a dash_duo fixture instance of the server with the app
    WHEN a HTTP request to the home page is made
    THEN the HTTP response status code should be 200
    """

    app = import_app(app_file="dash_multi.multi_app")
    dash_duo.start_server(app)
    time.sleep(3)

    # Get the url for the web app root
    url = dash_duo.driver.current_url

    # Make a HTTP request to the server.
    # This uses the Python requests library rather than the dash_duo client so that we can access the status code.
    response = requests.get(url)
    assert response.status_code == 200


def test_nav_link_charts(dash_duo):
    """
    Check the nav link works and leads to the charts page.
    """
    app = import_app(app_file="dash_multi.multi_app")
    dash_duo.start_server(app)
    # Delay just so I can visually check the page is loaded, this isn't necessary!
    time.sleep(2)

    # Wait for the navlink to be visible
    dash_duo.wait_for_element("#nav-charts", timeout=4)

    # Click on the navlink
    dash_duo.driver.find_element(By.ID, "nav-charts").click()

    # Delay just so I can visually check the page is loaded, this isn't necessary!
    time.sleep(2)

    # Check the page url includes "charts"
    dash_duo.wait_for_element("#nav-charts", timeout=4)
    assert "charts" in dash_duo.driver.current_url


def test_nav_link_event(dash_duo):
    """
    Check the nav link works and leads to the event page.
    """
    app = import_app(app_file="dash_multi.multi_app")
    dash_duo.start_server(app)
    # Delay just so I can visually check the page is loaded, this isn't necessary!
    time.sleep(1)

    # Wait for the charts navlink to be visible
    dash_duo.wait_for_element("#nav-charts", timeout=4)
    # Click on the charts page navlink
    dash_duo.driver.find_element(By.ID, "nav-charts").click()
    # Delay just so I can visually check the page is loaded, this isn't necessary!
    time.sleep(1)
    # Wait for the event navlink to be visible
    dash_duo.wait_for_element("#nav-event", timeout=4)
    # Click on the navlink
    dash_duo.driver.find_element(By.ID, "nav-event").click()
    # Delay just so I can visually check the page is loaded, this isn't necessary!
    time.sleep(1)

    # Check the page H1 include the words "event details"
    dash_duo.wait_for_element("H1", timeout=4)
    h1_text = dash_duo.driver.find_element(By.TAG_NAME, "H1").text
    assert h1_text.lower() == "event details"
