from scorm_abs import ScormScraperABC
from all_imports import *

class true_false_parser(ScormScraperABC):
    def parser(self, driver):
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

            
    def validate(self, driver):
        flag = False
        question_div = ''
        try:
            question_div = driver.find_element(By.CSS_SELECTOR, "div.current div.questionBody")
        except NoSuchElementException as e:
            print("No such question div element")
        if question_div:
            question_text = question_div.text.lower()
            print("question_text", question_text)
            if "true" in question_text and "false" in question_text:
                flag = True
        return flag