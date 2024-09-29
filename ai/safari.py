from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.SafariOptions()
driver = webdriver.Safari(options=options)

driver.get("https://google.com/")
time.sleep(15)
title = driver.title
print(title)
driver.implicitly_wait(0.5)

driver.quit()