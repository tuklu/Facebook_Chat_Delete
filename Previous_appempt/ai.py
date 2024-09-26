import cv2
import numpy as np
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC

# Edge options
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)  # Keeps the browser open after script ends

# Initialize WebDriver with Edge options
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

try:
    # Open Facebook
    # driver.get("https://www.facebook.com/")
    driver.get("https://www.facebook.com/messages/t/100015570004872/")
        
    # Log in
    email_element = driver.find_element(By.ID, "email")
    email_element.send_keys("name@example.com")
    password_element = driver.find_element(By.ID, "pass")
    password_element.send_keys("password")
    password_element.send_keys(Keys.RETURN)

    # Wait for login to be completed by checking for the post-login Facebook logo element
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Facebook']"))
    )

    # Open Facebook Messenger directly (skip login for now)
    # driver.get("https://www.facebook.com/messages/t/100015570004872/")

    # Wait for the Messenger page to fully load
    WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # Hover over the hidden menu button (based on the role attribute)
    menu_button = WebDriverWait(driver, 30).until(
        # EC.presence_of_element_located((By.XPATH, "(//div[@aria-label='Menu'])[2]"))
        EC.presence_of_element_located((By.CSS_SELECTOR, "body div div div div div div div div div div[aria-label='Thread list'] div div div div div div div[aria-label='Chats'] div div div div div div:nth-child(1) div:nth-child(1) div:nth-child(1) div:nth-child(1) div:nth-child(2) div:nth-child(1) div:nth-child(1) div:nth-child(1) div:nth-child(1)"))
    )

    # Perform hover action using ActionChains
    actions = ActionChains(driver)
    actions.move_to_element(menu_button).perform()  # Hover over the menu button

    # Wait for the flyout menu to appear and click on "Delete Chat" (adjust this as per the actual element)
    delete_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Delete Chat']"))
    )

    # Click on the "Delete Chat" button
    delete_button.click()

    # You can add additional waits or checks to confirm chat deletion
    print("Chat deletion button clicked successfully.")

finally:
    pass  # Keep the browser session open for inspection