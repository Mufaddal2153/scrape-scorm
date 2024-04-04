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
        self.driver.get("https://hazwoper-osha.com/login")
        # Fill in the login form and submit it
        username_field = self.driver.find_element(By.ID, 'Login_username')
        username_field.send_keys(self.username)
        password_field = self.driver.find_element(By.ID, 'login_password')
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)
        WebDriverWait(driver=self.driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        self.flag = True
        return self.driver
    

    def click_course(self, driver):
        try:
            driver.get("https://hazwoper-osha.com/my-account/my-courses")
            time.sleep(5)
            lesson_divs = driver.find_elements(By.CLASS_NAME, 'parentDiv')
        except NoSuchElementException as e:
            print("No such course div element")
        return (driver, lesson_divs)
    
    def pass_final_quiz(self, driver, count):
        try:
            driver.find_element(By.ID, 'final-quiz').click()
            time.sleep(3)
            driver.find_elements(By.CLASS_NAME, 'answer-list-item')[0].click()
            time.sleep(2)
            driver.find_element(By.ID, 'finish_quiz').click()
            question = driver.find_element(By.CLASS_NAME, 'question-heading').text
            print(question)
            options = driver.find_elements(By.CLASS_NAME, 'answer-list-item')
            options_list = []
            for option in options:
                option_value = option.text
                option_key = option.find_element(By.TAG_NAME, 'label').get_property("content")
                print("options")
                print(option_key, option_value)
                key, value = option_value.split()[0], " ".join(option_value.split()[1:])
                options_list.append((key, key+") "+value))
        except NoSuchElementException as e:
            print("No such element")
        time.sleep(2)
        try:
            driver.find_element(By.ID, 'continue_course').click()
        except NoSuchElementException as e:
            print("No such continue course element")
        time.sleep(2)
        return driver

    def click_lesson(self, driver, lesson_divs):
        try:
            lesson_links = [lesson_div.find_element(By.TAG_NAME, 'a').get_attribute("href") for lesson_div in lesson_divs]
            print(lesson_links)
            for lesson_link in lesson_links:
                driver.get(lesson_link)
                time.sleep(5)
                print("Lesson Div clicked")
                try:
                    driver.find_element(By.CLASS_NAME, 'learndash-resume-button').click()
                    time.sleep(5)
                    print("Lesson Resumed")
                    while True:
                        try:
                            class_values = driver.find_element(By.CLASS_NAME, 'player-div')
                        except NoSuchElementException as e:
                            print("No such element player-div element found")
                            class_values = None
                        class_values = class_values.get_attribute("class") if class_values else []
                        if "QuizMainDiv" in class_values:
                            print("QuizMainDiv")
                            driver.find_element(By.ID, 'lesson-quiz').click()
                            time.sleep(5)
                            count = driver.find_element(By.CLASS_NAME, 'question-count').text
                            print(count)
                            count = int(count.split()[-1].strip())
                            print(count)
                            driver = self.parse_quiz(driver, count)
                        time.sleep(2)
                        try:
                            driver.find_element(By.ID, 'play_topic_slide').click()
                        except NoSuchElementException as e:
                            print("No such element play topic slide element found")

                        if "QuizMainDiv2" in class_values:
                            print("in QuizMainDiv2")
                            try:
                                driver.find_element(By.ID, 'final-quiz').click()
                                time.sleep(3)
                                count = driver.find_element(By.CLASS_NAME, 'question-count').text
                                print(count)
                                count = int(count.split()[-1].strip())
                                print(count)
                                driver = self.pass_final_quiz(driver, count)
                                break
                            except NoSuchElementException as e:
                                print("No such element next topic slide element found")
                        time.sleep(2)
                except NoSuchElementException as e:
                    print("No such element play topic slide element found")
        except NoSuchElementException as e:
            print("No such course div element")
        return driver

    def parse_quiz(self, driver, count):
        for i in range(count-1):
            try:
                driver.find_elements(By.CLASS_NAME, 'answer-list-item')[0].click()
                time.sleep(2)
                driver.find_element(By.ID, 'next_quiz').click()
            except NoSuchElementException as e:
                print("No such element")
            time.sleep(3)
        try:
            driver.find_elements(By.CLASS_NAME, 'answer-list-item')[0].click()
            time.sleep(2)
            driver.find_element(By.ID, 'finish_quiz').click()
        except NoSuchElementException as e:
            print("No such element")
        time.sleep(2)
        try:
            driver.find_element(By.ID, 'continue_course').click()
        except NoSuchElementException as e:
            print("No such continue course element")
        time.sleep(2)
        return driver

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--u', help='Username for login', required=True)
    parser.add_argument('--p', help='Password for login', required=True)
    args = parser.parse_args()
    print(args)
    obj = main_login(args.u, args.p)
    driver = obj.login()
    time.sleep(5)
    driver, lesson_divs = obj.click_course(driver)
    driver = obj.click_lesson(driver, lesson_divs)
    time.sleep(5)