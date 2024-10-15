import sqlite3
import pandas as pd

DB_NAME = 'disc_data.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS discs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT,
                        Speed INTEGER,
                        Glide INTEGER,
                        Turn INTEGER,
                        Fade INTEGER,
                        Source TEXT,
                        UNIQUE(Name, Speed, Glide, Turn, Fade, Source))''')
    conn.commit()
    conn.close()

def save_to_database(df, source):
    conn = connect_db()
    df['Source'] = source  # Add a column to track the data source (PDGA or Marshall Street)
    
    try:
        # Check for duplicates using 'IGNORE' conflict resolution
        df.to_sql('discs', conn, if_exists='append', index=False, 
                  dtype={'Name': 'TEXT', 'Speed': 'INTEGER', 'Glide': 'INTEGER', 
                         'Turn': 'INTEGER', 'Fade': 'INTEGER', 'Source': 'TEXT'},
                  method='multi')
    except sqlite3.Error as e:
        print(f"Error saving to database: {e}")
    finally:
        conn.close()
        print(f"Data from {source} saved to the database without duplicates.")

