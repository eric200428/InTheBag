import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

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
    disc_data.append([disc_name, speed, glide, turn, fade])

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

# Create a DataFrame to organize the data
df = pd.DataFrame(disc_data, columns=['Disc Name', 'Speed', 'Glide', 'Turn', 'Fade'])

# Connect to the SQLite database
db_path = '../discs.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Loop through the DataFrame and update the corresponding discs in the database
for index, row in df.iterrows():
    disc_name = row['Disc Name']
    speed = row['Speed']
    glide = row['Glide']
    turn = row['Turn']
    fade = row['Fade']
    
    # Update the corresponding disc in the discs table
    cursor.execute('''
        UPDATE discs
        SET speed = ?, glide = ?, turn = ?, fade = ?
        WHERE model = ?
    ''', (speed, glide, turn, fade, disc_name))

# Commit the changes
conn.commit()

# Verify the update by querying some data
query = "SELECT * FROM discs LIMIT 5"
result = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Display the result to check the data
print(result)
