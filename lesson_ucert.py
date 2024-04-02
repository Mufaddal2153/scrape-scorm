from all_imports import *

class lesson_ucert():
    def __init__(self, driver, title_value, title_value_f):
        self.driver = driver
        self.flag = False
        self.title_value = title_value
        self.title_value_f = title_value_f
        self.count = 1
    
    def sorted_ls(self, path):
        mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
        return list(sorted(os.listdir(path), key=mtime))


    # switch to iframe
    def switch_to_iframe(self):
        if not os.path.exists("scorm_packages/"+self.title_value_f):
            os.mkdir("scorm_packages/"+self.title_value_f)
        html_files = self.sorted_ls(os.path.join("scorm_packages", self.title_value_f))
        if html_files:
            self.count = int(html_files[-1].split("_")[-1].split(".")[0])
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

        time.sleep(5)
        iframe = self.driver.find_element(By.ID, 'scormdriver_content')
        self.driver.switch_to.frame(iframe)
    
    def click_exit(self, exit_button):
        if exit_button:
            self.driver.execute_script("arguments[0].click();", exit_button)
            print("Exit button clicked")
            time.sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[0])
            return self.driver

    def main(self):
        parser_names = [i.split('.')[0] for i in os.listdir('parser') if i.endswith('.py')]
        time.sleep(2)
        a_tag = self.driver.find_element(By.ID, "navbar_narration")
        class_value = a_tag.get_attribute("class")
        if "toggled" not in class_value:
            a_tag.click()
            print("a_tag clicked")

        while True:
            print(f"Scraping page {self.count}...")
            # Use BeautifulSoup to parse the contents of the iframe
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            # Clicking on Disabler div
            try:
                div_disabler = self.driver.find_element(By.CSS_SELECTOR, "div.disablerWrapper.clickable")
                # print("class", div_disabler.get_attribute("class"))
                # if "clickable" in div_disabler.get_attribute("class"):
                div_disabler = self.driver.find_element(By.CSS_SELECTOR, "div.disablerWrapper.clickable div.disabler-play")
                self.driver.execute_script("arguments[0].click();", div_disabler)
                print("div_disabler clicked")

            except NoSuchElementException as e:
                print("No such div_disabler element")

            for parser_name in parser_names:
                parser_module = importlib.import_module(f'parser.{parser_name}')
                parser_class = getattr(parser_module, parser_name)
                parser_obj = parser_class()
                par_flag = parser_obj.validate(self.driver)
                if par_flag:
                    parser_obj.parser(self.driver)
                    time.sleep(5)
            try:
                exit_button = self.driver.find_element(By.XPATH, "//div[contains(@class, 'current')]//div[@data-title='Exit Button']//a")
                print("exit_button", exit_button)
                break
            except NoSuchElementException as e:
                print("No such next button element")

            while True:    
                try:
                    next_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'forwardButton')))
                    with open(r"scorm_packages/{}/page_{}.html".format(self.title_value_f, self.count), "w", encoding="utf-8") as f:
                        f.write(str(soup))
                    self.driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(3)
                    break
                except (TimeoutException, StaleElementReferenceException) as e:
                    print("No such next button element, timed out")
            self.count += 1
        return self.click_exit(exit_button)
