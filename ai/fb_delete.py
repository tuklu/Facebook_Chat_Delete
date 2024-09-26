import time
import pyautogui
import cv2
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import secure_store
import login  # Import your login module
import os

# Function to log in to Messenger
def login_to_messenger(driver, username, password):
    driver.get("https://www.facebook.com/messages/")

    # Enter email and password
    email_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_element.send_keys(username)
    password_element = driver.find_element(By.ID, "pass")
    password_element.send_keys(password)
    password_element.send_keys(Keys.RETURN)

    # Wait until Messenger page loads
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Facebook']"))
    )

    # Unfreeze click at the center of the screen
    pyautogui.click(x=driver.execute_script("return window.innerWidth/2"), y=driver.execute_script("return window.innerHeight/2"))
    time.sleep(1)

    # Press Tab 23 times to focus on the first chat in the list
    for _ in range(10):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB)

def find_hidden_menu_button(driver):
    total_tabs = 10  # Start with 14 tabs as per the original code
    max_tabs = 30

    while total_tabs <= max_tabs:
        # Press Tab key
        for _ in range(1):  # Press additional tabs
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB)

        # Take screenshot and process image
        screenshot = pyautogui.screenshot()
        screenshot.save("full_screenshot.png")
        img = cv2.imread("full_screenshot.png")
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Template array for hidden buttons
        templates = ["template_plain.png", "reacted_to_templet.png", "template_message.png", "reacted_to_templet.png","template_rounded_corner_message.png"]
        threshold = 0.8
        hover_position = None

        # Loop through templates and find a match
        for template_path in templates:
            template = cv2.imread(template_path, 0)
            result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                top_left = max_loc
                h, w = template.shape
                center_x = top_left[0] + w // 2
                center_y = top_left[1] + h // 2
                hover_position = (center_x, center_y)
                break

        if hover_position:
            print(f"Found hidden menu button after {total_tabs} Tab presses.")
            return hover_position
        
        total_tabs += 1

    print(f"Hidden menu button not found after {max_tabs} Tab presses.")
    return None

# Function to scan for delete button (this should be done on every loop)
def scan_for_delete_button():
    menu_screenshot = pyautogui.screenshot()
    menu_screenshot.save("menu_screenshot.png")
    menu_img = cv2.imread("menu_screenshot.png")
    delete_template = cv2.imread("delete_button_template.png", 0)
    gray_menu_img = cv2.cvtColor(menu_img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_menu_img, delete_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= 0.8:
        top_left = max_loc
        h, w = delete_template.shape
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        pyautogui.moveTo(center_x, center_y, duration=0)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1) # Making sure that the pop up loads fully
        print("Clicked on the Delete Chat button!")
        return True
    else:
        print("Delete button not found.")
        return False

# Function to scan for confirmation button (this should be done after clicking delete)
def find_confirmation_button():
    confirmation_screenshot = pyautogui.screenshot()
    confirmation_screenshot.save("confirmation_screenshot.png")
    confirmation_img = cv2.imread("confirmation_screenshot.png")
    confirm_template = cv2.imread("confirm_button_template.png", 0)
    gray_confirmation_img = cv2.cvtColor(confirmation_img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_confirmation_img, confirm_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= 0.8:
        top_left = max_loc
        h, w = confirm_template.shape
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        pyautogui.moveTo(center_x, center_y, duration=0)
        time.sleep(1)
        pyautogui.click()
        print("Clicked on the confirmation button!")
        return True
    else:
        print("Confirmation button not found.")
        return False

# Hover and click function (for both hidden button and confirmation)
def hover_and_click(position):
    pyautogui.moveTo(position[0], position[1], duration=0)
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)
    print(f"Clicked at {position}!")

# Function to delete all chats
def delete_all_chats(driver):
    hidden_button_position = find_hidden_menu_button(driver)
    if hidden_button_position is None:
        print("Couldn't find the hidden menu button, exiting.")
        return

    hover_and_click(hidden_button_position)
    time.sleep(1)

    while True:
        found_delete_button = scan_for_delete_button()
        if not found_delete_button:
            print("No delete button found, ending loop.")
            break

        found_confirmation_button = find_confirmation_button()
        if not found_confirmation_button:
            print("No confirmation button found, exiting.")
            break

        time.sleep(3)
        hover_and_click(hidden_button_position)
        time.sleep(1)

# Main function to handle the overall process
def main():
    # Step 1: Collect credentials via login.py GUI and encrypt them
    login.main()  # This will run the login process and store encrypted credentials

    # Ensure that credentials have been saved
    while not os.path.exists('credentials.json'):
        print("Waiting for credentials...")
        time.sleep(1)

    # Step 2: Load the encryption key
    key = secure_store.load_key()

    # Step 3: Load and decrypt the credentials
    username, password = secure_store.load_and_decrypt_credentials(key)

    # Step 4: Initialize WebDriver and log in to Messenger
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

    try:
        login_to_messenger(driver, username, password)
        delete_all_chats(driver)  # Start chat deletion process
    finally:
        # Print confirmation message
        print("All chats have been deleted!")
        
        # Quit the driver
        driver.quit()
        
        # Step 5: Delete the credentials.json file
        credentials_file = "credentials.json"
        if os.path.exists(credentials_file):
            try:
                os.remove(credentials_file)
                print(f"{credentials_file} has been deleted.")
            except Exception as e:
                print(f"Error deleting {credentials_file}: {e}")
        else:
            print(f"{credentials_file} does not exist.")

if __name__ == "__main__":
    main()
