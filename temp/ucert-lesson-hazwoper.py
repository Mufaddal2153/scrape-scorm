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

# find element by a link title
# title_values = [i.get('title') for i in a_list if i.get('title') is not None]
# print(title_values)

title_value = a_list[1].get('title')
reg = r'[<|>|||:|"|/|\\|?|*]'
title_value_f = re.sub(reg, '-', title_value)

# for title_value in title_values:
os.mkdir(title_value_f)

# find the element with the corresponding title using an XPath expression
element = driver.find_element(By.XPATH, f"//a[contains(@title, '{title_value}')]").click()
time.sleep(15)
driver.switch_to.window(driver.window_handles[1])

WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
time.sleep(10)
iframe = driver.find_element(By.ID, 'scormdriver_content')
driver.switch_to.frame(iframe)

count = 1
time.sleep(5)
while True:
    print(f"Scraping page {count}...")
    # Use BeautifulSoup to parse the contents of the iframe
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # save html to file
    try:
        time.sleep(5)
        question_div = driver.find_element(By.CLASS_NAME, "question-option-style-default")
        if question_div:
            radio_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//div[contains(@class, "current")]//input[@type="radio" and @value="Option1"]'))  # Replace with the actual ID of the radio button
            )
            print("Here", radio_button)
            driver.execute_script("arguments[0].click();", radio_button)

            submit_button = driver.find_element(By.CLASS_NAME, "dki-submit-button")  # Replace with the actual ID of the submit button
            submit_button.click()
            time.sleep(5)
            try:
                close_button = driver.find_element(By.CSS_SELECTOR, "div.current button[aria-label='Close']")
                driver.execute_script("arguments[0].click();", close_button)
            except NoSuchElementException as e:
                print("No such button element")
    except NoSuchElementException as e:
        print("No such question div element")
    except (TimeoutException, StaleElementReferenceException) as e:
        pass
    
    # click on divs with class "dki-hotspot-element" if exists in current page
    while True:
        try:
            hotspot_divs = driver.find_elements(By.CSS_SELECTOR, "div.current div.dki-hotspot-element div.dki-element-content")
            # if div with class "dki-hotspot-element" exists, click on it
            print("hotspot_divs", hotspot_divs)
            for hotspot_div in hotspot_divs:
                driver.execute_script("arguments[0].click();", hotspot_div)
                time.sleep(3)
                try:
                    cross_buttons = driver.find_elements(By.CSS_SELECTOR, "div.current div[data-text='cross_circle'] img")
                    print("cross_buttons", cross_buttons)
                    for cross_button in cross_buttons:
                        driver.execute_script("arguments[0].click();", cross_button)
                        time.sleep(2)
                    
                except NoSuchElementException as e:
                    print("No such cross button element")
            break
        except (TimeoutException, StaleElementReferenceException) as e:
            pass
        except NoSuchElementException as e:
            print("No such hotspot div element")
            break
    
    # find whether true or false text is present in questionBody div
    try:
        question_body = driver.find_element(By.CSS_SELECTOR, "div.current div.questionBody")
        if question_body:
            question_text = question_body.text.lower()
            print("question_text", question_text)
            if "true" in question_text and "false" in question_text:
                # find all divs with class "dki-fillBlanksOption-element"
                try:
                    input_divs = driver.find_elements(By.CSS_SELECTOR, "div.current div.dki-fillBlanksOption-element input")
                    for input_div in input_divs:
                        input_div.click()
                        time.sleep(2)
                        input_div.send_keys("true")
                        time.sleep(2)
                    # click on submit button
                    submit_button = driver.find_element(By.CSS_SELECTOR, "div.current button.dki-submit-button")
                    driver.execute_script("arguments[0].click();", submit_button)
                    time.sleep(5)
                except NoSuchElementException as e:
                    print("No such input div element")
    except NoSuchElementException as e:
        print("No such true/false question body element")

    with open(f"{title_value_f}/page_{count}.html", "w", encoding="utf-8") as f:
        f.write(str(soup))

    # Locate the "Next" button element using Selenium and wait for it to become clickable
    while True:
        try:
            button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'forwardButton')))
            # button.click() # Click on the button once it is clickable
            driver.execute_script("arguments[0].click();", button)
            break # Exit the loop once the button is clicked
        except (TimeoutException, StaleElementReferenceException):
            print("error") # Keep retrying if the button is not clickable yet

    count += 1
    # Wait for the next page to load
    time.sleep(20)
    try:
        exit_button = driver.find_element(By.XPATH, "//div[contains(@class, 'current')]//div[@data-title='Exit Button']//a")
        driver.execute_script("arguments[0].click();", exit_button)
        print("Exit button clicked")
        time.sleep(5)
        break
    except NoSuchElementException as e:
        print("No such exit button element")
# Switch back to the default content
time.sleep(20)