import os
from bs4 import BeautifulSoup

# Define the folder where the HTML files are located
folder_path = 'Access to Medical and Exposure Records for Managers (US)'
# Define the name of the output text file
output_file = 'output.txt'
# Define a set to store the unique text
unique_text_set = set()
# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an HTML file
    if filename.endswith('.html'):
        # Open the file and parse the HTML using BeautifulSoup
        with open(os.path.join(folder_path, filename)) as file:
            soup = BeautifulSoup(file, 'html.parser')
            # Find the transcription_body div and get its text
            transcription = soup.find('p', {'id': 'transcript_body'}).get_text()
            # Check if the transcription is unique and add it to the set
            if transcription not in unique_text_set:
                unique_text_set.add(transcription)
# Write the unique transcriptions to the output file
print('\n\n'.join(list(unique_text_set)))
# with open(folder_path+'\\'+output_file, 'w') as file:
#     file.write('\n\n'.join(list(unique_text_set)))

