import requests
from dash.testing.application_runners import import_app
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


def test_server_live(dash_duo):
    """
    GIVEN a dash_duo fixture instance of the server with the app
    WHEN a HTTP request to the home page is made
    THEN the HTTP response status code should be 200
    """

    # Create the app
    app = import_app(app_file="paralympics_dash.paralympics_app")
    # Start the server with the app using the dash_duo fixture
    dash_duo.start_server(app)

    # Delay to wait 2 seconds for the page to load
    dash_duo.driver.implicitly_wait(2)

    # Get the url for the web app root
    # You can print this to see what it is e.g. print(f'The server url is {url}')
    url = dash_duo.driver.current_url

    # Make a HTTP request to the server. This uses the Python requests library.
    response = requests.get(url)

    # Finally, use the pytest assertion to check that the status code in the HTTP response is 200
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

    # Wait for the H1 heading to be visible, timeout if this does not happen within 4 seconds
    dash_duo.wait_for_element("h1", timeout=4)

    # Find the text content of the H1 heading element
    h1_text = dash_duo.find_element("h1").text

    # Check the heading has the text we expect
    assert h1_text == "Paralympics Dashboard"


def test_map_marker_select_updates_card(dash_duo):
    """
    GIVEN the app is running which has a <div id='map>
    THEN there should not be any elements with a class of 'card' one the page
    WHEN a marker in the map is selected
    THEN the <div id="card"> should have a <div class="card"> element below it (or there should be one card on the page)
    """
    app = import_app(app_file="paralympics_dash.paralympics_app")
    dash_duo.start_server(app)
    # Wait for the div with id of card to be on the page
    dash_duo.wait_for_element("#card", timeout=2)

    # There is no card so finding elements with a bootstrap class of 'card' should return 0
    cards = dash_duo.driver.find_elements(By.CLASS_NAME, "card")
    cards_count_start = len(cards)

    # Find the first map marker
    marker_selector = '#map > div.js-plotly-plot > div > div > svg:nth-child(1) > g.geolayer > g > g.layer.frontplot > g > g > path:nth-child(1)'
    marker = dash_duo.driver.find_element(By.CSS_SELECTOR, marker_selector)
    # Use the Actions API and build a chain to move to the marker and hover
    ActionChains(dash_duo.driver).move_to_element(marker).pause(1).perform()

    # Check there is now 1 card on the page
    cards_end = dash_duo.driver.find_elements(By.CLASS_NAME, "card")
    cards_count_end = len(cards_end)
    # There should be 1 more card
    assert cards_count_end - cards_count_start == 1

    # Wait for the element with class of 'card'
    dash_duo.wait_for_element(".card", timeout=1)
    # Find the h6 element of the card
    card = dash_duo.find_element("#card > div > div > h6")
    # The test should be Rome as it is the first point, though this assertion just checks the length of the text
    assert len(card.text) > 2


def test_line_chart_selection(dash_duo):
    """
    GIVEN the app is running
    WHEN the dropdown for the line chart is changed to
    THEN the H1 heading text should be "Paralympics Dashboard"
    """
    app = import_app(app_file="paralympics_dash.paralympics_app")
    dash_duo.start_server(app)
    # To find an element by id you use '#id-name'; to find an element by class use '.class-name'
    dash_duo.wait_for_element("#type-dropdown", timeout=2)

    # See https://github.com/plotly/dash/blob/dev/components/dash-core-components/tests/integration/dropdown/test_dynamic_options.py#L31
    # Not easy to follow but give syntax for selecting values in a dropdown list
    dropdown_input = dash_duo.find_element("#type-dropdown")
    dropdown_input.send_keys("Sports")
    dash_duo.driver.implicitly_wait(2)

    # Run the app and use Chrome browser, find the element, right click and choose Select, find the element in the
    # Elements console and select 'copy selector'. Pate this as the value of the variable e.g. see css_selector below.
    css_selector = '#line > div.js-plotly-plot > div > div > svg:nth-child(3) > g.infolayer > g.g-gtitle > text'
    chart_title = dash_duo.find_element(css_selector)
    assert ("sports" in chart_title.text), "'sports' should appear in the chart title"
