import sqlite3
import pandas as pd

# Load the CSV file
csv_path = 'disc-data.csv'
df = pd.read_csv(csv_path)

# Print the column names to verify
print("Columns in the CSV:", df.columns)

# Display the first few rows to inspect
print(df.head())

# Connect to the SQLite database
db_path = 'discs.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


# Function to check if a column exists in a table
def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [info[1] for info in cursor.fetchall()]
    return column_name in columns


# Add new columns for flight numbers if they don't already exist
columns_to_add = ['speed', 'glide', 'turn', 'fade']
for column in columns_to_add:
    if not column_exists(cursor, 'discs', column):
        cursor.execute(f"ALTER TABLE discs ADD COLUMN {column} REAL;")

# Update the database with flight numbers from the CSV
for _, row in df.iterrows():
    mold_name = row['MOLD'].strip()  # Strip whitespace and newlines
    speed = row['SPEED']
    glide = row['GLIDE']
    turn = row['TURN']
    fade = row['FADE']

    # Update the discs table
    cursor.execute("""
        UPDATE discs 
        SET speed = ?, glide = ?, turn = ?, fade = ?
        WHERE Model = ?;
    """, (speed, glide, turn, fade, mold_name))

    # Print out what was just updated
    cursor.execute("SELECT * FROM discs WHERE Model = ?;", (mold_name,))
    updated_row = cursor.fetchone()
    print(f"Updated Row: {updated_row}")

# Commit the changes and close the connection
conn.commit()
conn.close()
