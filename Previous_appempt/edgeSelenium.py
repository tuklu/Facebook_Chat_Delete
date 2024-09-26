# Import the required modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains # Import the ActionChains class
import tkinter as tk

# Create a tkinter window for user input
window = tk.Tk()
window.title("Facebook Message Deleter")
window.geometry("350x150")

# Create labels and entries for username and password
username_label = tk.Label(window, text="Username:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

# Define a function to login using selenium
def login():
    # Get the user input from the entries
    username = username_entry.get()
    password = password_entry.get()

    # Edge options
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach",True)

    # Edge options
    driver = webdriver.Edge(options=options)

    # Navigate to Facebook login page
    # driver.get("https://www.facebook.com/")
    driver.get("https://mbasic.facebook.com/")


    # Find the email and password input elements and send the credentials
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(username)
    password_input = driver.find_element(By.ID, "pass")
    password_input.send_keys(password)

    # Find the login button element and click it
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()

    # Create another tkinter window for otp input
    otp_window = tk.Toplevel(window)
    otp_window.title("Enter OTP")
    otp_window.geometry("350x150")

    # Make the otp window appear on top of every window
    otp_window.attributes("-topmost", True)

    # Create a label and an entry for otp
    otp_label = tk.Label(otp_window, text="OTP:")
    otp_label.pack()
    otp_entry = tk.Entry(otp_window)
    otp_entry.pack()

    # Define a function to enter the otp and delete messages using selenium
    def enter_otp():
        # Get the user input from the entry
        otp = otp_entry.get()

        # Wait for the otp input element to appear and send the otp
        otp_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "approvals_code")))
        otp_input.send_keys(otp)

        # Find the continue button element and click it
        continue_button = driver.find_element(By.ID, "checkpointSubmitButton")
        continue_button.click()

        # Wait for the save browser button element to appear and click it
        save_browser_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkpointSubmitButton")))
        save_browser_button.click()

        # Navigate to the messenger page
        # driver.get("https://www.facebook.com/messages/t/")
        driver.get("https://mbasic.facebook.com/messages/")

        # Wait for the chat list element to appear
        chat_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "x1n2onr6")))

        # Find all the chat elements in the chat list
        chats = chat_list.find_elements_by_xpath(".//li")

        # Loop through each chat element
        for chat in chats:
            # Create an actions object using ActionChains(driver) and assign it to a variable named actions
            actions = ActionChains(driver)

            # Use actions.moveToElement(chat).perform() to hover over the chat element
            actions.moveToElement(chat).perform()

            # Find the chat menu button element and click it
            chat_menu_button = chat.find_element_by_xpath(".//div[@aria-label='Menu']")
            chat_menu_button.click()

            # Wait for the delete option element to appear and click it
            delete_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Delete']/ancestor::div[@role='menuitem']")))
            delete_option.click()

            # Wait for the delete confirmation button element to appear and click it
            delete_confirmation_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Delete']/ancestor::button")))
            delete_confirmation_button.click()

        # Close the driver and the windows
        driver.quit()
        window.destroy()

    # Create a button to trigger the function when clicked
    enter_otp_button = tk.Button(otp_window, text="Enter OTP", command=enter_otp)
    enter_otp_button.pack()


# Create a button to trigger the function when clicked
login_button = tk.Button(window, text="Login", command=login)
login_button.pack()

# Start the tkinter main loop
window.mainloop()