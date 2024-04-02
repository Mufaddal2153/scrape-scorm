from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException, UnexpectedAlertPresentException
import time, json, os
from llama_index import GPTListIndex, GPTVectorStoreIndex, LLMPredictor, PromptHelper, download_loader, SimpleDirectoryReader, ServiceContext
from langchain import OpenAI
from pathlib import Path
import sys, openai, asyncio




# function to get ans from openAI
def get_ans(prompt):

    os.environ['OPENAI_API_KEY'] = "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"
    openai.api_key = os.environ['OPENAI_API_KEY']

    ans = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Selects the correct option key that corresponds to the best answer for each question. Provide only the letter (A, B, C, etc.) that represents the correct option key, without any additional words."},
            {"role": "user", "content": f"Question: {prompt}."}
        ]
    )
    return ans['choices'][0]['message']['content']


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
time.sleep(10)
# driver.switch_to.window(driver.window_handles[1])
# time.sleep(15)
driver.find_element(By.CLASS_NAME, "start-button").click()
time.sleep(20)

while True:
    try:
        question = driver.find_element(By.CLASS_NAME, "question-header")
        question_text = question.text
        print(question_text)

        # Get the option key and value from li tags
        options = driver.find_elements(By.CSS_SELECTOR, "div.question-body ul.answer-list li.answer-item")
        options_list = []
        for option in options:
            option_value = option.text
            key, value = option_value.split()[0], " ".join(option_value.split()[1:])
            options_list.append((key, key+") "+value))
        
        # print(options_list)

        # make one question with options
        question_options = question_text + "\n" + ".\n".join([option[1] for option in options_list])
        print("question_options", question_options)
        # get ans from openAI
        ans = get_ans(question_options).split(")")[0]
        print("ans", ans)
        # # # find ans key from options_list
        but = driver.find_element(By.XPATH, f"//button[normalize-space()='{ans}']").click()
        time.sleep(20)

    except NoSuchElementException:
        print("No such element")

    # find article tag with 'test-summary-body' class
    try:
        test_body_tag = driver.find_element(By.CSS_SELECTOR, "article.test-summary-body button")
        driver.execute_script("arguments[0].click();", test_body_tag)
        time.sleep(20)
    except NoSuchElementException:
        print("No submit button")



# print(but)

time.sleep(30)