import cv2
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

try:
    # Step 1: Visit Messenger and Log In
    driver.get("https://www.facebook.com/messages/t/100015570004872/")

    # Log in
    email_element = driver.find_element(By.ID, "email")
    email_element.send_keys("name@example.com")
    password_element = driver.find_element(By.ID, "pass")
    password_element.send_keys("5password")
    password_element.send_keys(Keys.RETURN)

    # Wait for the Messenger page to fully load
    WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # Wait for the presence of a specific element
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Facebook']"))
    )


    # Unfreeze click at the center of the screen
    pyautogui.click(x=driver.execute_script("return window.innerWidth/2"), y=driver.execute_script("return window.innerHeight/2"))
    time.sleep(1)

    # Press Tab 23 times to focus on the first chat in the list
    for _ in range(23):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB)
        # time.sleep(0.5)  # Optional delay for better navigation

    # Function to find hidden menu button (this only needs to be done once)
    def find_hidden_menu_button():
        screenshot = pyautogui.screenshot()
        screenshot.save("full_screenshot.png")
        img = cv2.imread("full_screenshot.png")
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Template array for hidden buttons
        templates = ["template_plain.png", "reacted_to_templet.png", "template_message.png", "reacted_to_templet.png"]
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
            print("Found hidden menu button.")
            return hover_position
        else:
            print("Hidden menu button not found.")
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

    # Step 1: Get the coordinate for the hidden menu button (once)
    hidden_button_position = find_hidden_menu_button()
    if hidden_button_position is None:
        print("Couldn't find the hidden menu button, exiting.")
    else:
        # Initial click on the first chat (before looping)
        hover_and_click(hidden_button_position)
        time.sleep(1)

        # Start loop to delete all chats
        while True:
            # Step 2: Scan for delete button and click (each loop)
            found_delete_button = scan_for_delete_button()
            if not found_delete_button:
                print("No delete button found, ending loop.")
                break

            # Step 3: Scan for and click the confirmation button (only after delete)
            found_confirmation_button = find_confirmation_button()
            if not found_confirmation_button:
                print("No confirmation button found, exiting.")
                break

            # Wait for deletion to complete
            time.sleep(3)

            # Click on the next chat (reuse hidden button position)
            hover_and_click(hidden_button_position)
            time.sleep(1)

finally:
    print("Yooo.. your all chats have been deleted!")
    driver.quit()
