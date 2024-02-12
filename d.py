import requests

# Direct download link
download_url = "https://drive.google.com/uc?export=download&id=15hGDLhsx8bLgLcIRD5DhYt5iBxnjNF1M"

# Requesting the file
response = requests.get(download_url)

# Saving the file
with open("your_filename.ext", "wb") as file:
    file.write(response.content)
