import os
from all_imports import *

driver = webdriver.Edge(executable_path="msedgedriver.exe")

html = """
<div _ngcontent-wtp-c277="" class="answers-list align_right ng-tns-c277-54"><label _ngcontent-wtp-c277="" for="" class="question-count ng-tns-c277-54">QUESTION 1 OF 28</label><h3 _ngcontent-wtp-c277="" class="question-heading ng-tns-c277-54"><span _ngcontent-wtp-c277="" class="question-heading main-question-body ng-tns-c277-54">The words <b>“FUEL OIL”</b> may be used in place of the word “____________” on a placard that is displayed on a cargo tank or portable tank being used to transport fuel oil (not classed as a flammable liquid) by highway.</span><div _ngcontent-wtp-c277="" class="question-image ng-tns-c277-54 ng-trigger ng-trigger-slide"><!----><img _ngcontent-wtp-c277="" class="zoomable-image ng-tns-c277-54" src="" alt="undefined" style="width: 100%;"></div></h3><form _ngcontent-wtp-c277="" novalidate="" style="padding-bottom: 1px; padding-top: 10px;" class="ng-tns-c277-54 ng-untouched ng-pristine ng-invalid"><ul _ngcontent-wtp-c277="" class="wpProQuiz_questionList ng-tns-c277-54"><li _ngcontent-wtp-c277="" class="wpProQuiz_questionListItem answer-list-item ng-tns-c277-54 ng-star-inserted"><label _ngcontent-wtp-c277="" class="ng-tns-c277-54"><input _ngcontent-wtp-c277="" formcontrolname="option" type="radio" class="wpProQuiz_questionInput ng-tns-c277-54 ng-untouched ng-pristine ng-invalid" id="5607"><span _ngcontent-wtp-c277="" class="checkmark ng-tns-c277-54"></span> COMBUSTIBLE  </label></li><li _ngcontent-wtp-c277="" class="wpProQuiz_questionListItem answer-list-item ng-tns-c277-54 ng-star-inserted"><label _ngcontent-wtp-c277="" class="ng-tns-c277-54"><input _ngcontent-wtp-c277="" formcontrolname="option" type="radio" class="wpProQuiz_questionInput ng-tns-c277-54 ng-untouched ng-pristine ng-invalid" id="5605"><span _ngcontent-wtp-c277="" class="checkmark ng-tns-c277-54"></span> FLAMMABLE </label></li><li _ngcontent-wtp-c277="" class="wpProQuiz_questionListItem answer-list-item ng-tns-c277-54 ng-star-inserted"><label _ngcontent-wtp-c277="" class="ng-tns-c277-54"><input _ngcontent-wtp-c277="" formcontrolname="option" type="radio" class="wpProQuiz_questionInput ng-tns-c277-54 ng-untouched ng-pristine ng-invalid" id="5606"><span _ngcontent-wtp-c277="" class="checkmark ng-tns-c277-54"></span> NON-FLAMMABLE </label></li><!----></ul></form><div _ngcontent-wtp-c277="" class="footer-btn align_right ng-tns-c277-54"><button _ngcontent-wtp-c277="" type="button" id="next_quiz" aria-label="Next" class="ng-tns-c277-54 ng-star-inserted">Next</button><!----><!----></div></div>
"""

driver.get("data:text/html;charset=utf-8,{html_content}".format(html_content=html))
time.sleep(5)
question = driver.find_element(By.CLASS_NAME, 'question-heading').text
print(question)
options = driver.find_elements(By.CLASS_NAME, 'answer-list-item')
options_list = []
for option in options:
    option_value = option.text
    option_key = option.find_element(By.TAG_NAME, 'label').get_property("content")
    print(option_key, option_value)
    key, value = option_value.split()[0], " ".join(option_value.split()[1:])
    options_list.append((key, key+") "+value))