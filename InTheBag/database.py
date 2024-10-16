import sqlite3
import os

# Get the absolute path to the main.py directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'discs.db')  # Path to the database file

def execute_query(manufacturer, model):
    """
    Executes the query to fetch disc data from the database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Prepare the query with optional filtering
        query = """
        SELECT manufacturers.manufacturer, discs.model, discs.speed, discs.glide, discs.turn, discs.fade
        FROM discs
        JOIN manufacturers ON discs.manufacturer_id = manufacturers.manufacturer_id
        WHERE TRUE
        """
        params = []

        if manufacturer:
            query += " AND manufacturers.manufacturer LIKE ?"
            params.append(f'%{manufacturer}%')

        if model:
            query += " AND discs.model LIKE ?"
            params.append(f'%{model}%')

        query += " ORDER BY manufacturers.manufacturer, discs.model;"

        cursor.execute(query, params)
        results = cursor.fetchall()

        return results

    except Exception as e:
        print(f"Database error: {e}")
        return []

    finally:
        cursor.close()
        conn.close()
