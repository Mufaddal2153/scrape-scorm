from all_imports import *


class main_login():
    def __init__(self, username, password):
        # self.driver = webdriver.Edge(service=webdriver.edge.service.Service())
        self.driver = webdriver.Edge(executable_path="msedgedriver.exe")
        self.flag = False
        self.title_value = None
        self.class_values = []
        self.title_value_f = None
        self.username = username
        self.password = password
    
    
    def login(self):
        self.driver.maximize_window()
        self.driver.get("https://qa.hazwoper-osha.com/login")
        # Fill in the login form and submit it
        username_field = self.driver.find_element(By.ID, 'Login_username')
        username_field.send_keys(self.username) # hazwoperosha4
        password_field = self.driver.find_element(By.ID, 'login_password')
        password_field.send_keys(self.password) # yaAllah1#@
        password_field.send_keys(Keys.RETURN)
        WebDriverWait(driver=self.driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        self.flag = True
        return self.driver
    

    def click_course(self, driver):
        try:
            driver.get("https://qa.hazwoper-osha.com/my-account/my-courses")
            time.sleep(5)
            course_divs = driver.find_elements(By.CSS_SELECTOR, '.main_content .parentDiv')
        except NoSuchElementException as e:
            print("No such course div element")
        return (driver, course_divs)
    
    def click_lesson(self, driver):
        try:
            driver.get("https://hazwoper-osha.com/lms/player/139")
            time.sleep(5)
        except NoSuchElementException as e:
            print("No such course div element")
            
        return driver

    def get_div_title_val(self, driver):
        if not self.flag:
            self.login()
        reg = r'[<|>|||:|"|/|\\|?|*]'
        self.title_value = None
        while True:
            if self.title_value is not None:
                print(self.title_value, self.class_values)
                self.title_value_f = re.sub(reg, '-', title_value)
                self.title_value_f = self.title_value_f.strip()
                break
            driver.get("https://icert.puresafety.com/Home/Dashboard")
            WebDriverWait(driver=driver, timeout=20).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )
            while True:
                try:
                    loading_div = driver.find_element(By.CSS_SELECTOR, 'div.x-mask-loading')
                    time.sleep(3)
                except NoSuchElementException:
                    break
            time.sleep(5)
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
            elem = a_list[1]
            title_value = elem.get('title')
            class_values = elem.get('class')
            # for title_value in title_values:
            self.title_value = title_value
            self.class_values = class_values
        return driver, self.title_value, self.title_value_f, self.class_values

if __name__ == "__main__":
    # scrapers = [i.split('.')[0] for i in os.listdir() if i.endswith('ucert.py')]
    parser = argparse.ArgumentParser()
    parser.add_argument('--u', help='Username for login', required=True)
    parser.add_argument('--p', help='Password for login', required=True)
    args = parser.parse_args()
    obj = main_login(args.u, args.p)
    driver = obj.login()
    time.sleep(5)
    # driver, course_divs = obj.click_course(driver)
    # course_divs[0].find_element(By.CSS_SELECTOR, 'button').click()
    # time.sleep(5)
    # course_resume = driver.find_elements(By.CSS_SELECTOR, '.learndash-resume-button')
    # course_resume[0].click()
    # time.sleep(5)
    driver = obj.click_lesson(driver)
    time.sleep(5)
    while True:
        class_values = driver.find_element(By.CSS_SELECTOR, 'div#player-div').get('class')
        if "QuizMainDiv" in class_values:
            print("QuizMainDiv")
            driver.find_element(By.CSS_SELECTOR, '#lesson-quiz').click()
            time.sleep(5)
            break
        driver.find_element(By.CSS_SELECTOR, '#play_topic_slide').click()

    time.sleep(5)

    """
    while True:
        driver, title_value, title_value_f, class_values = obj.get_div_title_val(driver)
        print("Driver, title_value, title_value_f, class_values")
        print(driver, title_value, title_value_f, class_values)
        time.sleep(5)
        if "training-ThirdParty" in class_values:
            scraper_mod = importlib.import_module("lesson_ucert")
            scraper_class = getattr(scraper_mod, "lesson_ucert")
            scraper_obj = scraper_class(driver, title_value, title_value_f)
            scraper_obj.switch_to_iframe()
            driver = scraper_obj.main()
        if "training-Test" in class_values:
            scraper_mod = importlib.import_module("test_ucert")
            scraper_class = getattr(scraper_mod, "test_ucert")
            scraper_obj = scraper_class(driver, title_value)
            driver = scraper_obj.quiz_start()
        if "training-Url" in class_values:
            scraper_mod = importlib.import_module("doc_ucert")
            scraper_class = getattr(scraper_mod, "doc_ucert")
            scraper_obj = scraper_class(driver, title_value)
            driver = scraper_obj.click_done()
    """