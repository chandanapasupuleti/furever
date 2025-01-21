import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login_to_profile(driver):
    # Open the registration page
    driver.get("http://127.0.0.1:8000/profile")

    time.sleep(3)
    
    # Fill in the registration form
    driver.find_element(By.ID, "id_username").send_keys("test1")
    driver.find_element(By.ID, "id_password").send_keys("test")

    driver.find_element(By.ID, "login_btn").click()
    # Wait for page to load
    time.sleep(3)
    

    # Verify that registration is successful
    success_message = driver.find_element(By.XPATH, "/html/body/h2").text
    assert "Profile" in success_message

def test_profile_pet(driver):
 
    driver.find_element(By.ID, "edit").click()
    driver.find_element(By.ID, "email").clear()

    driver.find_element(By.ID, "email").send_keys("test2@gmail.com")
    driver.find_element(By.ID, "update_button").click()
    time.sleep(5)
    result=driver.find_element(By.ID, "email").get_attribute("value")
    assert result=="test2@gmail.com"




    