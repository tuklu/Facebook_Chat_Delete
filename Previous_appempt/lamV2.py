import cv2
import numpy as np
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Initialize WebDriver
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

try:
    # Step 1: Visit Messenger and Log In
    driver.get("https://www.facebook.com/messages/")

    # Log in
    email_element = driver.find_element(By.ID, "email")
    email_element.send_keys("name@example.com")
    password_element = driver.find_element(By.ID, "pass")
    password_element.send_keys("password")
    password_element.send_keys(Keys.RETURN)

    # Wait for the Messenger page to fully load
    WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # Step 2: Wait for the presence of a specific element
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Facebook']"))
    )

    # Step 3: Press Tab 23 times
    for _ in range(23):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB)
        time.sleep(0.5)  # Optional delay for better navigation

    # Step 4: Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save("full_screenshot.png")

    # Step 5: Load the screenshot and template for matching
    img = cv2.imread("full_screenshot.png")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Define your template array for the hidden button
    templates = ["template_plain.png", "reacted_to_templet.png", "template_message.png", "reacted_to_templet.png"]
    threshold = 0.8
    hover_position = None

    # Loop through each template to find a match
    for template_path in templates:
        template = cv2.imread(template_path, 0)
        result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            top_left = max_loc
            h, w = template.shape
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            hover_position = (center_x, center_y)
            break  # Exit the loop on first match

    if hover_position:
        # Step 6: Move the mouse to hover and click
        pyautogui.moveTo(hover_position[0], hover_position[1], duration=0.5)
        time.sleep(1)  # Wait for hover effect
        pyautogui.click()
        time.sleep(1)  # Wait for hover effect
        pyautogui.click()
        print("Clicked on the menu!")

        # After clicking the menu                       
        time.sleep(5)  # Wait for the menu to open

        # Step 1: Take a screenshot of the menu area
        menu_screenshot = pyautogui.screenshot()
        menu_screenshot.save("menu_screenshot.png")

        # Step 2: Load the menu screenshot and template for matching
        menu_img = cv2.imread("menu_screenshot.png")
        delete_template = cv2.imread("delete_button_template.png", 0)  # Template for the delete button
        gray_menu_img = cv2.cvtColor(menu_img, cv2.COLOR_BGR2GRAY)

        # Image Matching for Delete Button
        result = cv2.matchTemplate(gray_menu_img, delete_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Check if the delete button template was found
        if max_val >= threshold:
            top_left = max_loc
            h, w = delete_template.shape
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2

            # Step 3: Move the mouse to the delete button and click
            pyautogui.moveTo(center_x, center_y, duration=0.5)
            time.sleep(1)  # Wait for hover effect
            pyautogui.click()
            print("Clicked on the Delete Chat button!")

            # After clicking the Delete Chat button
            time.sleep(1)  # Wait for the confirmation popup to appear

            # Step 1: Take a screenshot of the confirmation popup area
            confirmation_screenshot = pyautogui.screenshot()
            confirmation_screenshot.save("confirmation_screenshot.png")

            # Step 2: Load the confirmation screenshot and template for matching
            confirmation_img = cv2.imread("confirmation_screenshot.png")
            confirm_template = cv2.imread("confirm_button_template.png", 0)  # Template for the confirm button
            gray_confirmation_img = cv2.cvtColor(confirmation_img, cv2.COLOR_BGR2GRAY)

            # Image Matching for Confirm Button
            result = cv2.matchTemplate(gray_confirmation_img, confirm_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Check if the confirmation button template was found
            if max_val >= threshold:
                top_left = max_loc
                h, w = confirm_template.shape
                center_x = top_left[0] + w // 2
                center_y = top_left[1] + h // 2

                # Step 3: Move the mouse to the confirm button and click
                pyautogui.moveTo(center_x, center_y, duration=0.5)
                time.sleep(1)  # Wait for hover effect
                pyautogui.click()
                print("Clicked on the confirmation button!")
            else:
                print("Confirmation button template not found.")
        else:
            print("Delete button template not found.")
    else:
        print("No matching template found.")

finally:
    time.sleep(15)
    driver.quit()  # Close the browser
