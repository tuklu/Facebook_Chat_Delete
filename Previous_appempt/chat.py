from getpass import getpass
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Edge options
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach",True)

#credincials
fb_username = "name@example.com"
fb_password = "Password"

# Edge service
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()),options=options)
driver.get('https://facebook.com/')

# Login
username = driver.find_element(By.ID, 'email').clear()
username = driver.find_element(By.ID, 'email').send_keys(fb_username)
password = driver.find_element(By.ID, 'pass').clear()
password = driver.find_element(By.ID, 'pass').send_keys(fb_password)
login = driver.find_element(By.NAME, 'login').click()


# Navigate to messenger
driver.implicitly_wait(50)

try:
    messenger_icon = driver.find_element(By.XPATH, "(//div)[55]")
    messenger_icon.click()

    messenger_icon = driver.find_element(By.XPATH, "(//span)[19]")
    messenger_icon.click()

    messenger_icon = driver.find_element(By.XPATH, "(//span)[20]")
    messenger_icon.click()

    messenger_icon = driver.find_element(By.XPATH, "(//div)[56]")
    messenger_icon.click()

    messenger_icon = driver.find_element(By.XPATH, "(//div[@aria-label='Messenger'])[1]")
    messenger_icon.click()
    
    messenger_icon = driver.find_element(By.XPATH, "(//*[name()='svg'])[10]")
    messenger_icon.click()

    messenger_icon = driver.find_element(By.XPATH, "(//*[name()='g'][@fill-rule='evenodd'])[3]")
    messenger_icon.click()

    messenger_icon = driver.find_element(By.XPATH, "(//*[name()='path'])[17]")
    messenger_icon.click()
finally:
    # Close the browser
    print("hi")



# See_all = driver.find_element(By.XPATH, "((//a[@role='link'])[46]")
# # See_all.click()
























































































# # Edge service
# driver = webdriver.Edge(options=options)
# driver.get('https://mbasic.facebook.com/')

# # Login
# username = driver.find_element(By.XPATH, '//*[@id="m_login_email"]')
# username.clear()
# username.send_keys('jisnukalita@yahoo.com')

# password = driver.find_element(By.XPATH, '//*[@id="password_input_with_placeholder"]/input')
# password.clear()
# password.send_keys('5m::tFqCntzfrai')

# login = driver.find_element(By.XPATH, '//*[@id="login_form"]/ul/li[3]/input')
# login.click()

# # Click on not now

# not_now = driver.find_element(By.XPATH, '//*[@id="root"]/table/tbody/tr/td/div/div[3]/a')
# not_now.click()

# # Go to the chat page
# messenger = driver.find_element(By.XPATH, '//*[@id="header"]/div/a[3]')
# messenger.click()

# # Click on the chat and click delete

# chat_elements = driver.find_elements(By.CLASS_NAME, "bu ba bv")

# for chat in chat_elements:
#     chat.click()
#     delete_button = driver.find_element(By.ID, "delete")
#     delete_button.click()
#     driver.back()