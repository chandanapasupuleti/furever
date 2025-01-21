import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
found_child=None
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login_to_forum(driver):
    # Open the registration page
    driver.get("http://127.0.0.1:8000/forum")

    time.sleep(3)
    
    # Fill in the registration form
    driver.find_element(By.ID, "id_username").send_keys("test1")
    driver.find_element(By.ID, "id_password").send_keys("test")

    driver.find_element(By.ID, "login_btn").click()
    # Wait for page to load
    time.sleep(3)
    

    # Verify that registration is successful
    success_message = driver.find_element(By.XPATH, "/html/body/div/h2").text
    assert "Forum" in success_message

def test_add_post(driver):
 
    driver.find_element(By.XPATH, "/html/body/div/a").click()

    driver.find_element(By.ID, "id_title").send_keys("some random heading8")
    driver.find_element(By.ID, "id_description").send_keys("some random desc")

    driver.find_element(By.ID, "submit_btn").click()
    time.sleep(3)

    parent_div = driver.find_element(By.CLASS_NAME, 'posts')  # Or other methods like By.CLASS_NAME

    # Find all child divs within the parent div
    child_divs = parent_div.find_elements(By.TAG_NAME, 'a')  # Finds all child divs

    # Define the name you're searching for
    name_to_check = "some random heading8"  # Replace with the actual name you're looking for

    # Loop through each child div to check if the name exists in its text
    found = False
    for child in child_divs:
        if name_to_check in child.text:
            found = True
            global found_child
            found_child=child
            break
    assert found



def test_add_comment(driver):
    found_comment=False
    found_child.click()
    driver.find_element(By.ID, "add_comment").send_keys("naisu")

    driver.find_element(By.NAME, "submit_comment_button").click()


    time.sleep(5)
    # Find all div elements with class name "blah"
    divs = driver.find_elements(By.CLASS_NAME, "comments")

    # Search for text inside these divs
    search_text = "naisu"  # Replace with the text you are looking for
    search_text_lower = search_text.lower()  
    for div in divs:
        # Find all section elements inside the div
        sections = div.find_elements(By.TAG_NAME, "section")
        print(f"Found {len(sections)} sections in this div.")  # Debug: print the number of sections found
        
        for section in sections:
            section_text = section.text.strip()  # Get text and remove leading/trailing spaces
            print(f"Section text: '{section_text}'")  # Debug: print the section text
            
            # Case-insensitive comparison for the search text
            if search_text_lower in section_text.lower():
                print(f"Text '{search_text}' found in section: {section_text}")  # Debug: when text is found
                found_comment = True
                break  # Exit loop once the text is found

    # Assert if the comment was found
    assert found_comment, f"Comment with the specified text '{search_text}' was not found."


    
    