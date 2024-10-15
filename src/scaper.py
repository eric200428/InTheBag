import pandas as pd
import sqlite3
from io import StringIO
import requests

# Download the CSV file (using your URL)
url = 'https://www.pdga.com/technical-standards/equipment-certification/discs/export'
response = requests.get(url)
csv_data = response.content.decode('utf-8')

# Read the CSV data into a DataFrame
df = pd.read_csv(StringIO(csv_data))

# Rename columns
df.rename(columns={
    'Manufacturer / Distributor': 'manufacturer',
    'Disc Model': 'model'
}, inplace=True)

# Select only the renamed columns and the 'Approved Date' column
df_select = df[['manufacturer', 'model', 'Approved Date']]

# Create a new DataFrame for manufacturers with unique IDs
manufacturers_df = df_select[['manufacturer']].drop_duplicates().reset_index(drop=True)
manufacturers_df['manufacturer_id'] = manufacturers_df.index + 1

# Merge the manufacturer IDs back into the original DataFrame
df_merged = pd.merge(df_select, manufacturers_df, on='manufacturer', how='left')

# Remove the 'manufacturer' column, keeping only the 'manufacturer_id'
df_final = df_merged[['manufacturer_id', 'model', 'Approved Date']]

# Connect to SQLite database (or create it if it doesn't exist)
db_path = '../discs.db'
conn = sqlite3.connect(db_path)

# Export the manufacturers DataFrame to SQLite database
manufacturers_df.to_sql('manufacturers', conn, if_exists='replace', index=False)

# Export the final DataFrame (with manufacturer_id) to SQLite database
df_final.to_sql('discs', conn, if_exists='replace', index=False)

# Add new columns for speed, glide, turn, and fade with NULL values
cursor = conn.cursor()
cursor.execute("ALTER TABLE discs ADD COLUMN speed REAL")
cursor.execute("ALTER TABLE discs ADD COLUMN glide REAL")
cursor.execute("ALTER TABLE discs ADD COLUMN turn REAL")
cursor.execute("ALTER TABLE discs ADD COLUMN fade REAL")

# Commit the changes
conn.commit()

# Verify the data and new columns were added correctly
query = "SELECT * FROM discs LIMIT 5"
result = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Display the result
print(result)
