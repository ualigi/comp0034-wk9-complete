from dash.testing.application_runners import import_app


def test_home_h1textequals(dash_duo):
    """
    GIVEN the app is running
    WHEN the home page is available
    THEN the page title should be
    """
    # Create the app
    app = import_app(app_file="paralympics_dash.paralympics_dash.py")

    # Start the app in a server
    yield dash_duo.start_server(app)

    # Waits for the page, this is a Dash function not Selenium see https://dash.plotly.com/testing#browser-apis
    dash_duo.wait_for_page(url='http://127.0.0.1:8050', timeout=10)

    dash_duo.wait_for_element("h1", timeout=4)

    h1_text = dash_duo.find_element("h1").text
    assert h1_text == "Paralympics Dashboard"
