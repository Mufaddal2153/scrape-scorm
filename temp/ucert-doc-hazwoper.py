from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException, UnexpectedAlertPresentException
import time, json, os, re
# Initialize the web driver and navigate to the login page
driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://icert.puresafety.com/Ondemand/Home")

# Fill in the login form and submit it
username_field = driver.find_element(By.ID, 'LoginName')
username_field.send_keys("hazwoperosha3")
password_field = driver.find_element(By.ID, 'Password')
password_field.send_keys("Zahabia1!")
password_field.send_keys(Keys.RETURN)

WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
error_message = "Incorrect username or password."
errors = driver.find_elements("css selector", ".flash-error")

if any(error_message in e.text for e in errors):
    print("[!] Login failed")
else:
    print("[+] Login successful")


driver.get("https://icert.puresafety.com/Home/Dashboard")
WebDriverWait(driver=driver, timeout=20).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
time.sleep(10)
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

# Get a tag in td with class "xgrid3-cell-first"
# Get the href attribute of the a tag
td_list = soup.find_all("td", class_="x-grid3-cell-first")

a_list = []
for td in td_list:
    a_list.append(td.find('a'))

# filter None from a_list
a_list = list(filter(None, a_list))

title_value = a_list[1].get('title')

element = driver.find_element(By.XPATH, f"//a[contains(@title, '{title_value}')]").click()
time.sleep(2)
driver.switch_to.window(driver.window_handles[-1])
# close the new tab
driver.close()
# switch to the old tab
driver.switch_to.window(driver.window_handles[0])
time.sleep(5)
driver.find_element(By.XPATH, "//input[contains(@type, 'submit')]").click()
time.sleep(15)