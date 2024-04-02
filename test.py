import os
from bs4 import BeautifulSoup
def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

html_files = os.path.join("scorm_packages", "Active Shooter- Law Enforcement", "page_100.html")
soup = BeautifulSoup(open(html_files), 'html.parser', from_encoding='utf-8')
transcription = soup.find('p', {'id': 'transcript_body'}).get_text()
curr_data = " ".join([i.get_text() for i in soup.find_all('div', class_="dki-element-text")])
print(curr_data)
