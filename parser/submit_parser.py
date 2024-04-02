from all_imports import *
from scorm_abs import ScormScraperABC

class submit_parser(ScormScraperABC):
    def parser(self, driver):
        self.submit_button.click()
        time.sleep(5)
        try:
            alert = Alert(driver)
            alert.accept()
        except NoAlertPresentException as e:
            print("No alert present")
        except UnexpectedAlertPresentException as e:
            print("Unexpected alert present")

    def validate(self, driver):
        self.submit_button = ''
        flag = False
        try:
            self.submit_button = driver.find_element(By.CSS_SELECTOR, "button.dki-submit-button")
        except NoSuchElementException as e:
            print("No such submit button element")
        if self.submit_button:
            flag = True
        return flag