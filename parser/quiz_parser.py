from scorm_abs import ScormScraperABC
from all_imports import *

class quiz_parser(ScormScraperABC):
    def parser(self, driver):
        try:
            radio_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f'//div[contains(@class, "current")]//input[@type="radio" and @value="Option1"]'))  # Replace with the actual ID of the radio button
                )
            print("Here", radio_button)
            driver.execute_script("arguments[0].click();", radio_button)
            time.sleep(5)
            try:
                submit_button = driver.find_element(By.CSS_SELECTOR, "button.dki-submit-button")  # Replace with the actual ID of the submit button
                submit_button.click()
                time.sleep(5)
            except NoSuchElementException as e:
                print("No such submit button element")
            try:
                close_button = driver.find_element(By.CSS_SELECTOR, "div.current button[aria-label='Close']")
                driver.execute_script("arguments[0].click();", close_button)
            except NoSuchElementException as e:
                print("No such button element")
        except (TimeoutException, StaleElementReferenceException) as e:
            print("No such next button element, timed out")

            
    def validate(self, driver):
        flag = False
        quiz_div = ''
        try:
            quiz_div = driver.find_element(By.CSS_SELECTOR, "div.current div.question-option-style-default")
        except NoSuchElementException as e:
            print("No such quiz div element")
        if quiz_div:
            flag = True
        return flag