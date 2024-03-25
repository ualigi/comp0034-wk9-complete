import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def test_server_is_up_and_running(live_server_iris):
    """Check the app is running"""
    # Chrome_driver navigates to the page,
    # whereas requests.get makes an HTTP GET request and returns an HTTP response
    response = requests.get("http://127.0.0.1:5000")
    assert response.status_code == 200


def test_prediction_returns_value(live_server_iris, chrome_driver):
    """
    GIVEN a chrome driver and live server running the Iris app
    WHEN appropriate values are passed to the prediction form
    THEN there should be element that has an id="prediction-text"
    """
    iris = {"sepal_length": 4.8, "sepal_width": 3.0, "petal_length": 1.4, "petal_width": 0.1, "species": "iris-setosa"}
    # Go to the home page (uses Flask url_for)
    chrome_driver.get("http://127.0.0.1:5000/")
    sep_len = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.NAME, "sepal_length")
    )

    time.sleep(2)

    # Complete the fields in the form
    # sep_len = chrome_driver.find_element(By.ID, "sepal_length")
    sep_len.clear()
    sep_len.send_keys(iris["sepal_length"])
    sep_wid = chrome_driver.find_element(By.ID, "sepal_width")
    sep_wid.clear()
    sep_wid.send_keys(iris["sepal_width"])
    pet_len = chrome_driver.find_element(By.ID, "petal_length")
    pet_len.clear()
    pet_len.send_keys(iris["petal_length"])
    time.sleep(2)
    pet_wid = chrome_driver.find_element(By.ID, "petal_width")
    pet_wid.clear()
    pet_wid.send_keys(iris["petal_width"])

    # Click the submit button
    chrome_driver.find_element(By.ID, "btn-predict").click()

    # Wait for the prediction text to appear on the page and then get the <p> with the id=“prediction-text”
    pt = WebDriverWait(chrome_driver, timeout=3).until(lambda d: d.find_element(By.ID, "prediction-text"))

    # Assert that 'setosa' is in the text value of the <p> element.
    assert iris["species"] in pt.text
