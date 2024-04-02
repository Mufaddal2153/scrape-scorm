from all_imports import *

class test_ucert():
    def __init__(self, driver, title_value):
        self.driver = driver
        self.title_value = title_value
    

    def get_ans(self, prompt):

        os.environ['OPENAI_API_KEY'] = "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"
        openai.api_key = os.environ['OPENAI_API_KEY']

        ans = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # mesages to prompt the model
            messages=[
                {"role":"system", "content": "Act as a HAZWOPER OSHA Standard expert."},
                {"role": "system", "content": "This is a multiple choice question. Select the correct option key that corresponds to the best answer for each question. Provide only the letter (A, B, C, etc.) that represents the correct option key, without any additional words."},
                {"role": "user", "content": f"Question: {prompt}."}
                ]
        )
        return ans['choices'][0]['message']['content']


    def quiz_start(self):
        element = self.driver.find_element(By.XPATH, f"//a[contains(@title, '{self.title_value}')]").click()
        time.sleep(10)
        # driver.switch_to.window(driver.window_handles[1])
        # time.sleep(15)
        self.driver.find_element(By.CLASS_NAME, "start-button").click()
        time.sleep(10)
        return self.attempt()

    def attempt(self):
        while True:
            try:
                question = self.driver.find_element(By.CLASS_NAME, "question-header")
                question_text = question.text
                print(question_text)
                # Get the option key and value from li tags
                options = self.driver.find_elements(By.CSS_SELECTOR, "div.question-body ul.answer-list li.answer-item")
                options_list = []
                for option in options:
                    option_value = option.text
                    key, value = option_value.split()[0], " ".join(option_value.split()[1:])
                    options_list.append((key, key+") "+value))

                # make one question with options
                question_options = question_text + "\n" + ".\n".join([option[1] for option in options_list])
                print("question_options", question_options)
                # get ans from openAI
                ans = self.get_ans(question_options).split(")")[0]
                print("ans", ans)
                # # # find ans key from options_list
                but = self.driver.find_element(By.XPATH, f"//button[normalize-space()='{ans}']").click()
                time.sleep(20)

            except NoSuchElementException:
                print("No such element")

            # find article tag with 'test-summary-body' class
            try:
                test_body_tag = self.driver.find_element(By.CSS_SELECTOR, "article.test-summary-body button")
                self.driver.execute_script("arguments[0].click();", test_body_tag)
                time.sleep(20)
                break
            except NoSuchElementException:
                print("No submit button")
        return self.driver