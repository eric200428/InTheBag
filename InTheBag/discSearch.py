import sqlite3
import tkinter as tk
from tkinter import messagebox, Scrollbar

# A dictionary to track the state of each disc (whether showing name or details)
flipped_discs = {}

def truncate_text(text, max_length=15):
    """
    Truncate text to fit within a circle, adding ellipsis if too long.
    """
    return (text[:max_length] + '...') if len(text) > max_length else text

def flip_disc(event, canvas, disc_id, disc_info, showing_name):
    """
    Flip the disc circle to show either its name or its detailed info.
    """
    if showing_name:
        # Flip to show details (speed, glide, turn, fade)
        canvas.itemconfig(disc_id, text=f"Spd: {disc_info[2]}\n"
                                        f"Gld: {disc_info[3]}\n"
                                        f"Trn: {disc_info[4]}\n"
                                        f"Fde: {disc_info[5]}")
        flipped_discs[disc_id] = False  # Update the state to showing details
    else:
        # Flip back to show disc name
        disc_name = truncate_text(disc_info[1])
        canvas.itemconfig(disc_id, text=disc_name)
        flipped_discs[disc_id] = True  # Update the state to showing name

def execute_query(event=None):
    """
    Executes the query and displays the discs. Can be triggered by the button or Enter key.
    """
    manufacturer_input = manufacturer_entry.get().strip()
    model_input = model_entry.get().strip()

    if not manufacturer_input and not model_input:
        messagebox.showerror("Input Error", "Either Manufacturer or Model is required.")
        return

    conn = sqlite3.connect('../discs.db')
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

        if manufacturer_input:
            query += " AND manufacturers.manufacturer LIKE ?"
            params.append(f'%{manufacturer_input}%')

        if model_input:
            query += " AND discs.model LIKE ?"
            params.append(f'%{model_input}%')

        query += " ORDER BY manufacturers.manufacturer, discs.model;"

        cursor.execute(query, params)
        results = cursor.fetchall()

        # Clear the canvas before drawing new circles
        canvas.delete("all")
        flipped_discs.clear()  # Clear the flipped state dictionary

        if results:
            # Calculate positions for discs to display them as circles
            x_pos, y_pos = 100, 100  # Adjust initial position
            for index, row in enumerate(results):
                # Draw a larger circle for each disc
                disc_circle = canvas.create_oval(x_pos, y_pos, x_pos+150, y_pos+150, fill="lightblue")

                # Truncate the disc name if it's too long
                disc_name = truncate_text(row[1], max_length=15)

                # Label the disc with the model name using a larger font
                disc_label = canvas.create_text(x_pos+75, y_pos+75, text=disc_name, font=("Arial", 12))

                # Store the initial state (showing name) for each disc
                flipped_discs[disc_label] = True

                # Attach click event to the circle and label
                canvas.tag_bind(disc_circle, "<Button-1>", lambda event, disc_id=disc_label, info=row: flip_disc(event, canvas, disc_id, info, flipped_discs[disc_id]))
                canvas.tag_bind(disc_label, "<Button-1>", lambda event, disc_id=disc_label, info=row: flip_disc(event, canvas, disc_id, info, flipped_discs[disc_id]))

                # Adjust position for the next circle
                x_pos += 200
                if (index + 1) % 4 == 0:  # Adjust layout to 4 discs per row
                    x_pos = 100
                    y_pos += 200

            # Adjust the scroll region to encompass all the discs
            canvas.config(scrollregion=canvas.bbox("all"))
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
root.geometry("1200x900")  # Enlarge the window size

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

# Bind the Enter key to execute_query
root.bind('<Return>', execute_query)

# Execute button
execute_button = tk.Button(root, text="Execute Query", command=execute_query)
execute_button.grid(row=2, column=0, columnspan=2, pady=10)

# Create a frame to hold the canvas and scrollbar
canvas_frame = tk.Frame(root)
canvas_frame.grid(row=3, column=0, columnspan=2)

# Create canvas for displaying discs as circles
canvas = tk.Canvas(canvas_frame, width=1000, height=700)
canvas.grid(row=0, column=0)

# Add a vertical scrollbar linked to the canvas
scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
canvas.config(yscrollcommand=scrollbar.set)

# Enable scrolling inside the canvas by configuring mouse scrolling and scroll region
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Run the application
root.mainloop()
