import sqlite3
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, END


def execute_query():
    manufacturer_input = manufacturer_entry.get()
    model_input = model_entry.get()

    if not manufacturer_input:
        messagebox.showerror("Input Error", "Manufacturer is required.")
        return

    try:
        conn = sqlite3.connect('discs.db')
        cursor = conn.cursor()

        with open('discs.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        cursor.executescript(sql_script)

        query = "SELECT * FROM discs WHERE manufacturer LIKE ?"
        params = [f'%{manufacturer_input}%']

        if model_input:
            query += " AND model LIKE ?"
            params.append(f'%{model_input}%')

        query += " ORDER BY manufacturer, model;"

        cursor.execute(query, params)
        results = cursor.fetchall()

        # Clear the listbox
        result_listbox.delete(0, END)

        for row in results:
            result_listbox.insert(END, row)

        conn.commit()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


# Create the main window
root = tk.Tk()
root.title("SQL Query Executor")

# Manufacturer input
manufacturer_label = tk.Label(root, text="Enter Manufacturer:")
manufacturer_label.grid(row=0, column=0, padx=10, pady=10)
manufacturer_entry = tk.Entry(root)
manufacturer_entry.grid(row=0, column=1, padx=10, pady=10)

# Model input
model_label = tk.Label(root, text="Enter Model (optional):")
model_label.grid(row=1, column=0, padx=10, pady=10)
model_entry = tk.Entry(root)
model_entry.grid(row=1, column=1, padx=10, pady=10)

# Execute button
execute_button = tk.Button(root, text="Execute Query", command=execute_query)
execute_button.grid(row=2, column=0, columnspan=2, pady=10)

# Result listbox with a scrollbar
result_listbox = Listbox(root, width=80, height=20)
result_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

scrollbar = Scrollbar(root)
scrollbar.grid(row=3, column=2, sticky='ns')
result_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=result_listbox.yview)

# Run the application
root.mainloop()
