import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_server_is_up_and_running(live_server, client):
    # Uses the flask test client which makes a HTTP request and gets back a HTTP response
    # Chrome driver navigates to the page and does not access HTTP response
    response = client.get('/')
    assert response.status_code == 200
    assert b'Paralympics' in response.data


def test_home_page_title(chrome_driver, live_server):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    THEN the value of the page title should be "Paralympics - Home"
    """
    # Change the url if you configured a different port!
    chrome_driver.get("http://127.0.0.1:5000/")
    # Wait for the title to be there and its value to be "Paralympics - Home"
    WebDriverWait(chrome_driver, 200).until(EC.title_is("Paralympics - Home"))
    assert chrome_driver.title == "Paralympics - Home"


def test_event_detail_page_selected(chrome_driver, live_server):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the id="1"
    THEN a page with the title "Rome" should be displayed
    AND the page should contain an element with the id "highlights"
    should be displayed and contain a text value "First Games"
    """
    chrome_driver.get("http://127.0.0.1:5000/")
    # Wait until element with id="1" is on the page then click it (this will be the URL for Rome)
    # https://www.selenium.dev/documentation/webdriver/waits/
    el_1 = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "1")
    )
    el_1.click()
    # Clicking on the links takes you to the event details page for Rome
    # Wait until event highlights is visible
    text = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "highlights")
    )
    assert "First Games" in text.text


def test_home_nav_link_returns_home(chrome_driver, live_server):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND then the user clicks on the event with the id="1"
    AND then the user clicks on the navbar in the 'Home' link
    THEN the page url should be "http://127.0.0.1:5000/"
    """
    chrome_driver.get("http://127.0.0.1:5000/")
    # Wait until element with id="1" is on the page then click
    # https://www.selenium.dev/documentation/webdriver/waits/
    el_1 = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "1")
    )
    el_1.click()
    nav_home = WebDriverWait(chrome_driver, timeout=5).until(
        EC.element_to_be_clickable((By.ID, "nav-home"))
    )
    nav_home.click()
    url = chrome_driver.current_url
    assert url == "http://127.0.0.1:5000/"
