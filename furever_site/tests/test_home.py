import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login_to_home(driver):
    # Open the registration page
    driver.get("http://127.0.0.1:8000/accounts/login/")

    time.sleep(3)
    
    # Fill in the registration form
    driver.find_element(By.ID, "id_username").send_keys("test1")
    driver.find_element(By.ID, "id_password").send_keys("test")

    driver.find_element(By.ID, "login_btn").click()
    # Wait for page to load
    time.sleep(3)
    

    # Verify that registration is successful
    success_message = driver.find_element(By.XPATH, "/html/body/a[1]").text
    assert "A Beginner’s Guide to Having a Pet Cat" in success_message

def test_edu_resource_download(driver):
    driver.find_element(By.XPATH, "/html/body/a[1]").click()
    time.sleep(5)
    file_path="C:\\Users\\lenovo\\Downloads\\Cat_Beginner_Guide.pdf"
    assert os.path.exists(file_path)





