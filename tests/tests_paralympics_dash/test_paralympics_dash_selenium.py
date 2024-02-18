import requests
from selenium.webdriver import Keys
from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By


def test_server_live(dash_duo):
    """
    GIVEN the app is running
    WHEN a HTTP request to the home page is made
    THEN the HTTP response status code should be 200
    """

    # Start the app in a server
    app = import_app(app_file="paralympics_dash.paralympics_app")
    dash_duo.start_server(app)
    # Delay to wait 2 seconds for the page to load
    dash_duo.driver.implicitly_wait(2)

    url = dash_duo.driver.current_url
    response = requests.get(url)
    assert response.status_code == 200


def test_home_h1textequals(dash_duo):
    """

    NOTE: dash_duo has a scope of fixture, so you have to start the server each time. There is no stop_server function,
    the dash_duo fixture handles this

    GIVEN the app is running
    WHEN the home page is available
    THEN the H1 heading text should be "Paralympics Dashboard"
    """
    app = import_app(app_file="paralympics_dash.paralympics_app")
    dash_duo.start_server(app)
    dash_duo.driver.implicitly_wait(2)

    dash_duo.wait_for_element("h1", timeout=4)
    h1_text = dash_duo.find_element("h1").text
    assert h1_text == "Paralympics Dashboard"


def test_line_chart_selection(dash_duo):
    """
    GIVEN the app is running
    WHEN the dropdown for the line chart is changed to
    THEN the H1 heading text should be "Paralympics Dashboard"
    """
    app = import_app(app_file="paralympics_dash.paralympics_app")
    dash_duo.start_server(app)
    dash_duo.driver.implicitly_wait(2)

    # See https://github.com/plotly/dash/blob/dev/components/dash-core-components/tests/integration/dropdown/test_dynamic_options.py#L31
    # Not easy to follow but give syntax for selecting values in a dropdown list
    dropdown_input = dash_duo.find_element("#type-dropdown")
    dropdown_input.send_keys("Sports")
    dash_duo.driver.implicitly_wait(2)

    # To find part of a graph is not easy, selecting the id of the chart does not let you find chart name etc
    # One technique is to find the Xpath of the component you want using a Chrome browser.
    # See answers https://stackoverflow.com/questions/59961926/how-to-get-absolute-xpath-in-chrome-or-firefox

    # Currently fails!
    xpath = '/html/body/div/div/div/div[3]/div[1]/div/div/div[3]/div[1]/div/div[2]/div/div/svg[2]/g[4]/g[2]/text'
    chart_title = dash_duo.driver.find_element(By.XPATH, xpath)

    # line_div = dash_duo.find_element("#line .g-gtitle .gtitle .gtitle")

    assert ("sports" in chart_title.text), "'sports' should appear in the chart title"
