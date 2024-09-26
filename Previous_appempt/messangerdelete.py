from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk

# Create a tkinter window for user input
window = tk.Tk()
window.title("Facebook Message Deleter")
window.geometry("400x200")

# Create labels and entries for username and password
username_label = tk.Label(window, text="Username:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

# Define a function to delete Facebook Messenger chats
def delete_chats(username, password):

    # Edge options
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)

    # Create a webdriver object and specify the path to the msedgedriver.exe file
    driver = webdriver.Edge(options=options)

    # Maximize the window
    driver.maximize_window()

    # Navigate to Facebook login page
    driver.get("https://mbasic.facebook.com/")

    # Find the email and password input elements and send the credentials
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys(username)
    password_input = driver.find_element(By.NAME, "pass")
    password_input.send_keys(password)

    # Find the login button element and click it
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()

    try:
        # Wait until the user is fully logged in by checking for a specific element on the homepage or Messenger
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'messages')]")))
        
        # Navigate to the messenger page
        driver.get("https://mbasic.facebook.com/messages/")
        
        # Wait for the chat list element to appear
        chat_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'bm')]/div")))

        # Find all the chat elements in the chat list
        chats = chat_list.find_elements(By.XPATH, "//div[contains(@class, 'bm')]/div")

        # Loop through each chat element and delete it
        for chat in chats:
            try:
                # Find the "Options" button element and click it
                options_button = chat.find_element(By.XPATH, "//a[@role='button']")
                options_button.click()

                # Find the "Delete" button element and click it
                delete_button = WebDriverWait(chat, 5).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Delete']")))
                delete_button.click()

                # Confirm the deletion
                confirm_delete_button = WebDriverWait(chat, 5).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Delete']")))
                confirm_delete_button.click()

            except Exception as e:
                # Handle any errors during the deletion process
                print("Error deleting chat:", e)

    except Exception as e:
        print("Login failed or Messenger not accessible:", e)

    # Close the browser
    driver.quit()

# Define a function to handle the button click event
def delete_chats_button_clicked():
    username = username_entry.get()
    password = password_entry.get()
    delete_chats(username, password)

# Create a button to initiate the chat deletion process
delete_chats_button = tk.Button(window, text="Delete Chats", command=delete_chats_button_clicked)
delete_chats_button.pack()

# Run the tkinter main loop
window.mainloop()
