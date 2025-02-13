import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
import sqlite3
import os

# URL of the page to scrape
url = "https://www.marshallstreetdiscgolf.com/flightguide"

# Send a GET request to fetch the page content
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Create an empty list to store disc data
disc_data = []

# Find all div elements with the class 'disc-item' which contain flight numbers
discs = soup.find_all('div', class_='disc-item')

# Extract data from each disc
for disc in discs:
    if isinstance(disc, Tag):  # Ensure it's a valid tag
        disc_name = disc.get('data-title', 'Unknown')  
        speed = disc.get('data-speed', '0')  
        glide = disc.get('data-glide', '0')  
        turn = disc.get('data-turn', '0')  
        fade = disc.get('data-fade', '0')  

        disc_data.append([disc_name, speed, glide, turn, fade])

# Find all div elements with the class 'putter-child pc-entry' which contain flight numbers for putters
putters = soup.find_all('div', class_='putter-child pc-entry')

# Extract data from each putter
for putter in putters:
    if isinstance(putter, Tag):  # Ensure it's a valid tag
        putter_name = putter.get('data-putter', 'Unknown')  
        speed = putter.get('data-speed', '0')  
        glide = putter.get('data-glide', '0')  
        turn = putter.get('data-turn', '0')  
        fade = putter.get('data-fade', '0')  

        disc_data.append([putter_name, speed, glide, turn, fade])

# Create a DataFrame to organize the data
df = pd.DataFrame(disc_data, columns=['Disc Name', 'Speed', 'Glide', 'Turn', 'Fade'])

# Check if the DataFrame is empty
if df.empty:
    print("No data scraped. Exiting program.")
else:
    # Connect to the SQLite database
    db_path = os.path.abspath("discs.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Update database only if data exists
    for index, row in df.iterrows():
        cursor.execute('''
            UPDATE discs
            SET speed = ?, glide = ?, turn = ?, fade = ?
            WHERE model = ?
        ''', (row['Speed'], row['Glide'], row['Turn'], row['Fade'], row['Disc Name']))

    # Commit and verify update
    conn.commit()

    query = "SELECT * FROM discs LIMIT 5"
    result = pd.read_sql(query, conn)

    # Close the connection
    conn.close()

    # Display the result to check the data
    print(result)
