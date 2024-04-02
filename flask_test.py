from flask import Flask, render_template, request, redirect, url_for, flash
from main_login import main_login
import os, importlib, time


app = Flask(__name__)

@app.route('/')
def index():
    return f"<h1> Hello World </h1></br><a href=" + url_for('login') + ">Login</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    scrapers = [i.split('.')[0] for i in os.listdir() if i.endswith('ucert.py')]
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--u', help='Username for login', required=True)
    # parser.add_argument('--p', help='Password for login', required=True)
    # args = parser.parse_args()
    obj = main_login("bob1", "BobMicheal1!")
    driver = obj.login()
    time.sleep(5)
    print("logged in")
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


if __name__ == '__main__':
    app.run(debug=True)