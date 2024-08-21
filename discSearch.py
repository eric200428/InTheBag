import sqlite3
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, END


def execute_query():
    manufacturer_input = manufacturer_entry.get().strip()
    model_input = model_entry.get().strip()

    if not manufacturer_input and not model_input:
        messagebox.showerror("Input Error", "Either Manufacturer or Model is required.")
        return
    conn = sqlite3.connect('discs.db')
    cursor = conn.cursor()
    try:

        # Prepare the query with optional filtering
        query = "SELECT * FROM discs WHERE TRUE"
        params = []

        if manufacturer_input:
            query += " AND \"Manufacturer\" LIKE ?"
            params.append(f'%{manufacturer_input}%')

        if model_input:
            query += " AND \"Model\" LIKE ?"
            params.append(f'%{model_input}%')

        query += " ORDER BY \"Manufacturer\", \"Model\";"

        cursor.execute(query, params)
        results = cursor.fetchall()

        # Clear the listbox before inserting new results
        result_listbox.delete(0, END)

        if results:
            for row in results:
                result_listbox.insert(END, f"{row[0]} - {row[1]}")
        else:
            messagebox.showinfo("No Results", "No matching records found.")

        conn.commit()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Create the main window
root = tk.Tk()
root.title("Disc Lookup")

# Manufacturer input
manufacturer_label = tk.Label(root, text="Enter Manufacturer:")
manufacturer_label.grid(row=0, column=0, padx=10, pady=10)
manufacturer_entry = tk.Entry(root)
manufacturer_entry.grid(row=0, column=1, padx=10, pady=10)

# Model input
model_label = tk.Label(root, text="Enter Model:")
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
