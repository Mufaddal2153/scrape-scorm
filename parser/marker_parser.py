from scorm_abs import ScormScraperABC
from all_imports import *

class marker_parser(ScormScraperABC):
    def parser(self, driver):
        for marker_div in self.marker_dki_element:
            driver.execute_script("arguments[0].click();", marker_div)
            time.sleep(3)
            try:
                cross_buttons = driver.find_elements(By.CSS_SELECTOR, "div.current div[data-text='cross_circle'] img")
                print("cross_buttons", cross_buttons)
                for cross_button in cross_buttons:
                    driver.execute_script("arguments[0].click();", cross_button)
                    time.sleep(2)
            except NoSuchElementException as e:
                print("No such cross marker button element")
    def validate(self, driver):
        flag = False
        self.marker_dki_element = ''
        try:
            self.marker_dki_element = driver.find_elements(By.CSS_SELECTOR, "div.current div.dki-marker-element i")
        except NoSuchElementException as e:
            print("No such marker div element")
        if len(self.marker_dki_element) > 0:
            flag = True
        return flag