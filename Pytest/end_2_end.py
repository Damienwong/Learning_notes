import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def browser():
    chrome_driver_path = 'D:\Codes\TestScript\QT\WebUpgrade\WebDriver\chromedriver.exe'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()


def test_google_search(browser):
    browser.get("https://www.google.com")
    assert 'Google' in browser.title

