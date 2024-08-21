import requests
import sqlite3
import pandas as pd
from io import StringIO

# URL of the CSV file
url = 'https://www.pdga.com/technical-standards/equipment-certification/discs/export'

# Download the CSV file
response = requests.get(url)
csv_data = response.content.decode('utf-8')

# Read the CSV data into a DataFrame
df = pd.read_csv(StringIO(csv_data))

# Print column headers to identify correct column names
print("Column headers:", df.columns.tolist())

# Select only the "Manufacturer / Distributor", "Disc Model", and "Approved Date" columns
df_select = df[['Manufacturer / Distributor', 'Disc Model', 'Approved Date']]

# Connect to SQLite database (or create it if it doesn't exist)
db_path = 'discs.db'
conn = sqlite3.connect(db_path)

# Export the selected DataFrame to SQLite database
df_select.to_sql('discs', conn, if_exists='replace', index=False)

# Verify the data was loaded correctly
query = "SELECT * FROM discs LIMIT 5"
result = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Display the result
print(result)
