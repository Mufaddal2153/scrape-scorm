from all_imports import *
from scorm_abs import ScormScraperABC

class flip_card_parser(ScormScraperABC):
    def parser(self, driver):
        try:
            for i in self.flip_card_div:
                driver.execute_script("arguments[0].click();", i)
                time.sleep(2)
                try:
                    alert = Alert(driver)
                    alert.accept()
                except NoAlertPresentException as e:
                    print("No alert present")
        except (TimeoutException, StaleElementReferenceException) as e:
            print("No such next button element, timed out")
        except NoSuchElementException as e:
            print("No such flip card div element")
    def validate(self, driver):
        flag = False
        self.flip_card_div = []
        try:
            self.flip_card_div = driver.find_elements(By.CSS_SELECTOR, "div.current div.flipCardPanel img")
        except NoSuchElementException as e:
            print("No such flip card div element")
        if self.flip_card_div:
            flag = True
        return flag