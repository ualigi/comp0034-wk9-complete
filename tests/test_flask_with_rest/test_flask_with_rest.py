import json
import time

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def test_home_page_status_code():
    """
    GIVEN a live server
    WHEN a GET HTTP request to the home page is made
    THEN the HTTP response should have a status code of 200
    """
    url = f'http://127.0.0.1:5000/'
    response = requests.get(url)
    assert response.status_code == 200


def test_home_to_rest(chrome_driver):
    """
    GIVEN a running Flask app and chrome driver
    WHEN a GET HTTP request to the home page is made
    AND the link to the rest page is clicked on (this shows a page with the JSON for 1 paralympic event)
    THEN the page should contain valid JSON which is checked by ensure the 'NOC' attribute in the JSON is 3 chars long
    """
    url = f'http://127.0.0.1:5000/'
    chrome_driver.get(url)
    link = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "main-link")
    )
    link.click()
    time.sleep(2)

    # The JSON is placed in a <pre> tag in the page body
    pre = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.TAG_NAME, "pre")
    )

    # Get the string which is the innerHTML of the pre tag and then convert to a JSON object
    json_string = pre.get_attribute("innerHTML")
    event_json = json.loads(json_string)

    # The NOC code should be three characters long
    assert len(event_json['NOC']) == 3
