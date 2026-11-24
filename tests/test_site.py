import os
import tempfile
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8091")


@pytest.fixture
def driver():
    with tempfile.TemporaryDirectory() as profile:
        options = Options()
        options.binary_location = "/usr/bin/chromium"
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,800")
        options.add_argument("--user-data-dir=" + profile)

        browser = webdriver.Chrome(
            service=Service("/usr/bin/chromedriver"),
            options=options
        )

        try:
            yield browser
        finally:
            browser.quit()


def test_page_title(driver):
    driver.get(BASE_URL)
    assert driver.title == "Cloud Computing - SP23-BSE-032"


def test_heading(driver):
    driver.get(BASE_URL)
    assert driver.find_element(By.ID, "heading").text == "Cloud Deployment Portal"


def test_message_button(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "greet").click()
    assert driver.find_element(By.ID, "message").text == "Welcome to my cloud application!"


def test_text_input(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "userInput").send_keys("Cloud Computing Test")
    driver.find_element(By.ID, "submit").click()
    assert driver.find_element(By.ID, "output").text == "Cloud Computing Test"
    driver.save_screenshot("screenshot.png")
