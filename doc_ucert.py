from all_imports import *

class doc_ucert():
    def __init__(self, driver, title_value):
        self.driver = driver
        self.title_value = title_value
    
    def click_done(self):
        element = self.driver.find_element(By.XPATH, f"//a[contains(@title, '{self.title_value}')]").click()
        time.sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # close the new tab
        self.driver.close()
        # switch to the old tab
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(5)
        self.driver.find_element(By.XPATH, "//input[contains(@type, 'submit')]").click()
        time.sleep(15)
        return self.driver