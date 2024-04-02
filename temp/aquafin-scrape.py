import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def scrape_links(url):
    # Set up Selenium webdriver
    # service = Service('chromedriver.exe')  # Replace with actual path to chromedriver
    driver = webdriver.Edge()
    
    # Initialize the list to store the links
    links = []
    scraped_links = []
    inside_links = []
    # Scrape links from the main page
    driver.get(url)
    elements = driver.find_elements(By.TAG_NAME, 'a')
    for element in elements:
        href = element.get_attribute('href')
        if href:
            links.append(href)
    
    # Scrape links from inside pages
    count = 0
    while True:
        if count >= len(links):
            break
        link = links[count]
        flag = True
        # check if # is in link end
        ch_hash = link.split("/")[-1]
        if '#' in ch_hash:
            if '#' in ch_hash[0]:
                flag = False
        if (flag) and (url in link) and (link not in scraped_links):
            driver.get(link)
            elements = driver.find_elements(By.TAG_NAME, 'a')
            for element in elements:
                href = element.get_attribute('href')
                if href:
                    links.append(href)
            scraped_links.append(link)
            
            scraped_links = list(set(scraped_links))
        count += 1
    
    # Close the webdriver
    driver.quit()
    
    # Remove duplicate links
    links = list(set(links))
    return links

def save_links_to_csv(links, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Links'])
        for link in links:
            writer.writerow([link])

# Usage example
url = 'https://www.theone.com'
links = scrape_links(url)
save_links_to_csv(links, 'theone.csv')