import requests
from bs4 import BeautifulSoup
import pandas as pd

# Create empty lists to store data
names = []
emails = []
h6_elements = []
addresses = []

# The URL of the page you want to scrape
for i in range(1, 50):
    url = f'https://profiles.utdallas.edu/browse?page={i}'

    # Send an HTTP GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the links within the specified div
        profile_links = soup.select('div.profiles a')

        # Initialize an empty list to store the links
        links = []

        # Loop through the link elements and extract the href attribute
        for link in profile_links:
            link_url = link['href']
            links.append(link_url)

        # Now 'links' contains all the URLs from the specified div
        for link in links:
            print(link)

            response = requests.get(link)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the div element with the specified class
                name = soup.find('h2', class_='mt-sm-0')
                name = name.get_text(strip=True) if name else None

                contact_info_div = soup.find('div', class_='contact_info')

                # Find the h6 element within the "contact_info" div
                h6_element = contact_info_div.find('h6')
                if h6_element:
                    # Extract text from the div element
                    h6_element = h6_element.get_text()
                else:
                    print("H6 element not found on the page.")

                # Find the email address within the "contact_info" div
                email_element = contact_info_div.find('i', class_='Email address')
                email = email_element.find_next('a').get_text(strip=True) if email_element else None

                # Find the address within the "contact_info" div
                address_element = contact_info_div.find('i', class_='Location')
                address = address_element.find_next('br').get_text(strip=True) if address_element else None

                # Append data to lists
                names.append(name)
                emails.append(email)
                h6_elements.append(h6_element)
                addresses.append(address)

            else:
                print(f"Failed to fetch the page. Status code: {response.status_code}")

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Create a DataFrame from the collected data
data = {'Name': names, 'Email': emails, 'H6 Element': h6_elements, 'Address': addresses}
df = pd.DataFrame(data)

# Export the DataFrame to an Excel file
df.to_excel('profile_data.xlsx', index=False)
