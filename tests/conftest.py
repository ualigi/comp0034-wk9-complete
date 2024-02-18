import os
import pytest
from selenium.webdriver import Chrome, ChromeOptions

'''
@pytest.fixture(scope="function")
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
'''