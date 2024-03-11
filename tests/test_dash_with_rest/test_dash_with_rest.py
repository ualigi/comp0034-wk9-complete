import requests
from dash.testing.application_runners import import_app


def test_server_live(dash_duo):
    """
    GIVEN a dash_duo fixture instance of the server with the app
    WHEN a HTTP request to the home page is made
    THEN the HTTP response status code should be 200
    """

    # Create the app
    app = import_app(app_file="dash_app_uses_rest.app_dash")

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
