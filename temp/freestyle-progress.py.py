from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
# Initialize the web driver and navigate to the login page
driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://progress.freestylediabetes.co.uk/sign-in")

# Fill in the login form and submit it
username_field = driver.find_element(By.ID, 'loginUsername')
username_field.send_keys("Mai.sallam@abbott.com")
password_field = driver.find_element(By.ID, 'loginPassword')
password_field.send_keys("2$OF#cyNv(MbXSx1")
password_field.send_keys(Keys.RETURN)

WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
error_message = "Incorrect username or password."
errors = driver.find_elements("css selector", ".flash-error")

if any(error_message in e.text for e in errors):
    print("[!] Login failed")
else:
    print("[+] Login successful")

time.sleep(5)
# Wait for the page to load

urls = ["https://progress.freestylediabetes.co.uk/modules/the-importance-of-time-in-range-2", "https://progress.freestylediabetes.co.uk/modules/triangle-of-diabetes", "https://progress.freestylediabetes.co.uk/modules/freestyle-libre-2-glucose-alarms-feature-2", "https://progress.freestylediabetes.co.uk/modules/freestyle-libre-3", "https://progress.freestylediabetes.co.uk/modules/how-the-freestyle-libre-system-works-2", "https://progress.freestylediabetes.co.uk/modules/trend-arrows-and-projected-glucose", "https://progress.freestylediabetes.co.uk/modules/targeting-glucose-variability", "https://progress.freestylediabetes.co.uk/modules/targeting-hypoglycaemia", "https://progress.freestylediabetes.co.uk/modules/the-power-of-glucose-pattern-insights", "https://progress.freestylediabetes.co.uk/modules/making-positive-changes-in-a-diabetes-day", "https://progress.freestylediabetes.co.uk/modules/freestyle-librelink-and-librelinkup", "https://progress.freestylediabetes.co.uk/modules/using-libreview-software", "https://progress.freestylediabetes.co.uk/modules/understanding-and-evaluating-mental-health", "https://progress.freestylediabetes.co.uk/modules/diabetes-pregnancy"]

for i, url in enumerate(urls):
    driver.get(url)
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    name = url.split("/")[-1]
    # Get the page source and parse it with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    # Find all CSS link tags and save them to a list
    css_links = []
    for link in soup.find_all("link"):
        if link.get("rel") == ["stylesheet"]:
            css_links.append(link.get("href"))

    # Find all JS script tags and save them to a list
    js_scripts = []
    for script in soup.find_all("script"):
        if script.get("src"):
            js_scripts.append(script.get("src"))

    # Find the div with a specific class and save its content to a variable
    div_content = soup.find("div", {"id": "module"}).prettify()
    print(i, name)
    # Create a new HTML file and write the scraped data to it
    with open(f"{name}.html", "w", encoding="utf-8") as f:
        f.write("<html>\n<head>\n")
        for css_link in css_links:
            f.write(f'<link rel="stylesheet" href="{css_link}">\n')
        for js_script in js_scripts:
            f.write(f'<script src="{js_script}"></script>\n')
        f.write("</head>\n<body>\n")
        f.write(f"{div_content}\n")
        f.write("</body>\n</html>")

# Close the web driver
driver.quit()
