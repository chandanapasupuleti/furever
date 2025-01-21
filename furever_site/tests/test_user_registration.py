import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver for all tests
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_account_creation(driver):
    # Open the registration page
    driver.get("http://127.0.0.1:8000/signup")

    time.sleep(3)
    
    # Fill in the registration form
    driver.find_element(By.NAME, "username").send_keys("test2")
    driver.find_element(By.NAME, "email").send_keys("test1@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("test")
    driver.find_element(By.NAME, "re_password").send_keys("test")
    driver.find_element(By.NAME, "location").send_keys("Carolina")

    # Submit the form
    driver.find_element(By.ID, "id_age_0").click()
    driver.find_element(By.NAME, "signup_btn").click()
    
    # Wait for page to load
    time.sleep(3)
    
    # Verify that registration is successful
    success_message = driver.find_element(By.XPATH, "/html/body/h2").text
    assert "Log In" in success_message

