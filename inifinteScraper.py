from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import csv

# Path to ChromeDriver installed via Homebrew
CHROME_DRIVER_PATH = '/opt/homebrew/bin/chromedriver'

# Initialize the WebDriver with the correct path
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

# Load the webpage
driver.get('https://www.marshallstreetdiscgolf.com/flightguide')

# Wait for the page to fully load
time.sleep(5)  # Adjust the sleep time if necessary for the page to load completely

# Get the page source after JS has executed
html = driver.page_source

# Parse the content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all divs that represent individual discs
discs = []

# Each disc is inside a div with the class 'disc-item'
for disc_div in soup.find_all('div', class_='disc-item'):
    disc_name = disc_div['data-title']
    speed = disc_div['data-speed']
    glide = disc_div['data-glide']
    turn = disc_div['data-turn']
    fade = disc_div['data-fade']

    discs.append({
        'name': disc_name,
        'speed': speed,
        'glide': glide,
        'turn': turn,
        'fade': fade
    })

# Close the browser
driver.quit()

# Define the CSV file name
csv_file = 'discs_flight_numbers.csv'

# Write data to CSV
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['name', 'speed', 'glide', 'turn', 'fade'])
    writer.writeheader()
    writer.writerows(discs)

print(f"Data has been saved to {csv_file}")
