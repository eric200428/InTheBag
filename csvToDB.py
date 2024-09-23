import sqlite3
import csv


def csv_to_db(csv_file):
    # Path to your SQLite database
    db_path = 'discs.db'

    # Path to your CSV file
    csv_path = csv_file

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Open the CSV file and update the database with new flight numbers
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Assuming the CSV has a column named 'Disc Model'
            model_name = row.get('name')

            if model_name:
                # Check if the disc exists in the database
                cursor.execute('SELECT model FROM discs WHERE model = ?', (model_name,))
                result = cursor.fetchone()

                if result:
                    # If the disc exists, update its flight numbers
                    cursor.execute('''
                        UPDATE discs
                        SET speed = ?, glide = ?, turn = ?, fade = ?
                        WHERE model = ?
                    ''', (row.get('speed'), row.get('glide'), row.get('turn'), row.get('fade'), model_name))
                    print(f"Updated flight numbers for {model_name}.")
                else:
                    print(f"Disc {model_name} not found in the database.")
            else:
                print("Model name not found in the CSV row.")

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print("Database update completed.")
