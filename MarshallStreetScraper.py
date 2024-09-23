import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set pandas option to display all rows

# URL of the page to scrape
url = "https://www.marshallstreetdiscgolf.com/flightguide"

# Send a GET request to fetch the page content
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Create an empty list to store disc data
disc_data = []

# Find all div elements with the class 'disc-item' which contain flight numbers for drivers and midranges
discs = soup.find_all('div', class_='disc-item')

# Loop through each disc element and extract the relevant data
for disc in discs:
    disc_name = disc['data-title']  # Extract disc name from data-title attribute
    speed = disc['data-speed']      # Extract speed from data-speed attribute
    glide = disc['data-glide']      # Extract glide from data-glide attribute
    turn = disc['data-turn']        # Extract turn from data-turn attribute
    fade = disc['data-fade']        # Extract fade from data-fade attribute

    # Append the extracted data to the disc_data list
    disc_data.append([disc_name, speed, glide, turn, fade])  # No brand for drivers

# Find all div elements with the class 'putter-child pc-entry' which contain flight numbers for putters
putters = soup.find_all('div', class_='putter-child pc-entry')

# Loop through each putter element and extract the relevant data
for putter in putters:
    putter_name = putter['data-putter']  # Extract putter name
    speed = putter['data-speed']         # Extract speed from data-speed attribute
    glide = putter['data-glide']         # Extract glide from data-glide attribute
    turn = putter['data-turn']           # Extract turn from data-turn attribute
    fade = putter['data-fade']           # Extract fade from data-fade attribute

    # Append the extracted data to the disc_data list
    disc_data.append([putter_name, speed, glide, turn, fade])

# Create a DataFrame to organize the data, adding a 'Brand' column for both discs and putters
df = pd.DataFrame(disc_data, columns=['Disc Name', 'Speed', 'Glide', 'Turn', 'Fade'])

# Save the DataFrame to a CSV file
df.to_csv('marshall_street_flight_numbers.csv', index=False)

# Display the DataFrame
print(df)
