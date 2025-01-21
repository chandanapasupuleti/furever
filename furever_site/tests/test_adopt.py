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

def test_login_to_lost(driver):
    # Open the registration page
    driver.get("http://127.0.0.1:8000/adopt")

    time.sleep(3)
    
    # Fill in the registration form
    driver.find_element(By.ID, "id_username").send_keys("test1")
    driver.find_element(By.ID, "id_password").send_keys("test")

    driver.find_element(By.ID, "login_btn").click()
    # Wait for page to load
    time.sleep(3)
    

    # Verify that registration is successful
    success_message = driver.find_element(By.XPATH, "/html/body/a").text
    assert "Add pet for adopt" in success_message



def test_report_adopt_pet(driver):
    # Open the adopt page
    parent_div = driver.find_element(By.XPATH, "/html/body/div") 
    init_count=len(parent_div.find_elements(By.TAG_NAME, "div"))
    # Click on the button to add a pet for adoption
    driver.find_element(By.XPATH, "/html/body/a").click()
    
    # Fill in the form with the pet details
    driver.find_element(By.ID, "dog").click()
    driver.find_element(By.ID, "name").clear()

    driver.find_element(By.ID, "name").send_keys("happbee")

    dropdown=driver.find_element(By.ID, "breeds_dog")
    select=Select(dropdown)
    select.select_by_visible_text("Beagle")
    time.sleep(2)
    dropdown=driver.find_element(By.ID, "pet_gender")
    select=Select(dropdown)
    select.select_by_visible_text("Male")
    time.sleep(2)
    driver.find_element(By.ID, "color").send_keys("grey")
    driver.find_element(By.ID, "age").send_keys("6")
    driver.find_element(By.ID, "weight").send_keys("3")
    driver.find_element(By.ID, "vaccination").send_keys("21-10-2024")
    driver.find_element(By.ID, "health_issues").send_keys("none")
    dropdown=driver.find_element(By.ID, "Behavior_people")
    select=Select(dropdown)
    select.select_by_visible_text("Neutral")
    time.sleep(2)
    dropdown=driver.find_element(By.ID, "Behavior_animals")
    select=Select(dropdown)
    select.select_by_visible_text("Neutral")
    time.sleep(2)
    driver.find_element(By.ID, "Trainings").send_keys("No")
    driver.find_element(By.ID, "Activities").send_keys("Loves to play with toys")
    dropdown=driver.find_element(By.ID, "Energy_level")
    select=Select(dropdown)
    select.select_by_visible_text("Neutral")
    time.sleep(2)
    dropdown=driver.find_element(By.ID, "prev_owner")
    select=Select(dropdown)
    select.select_by_visible_text("Yes")
    time.sleep(2)
    pic_path="C:\\Users\\lenovo\\Downloads\\pup.jpg"
    driver.find_element(By.ID, "img").send_keys(pic_path)

    time.sleep(2)
    # Submit the form
    driver.find_element(By.ID, "submit_btn").click()
    
    # Wait for the report to be processed
    time.sleep(20)
    
    # Verify that the report was submitted successfully
    parent_div = driver.find_element(By.XPATH, "/html/body/div") 

    final_count=len(parent_div.find_elements(By.TAG_NAME, "div"))

    assert init_count+2==final_count

    time.sleep(50)
