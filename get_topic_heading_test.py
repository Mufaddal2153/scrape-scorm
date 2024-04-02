from bs4 import BeautifulSoup
import os, requests
from io import BytesIO

# soup = BeautifulSoup(open("scorm_packages\Personal Protective Equipment (PPE) Overview for Construction- Using and Maintaining PPE\page_5.html", encoding='utf-8'), 'html.parser')

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))


folder_path = 'scorm_packages'
headers = headers = {
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}
for folder_name in os.listdir(folder_path):
    # Define a set to store the unique text
    unique_text_set = set()
    text_heading = []
    # Loop through all the files in the folder
    html_files = sorted_ls(os.path.join(folder_path, folder_name))
    for filename in html_files:
        # Check if the file is an HTML file
        if filename.endswith('.html'):
            # Open the file and parse the HTML using BeautifulSoup
            # print(filename)
            with open(os.path.join(folder_path, folder_name, filename), encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser', from_encoding='utf-8')
                # Find the transcription_body div and get its text
                transcription = soup.find('p', {'id': 'transcript_body'}).get_text()
                baseUrl = "/".join(soup.find('audio').get('src').split('/')[:-2])
                # Check if the transcription is unique and add it to the set
                if transcription not in unique_text_set:
                    curr_div = soup.find('div', class_='current')
                    img_tags = curr_div.find_all('img')
                    img_src = [baseUrl+"/"+img_tag.get('src') for img_tag in img_tags if img_tag.get('src')]
                    print(folder_name, filename)
                    print(img_src)
                    unique_text_set.add(transcription)
                    for x in soup.find_all('li', {'class': 'dki_course_outline-subeo'}):
                        a_tag = x.find('a', {'class': 'current'})
                        if a_tag:
                            a_tag = a_tag.get_text()
                            text_heading.append((a_tag, transcription))
                            # print(a_tag)

# curr = [y.get_text() for x in soup.find('li', {'class': 'dki_course_outline-object'}) for y in x.find('a', {'class': 'current'})]
# print(curr)

# loop through the divs