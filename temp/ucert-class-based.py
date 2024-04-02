from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException, UnexpectedAlertPresentException
import time, json, os, re

class ScormScraper():
    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.flag = False
        self.title_value = ""
        self.class_values = []
        self.count = 1
    
    
    def login(self):
        self.driver.get("https://icert.puresafety.com/Ondemand/Home")
        # Fill in the login form and submit it
        username_field = self.driver.find_element(By.ID, 'LoginName')
        username_field.send_keys("hazwoperosha3")
        password_field = self.driver.find_element(By.ID, 'Password')
        password_field.send_keys("Zahabia1!")
        password_field.send_keys(Keys.RETURN)
        WebDriverWait(driver=self.driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        self.flag = True
    

    def get_div_title_val(self):
        if not self.flag:
            self.login()
        self.driver.get("https://icert.puresafety.com/Home/Dashboard")
        WebDriverWait(driver=self.driver, timeout=20).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        # loop while loading div is there
        while True:
            try:
                loading_div = self.driver.find_element(By.CSS_SELECTOR, 'div.x-mask-loading')
                time.sleep(3)
            except NoSuchElementException:
                break
        time.sleep(10)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        # Get a tag in td with class "xgrid3-cell-first"
        # Get the href attribute of the a tag
        td_list = soup.find_all("td", class_="x-grid3-cell-first")
        a_list = []
        for td in td_list:
            a_list.append(td.find('a'))
        # filter None from a_list
        a_list = list(filter(None, a_list))
        elem = a_list[1]
        print("elem", a_list)
        title_value = elem.get('title')
        class_values = elem.get('class')
        reg = r'[<|>|||:|"|/|\\|?|*]'
        self.title_value_f = re.sub(reg, '-', title_value)
        # for title_value in title_values:
        os.mkdir(self.title_value_f)
        self.title_value = title_value
        self.class_values = class_values
    
    
    # switch to iframe
    def switch_to_iframe(self):
        # find the element with the corresponding title using an XPath expression
        element = self.driver.find_element(By.XPATH, f"//a[contains(@title, '{self.title_value}')]").click()
        WebDriverWait(driver=self.driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        while True:
            try:
                time.sleep(15)
                self.driver.switch_to.window(self.driver.window_handles[1])
                break
            except IndexError as e:
                print("IndexError", e)
                self.driver.refresh()

        iframe = self.driver.find_element(By.ID, 'scormdriver_content')
        self.driver.switch_to.frame(iframe)
    
    
    # question-div content
    def get_quiz_div_content(self, quiz_div):
        if quiz_div:
            radio_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//div[contains(@class, "current")]//input[@type="radio" and @value="Option1"]'))  # Replace with the actual ID of the radio button
            )
            print("Here", radio_button)
            self.driver.execute_script("arguments[0].click();", radio_button)
            time.sleep(5)
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "div.current button.dki-submit-button")  # Replace with the actual ID of the submit button
            submit_button.click()
            time.sleep(5)
            try:
                close_button = self.driver.find_element(By.CSS_SELECTOR, "div.current button[aria-label='Close']")
                self.driver.execute_script("arguments[0].click();", close_button)
            except NoSuchElementException as e:
                print("No such button element")
    
    
    # get hotspot-dki-element
    def get_hotspot_dki_element(self, hotspot_dki_element):
        if len(hotspot_dki_element) > 0:
            for hotspot_div in hotspot_dki_element:
                self.driver.execute_script("arguments[0].click();", hotspot_div)
                time.sleep(3)
                try:
                    cross_buttons = self.driver.find_elements(By.CSS_SELECTOR, "div.current div[data-text='cross_circle'] img")
                    print("cross_buttons", cross_buttons)
                    for cross_button in cross_buttons:
                        self.driver.execute_script("arguments[0].click();", cross_button)
                        time.sleep(2)
                except NoSuchElementException as e:
                    print("No such cross button element")
    
    
    # get true-false-div
    def get_true_false_div(self, true_false_div):
        if true_false_div:
            question_text = true_false_div.text.lower()
            print("question_text", question_text)
            if "true" in question_text and "false" in question_text:
                # find all divs with class "dki-fillBlanksOption-element"
                try:
                    input_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.current div.dki-fillBlanksOption-element input")
                    for input_div in input_divs:
                        input_div.click()
                        time.sleep(2)
                        input_div.send_keys("true")
                        time.sleep(2)
                    # click on submit button
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, "div.current button.dki-submit-button")
                    self.driver.execute_script("arguments[0].click();", submit_button)
                    time.sleep(5)
                except NoSuchElementException as e:
                    print("No such input div element")
    
    
    def click_exit(self, exit_button):
        if exit_button:
            self.driver.execute_script("arguments[0].click();", exit_button)
            print("Exit button clicked")
            time.sleep(5)
    
    
    # get scorm content
    def get_scorm_content(self):
        while True:
            print(f"Scraping page {self.count}...")
            # Use BeautifulSoup to parse the contents of the iframe
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            quiz_div = ''
            hotspot_dki_element = ''
            true_false_div = ''
            next_button = ''
            exit_button = ''
            try:
                quiz_div = self.driver.find_element(By.CSS_SELECTOR, "div.current div.question-option-style-default")
                print("quiz_div", quiz_div)
                self.get_quiz_div_content(quiz_div)
                time.sleep(3)
            except NoSuchElementException as e:
                print("No such question div element")
            try:
                hotspot_dki_element = self.driver.find_elements(By.CSS_SELECTOR, "div.current div.dki-hotspot-element div.dki-element-content")
                print("hotspot_dki_element", hotspot_dki_element)
                self.get_hotspot_dki_element(hotspot_dki_element)
                time.sleep(3)
            except NoSuchElementException as e:
                print("No such hotspot dki element")
            try:
                true_false_div = self.driver.find_element(By.CSS_SELECTOR, "div.current div.questionBody")
                print("true_false_div", true_false_div)
                self.get_true_false_div(true_false_div)
                time.sleep(3)
            except NoSuchElementException as e:
                print("No such true-false div element")
            try:
                exit_button = self.driver.find_element(By.XPATH, "//div[contains(@class, 'current')]//div[@data-title='Exit Button']//a")
                print("exit_button", exit_button)
                self.click_exit(exit_button)
                time.sleep(3)
                break
            except NoSuchElementException as e:
                print("No such next button element")

            with open(f"{self.title_value_f}/page_{self.count}.html", "w", encoding="utf-8") as f:
                f.write(str(soup))
            try:
                next_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'forwardButton')))
                self.driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)
            except (TimeoutException, StaleElementReferenceException) as e:
                print("No such next button element, timed out")
            self.count += 1

        print("Scraping complete!")
    
    # main function
    def main(self):
        self.login()
        time.sleep(5)
        self.get_div_title_val()
        time.sleep(5)
        self.switch_to_iframe()
        time.sleep(5)
        self.get_scorm_content()
        time.sleep(5)
        self.driver.quit()

# run main
if __name__ == "__main__":
    obj = ScormScraper()
    obj.main()