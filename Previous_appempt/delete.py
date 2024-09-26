# Import selenium and webdriver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# Edge options
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach",True)

# Edge service
driver = webdriver.Edge(options=options)

# open facebook.com
driver.get("https://www.facebook.com/")

# Log in to your account using your email and password
username = driver.find_element(By.ID, 'email')
username.clear()
username.send_keys('manabjkalita86@gmail.com')

password = driver.find_element(By.ID, 'pass')
password.clear()
password.send_keys('781040')
login = driver.find_element(By.NAME, 'login').click()

# Navigate to messenger page to access the chat list
driver.get('https://www.facebook.com/messages/')

# Find the chat list element
chat_list = driver.find_element(By.ID, "js_1")

# Loop through the chat items and hover over each one
for chat in chat_list.find_elements(By.TAG_NAME, "li"):
    # Create an action chain to hover over the chat item
    action = ActionChains(driver)
    action.move_to_element(chat).perform()
    # Find the ellipsis menu element and click on it
    ellipsis = chat.find_element(By.CSS_SELECTOR, "a[aria-label='Conversation actions']")
    ellipsis.click()
    # Do whatever you want with the menu options
    # For example, you can click on the delete option
    delete = chat.find_element(By.CSS_SELECTOR,"a[aria-label='Delete']")
    delete.click()
