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
import secure_store
import login
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

def init_driver_with_existing_session():
    # Initialize Edge WebDriver
    profile_path="C:/Users/jisnu/AppData/Local/Microsoft/Edge/User Data"
    profile_name="Default"
    options = Options()
    options.add_argument(f"user-data-dir={profile_path}")  
    options.add_argument(f"profile-directory={profile_name}")
    options.add_argument("--disable-infobars")
    options.binary_location = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
    options.add_argument("--start-maximized")
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    
    return driver

# Function to check if we landed on messenger safely
def wait_for_page_load(driver, timeout=30):
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

# Functon to load cookies
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
def scan_for_delete_button(driver, refresh=False):
    """
    - Attempts to find the delete button. 
    - If not found, checks for the no chat template.
    - If no chats are found, exits.
    - If delete button is still not found after a retry (with refresh), it refreshes the page and tries again.
    """
    # Load the delete button template
    delete_button_template = cv2.imread("delete_button_template.png", 0)
    no_chats_template = cv2.imread("conform_delete_button_notfound_template.png", 0)
    
    # Try to find the delete button on the page
    screenshot = pyautogui.screenshot()
    screenshot.save("current_view.png")
    
    img = cv2.imread("current_view.png")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    result = cv2.matchTemplate(gray_img, delete_button_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    
    if max_val >= 0.8:
        print("Delete button found!")
        return True
    else:
        print("Delete button not found.")
        
        # Check if no chats template is matched
        no_chats_result = cv2.matchTemplate(gray_img, no_chats_template, cv2.TM_CCOEFF_NORMED)
        _, max_no_chats_val, _, _ = cv2.minMaxLoc(no_chats_result)
        
        if max_no_chats_val >= 0.8:
            print("No chats left. Exiting.")
            return False
        
        if refresh:
            print("Delete button still not found after retry, refreshing page.")
            driver.refresh()
            wait_for_page_load(driver, timeout=30)
            
            # Recheck for delete button after page refresh
            print("Page refreshed. Rechecking for the delete button.")
            screenshot = pyautogui.screenshot()
            screenshot.save("current_view_after_refresh.png")
            
            img = cv2.imread("current_view_after_refresh.png")
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            result = cv2.matchTemplate(gray_img, delete_button_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            
            if max_val >= 0.8:
                print("Delete button found after refresh!")
                return True
            else:
                print("Delete button still not found after refresh.")
                
                # Check for no chats template again
                no_chats_result = cv2.matchTemplate(gray_img, no_chats_template, cv2.TM_CCOEFF_NORMED)
                _, max_no_chats_val, _, _ = cv2.minMaxLoc(no_chats_result)
                
                if max_no_chats_val >= 0.8:
                    print("No chats left after refresh. Exiting.")
                    return False
                
                print("No chats template not found, retrying delete button scan.")
                return False

        print("Delete button not found, retrying after waiting.")
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

def check_if_all_chats_deleted():
    # Take a screenshot of the current view
    screenshot = pyautogui.screenshot()
    screenshot.save("no_messages_screenshot.png")
    
    # Load the screenshot and the template
    img = cv2.imread("no_messages_screenshot.png")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Load the "no chats" template
    no_chats_template = cv2.imread("conform_delete_button_notfound_template.png", 0)
    
    # Match the screenshot with the template
    result = cv2.matchTemplate(gray_img, no_chats_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    
    # If we get a strong match, that means there are no more chats
    if max_val >= 0.8:
        print("All chats have been deleted. No messages found.")
        return True
    else:
        return False

def delete_all_chats(driver, total_tabs):
    # Check if all chats have already been deleted
    if check_if_all_chats_deleted():
        print("No chats to delete. Exiting.")
        return

    hidden_button_position = find_hidden_menu_button(driver, total_tabs, 70)
    if hidden_button_position is None:
        print("Couldn't find the hidden menu button, exiting.")
        return

    hover_and_click(hidden_button_position)
    time.sleep(1)

    while True:
        found_delete_button = scan_for_delete_button(driver)
        if not found_delete_button:
            # Check if refreshing is needed after the first failure
            found_delete_button = scan_for_delete_button(driver, refresh=True)
            if not found_delete_button:
                print("No delete button found after refreshing. Exiting.")
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

def run_with_login():
    login.main()
    username, password = secure_store.get_credentials()
    driver = init_driver_with_session()
    try:
        login_to_messenger(driver, username, password)
        press_tab(driver)

        # Start chat deletion process
        delete_all_chats(driver)
    finally:
        driver.quit()

def run_on_ecisting():
    os.system("taskkill /f /im msedge.exe")
    driver = init_driver_with_existing_session()
    try:
        driver.get("https://www.facebook.com/messages/")
        wait_for_page_load
        total_tabs = press_tab(driver)

        # Start chat deletion process
        delete_all_chats(driver, total_tabs)
        # time.sleep(40)
    finally:
        driver.quit()


# Main function to handle the overall process
def main():
    print("Choose a method to proceed:")
    print("1. Use cookies")
    print("2. Full login")
    print("3. Use existing session")

    # Taking user input
    choice = input("Enter the number of your choice (1/2/3): ")

    if choice == '1':
        run_with_cookies()
    elif choice == '2':        
        run_with_login()        
        return
    elif choice == '3':
        run_on_ecisting()
    else:
        print("Invalid choice. Please restart and choose 1, 2, or 3.")
        return

    # Print confirmation message
    print("All chats have been deleted!")


    # Print confirmation message
    print("All chats have been deleted!")
    
    # Step 5: Delete the credentials.json file
    # credentials_file = "credentials.json"
    # if os.path.exists(credentials_file):
    #     try:
    #         os.remove(credentials_file)
    #         print(f"{credentials_file} has been deleted.")
    #     except Exception as e:
    #         print(f"Error deleting {credentials_file}: {e}")
    # else:
    #     print(f"{credentials_file} does not exist.")

if __name__ == "__main__":
    main()
