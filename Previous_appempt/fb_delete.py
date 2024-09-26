import time
import pyautogui
import cv2
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import secure_store
# import login
import os
import json

def init_driver_with_session():
    # Initialize Edge WebDriver
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    
    # Navigate to Facebook Messenger
    driver.get("https://www.facebook.com/messages/")
        
    # Now proceed with the automation
    return driver

# Function to check if we landed on messenger safely
def wait_for_page_load(driver, timeout):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Facebook']"))
    )

# Function to send tab key
def press_tab(driver, times=10):
    for _ in range(times):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB)
    time.sleep(0.5)

    total_tabs = times

    return total_tabs

# Functon to load cookiers
def load_cookies(driver, cookie_file):
    # Load cookies from the exported JSON file
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)
    print("cookies inserted")
    driver.refresh()

# Function to log in to Messenger
def login_to_messenger(driver, username, password):
    # Enter email and password
    email_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_element.send_keys(username)
    password_element = driver.find_element(By.ID, "pass")
    password_element.send_keys(password)
    password_element.send_keys(Keys.RETURN)

    # Wait until Messenger page loads
    wait_for_page_load(driver,200)

    # Unfreeze click at the center of the screen
    pyautogui.click(x=driver.execute_script("return window.innerWidth/2"), y=driver.execute_script("return window.innerHeight/2"))
    time.sleep(1)


def find_hidden_menu_button(driver,total_tabs,max_tabs):
    
    while total_tabs <= max_tabs:
        # Press Tab key
        press_tab(driver, 1)
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

def run_with_cookies():
    driver = init_driver_with_session()
    try:
        wait_for_page_load(driver)
        press_tab(driver)
        load_cookies(driver,"cookies.json")

        # Start chat deletion process
        delete_all_chats(driver)
    finally:
        driver.quit()

def run_with_login(username, password):
    login.main()
    driver = init_driver_with_session()
    try:
        login_to_messenger(driver, username, password)
        press_tab(driver)

        # Start chat deletion process
        delete_all_chats(driver)
    finally:
        driver.quit()


# Main function to handle the overall process
def main():
    # Option to choose between cookie-based session or full login
    use_cookies = True  # Set this to False if you want full login
    
    if use_cookies:
        run_with_cookies()
    else:
        # Retrieve the encrypted credentials from your secure store
        # Assuming `secure_store` has a method `get_credentials` which returns (username, password)
        username, password = secure_store.get_credentials()

        if username and password:
            run_with_login(username, password)
        else:
            print("Failed to retrieve or decrypt credentials.")
            return
    
    # Print confirmation message
    print("All chats have been deleted!")
    
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
