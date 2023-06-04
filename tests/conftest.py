import pytest
from base_handler import BaseHandler

@pytest.fixture
def browser():
    browser = BaseHandler(headless=False)
    browser.init_chrome_driver()
    yield browser
    browser.close_driver()