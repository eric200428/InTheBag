from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import sqlite3
from concurrent.futures import ThreadPoolExecutor

# Configure Selenium to use a headless browser
options = Options()
options.headless = True  # Change to True to run in headless mode

# There is too much going on in this file, scrapingm creating DB, adding records to the DB.
# try to Follow the SOLID principals
# create a file to just scrape the pages
# create a file to do the DB stuff
# create a class called disc that will get from the scraper and can be used in the DB 
# use main to get records from the scraper and add to the DB
# main..
# while disc =  sraper.getNextDisc!= null
#    disc = 
#    DB.insert(disc)




def get_discs_from_page(page_number):
    url = f"https://www.pdga.com/technical-standards/equipment-certification/discs?page={page_number}"
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # Wait until the table is loaded
    try:
        WebDriverWait(driver, 20).until(  # Increased timeout to 20 seconds
            ec.presence_of_element_located((By.CLASS_NAME, 'views-table'))
        )
    except Exception as e:
        print(f"Timeout or error waiting for page {page_number}: {e}")
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    discs = []
    # Find the table containing the discs
    table = soup.find('table', {'class': 'views-table'})
    if not table:
        print(f"No table found on page {page_number}")
        return discs

    # Iterate over the rows in the table (excluding the header row)
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            manufacturer = cols[0].text.strip()
            model = cols[1].text.strip()
            discs.append((manufacturer, model))

    return discs


# Function to scrape a range of pages in parallel
def scrape_pages(start, end):
    all_discs = []
    # Adjust the number of workers based on your system capabilities
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(get_discs_from_page, range(start, end + 1))
        for result in results:
            all_discs.extend(result)
    return all_discs


# Test single page first
test_page = get_discs_from_page(0)
print(f"Test page result: {test_page}")

# Scrape all pages from 0 to 51 in parallel
all_discs = scrape_pages(0, 51)

# Create a SQLite database and table
conn = sqlite3.connect('discs.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS discs (
        id INTEGER PRIMARY KEY,
        manufacturer TEXT,
        model TEXT,
        UNIQUE(manufacturer, model)  -- Add unique constraint to prevent duplicates
    )
''')

# Insert the scraped data into the database
for manufacturer, model in all_discs:
    try:
        c.execute('INSERT INTO discs (manufacturer, model) VALUES (?, ?)', (manufacturer, model))
    except sqlite3.IntegrityError:
        # Ignore duplicate entries
        print(f"Duplicate entry found for {manufacturer} - {model}, skipping...")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data saved to discs.db")
