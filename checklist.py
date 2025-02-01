import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup for history
def setup_database():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS operations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operation TEXT,
        result TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_to_history(operation, result):
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO operations (operation, result) VALUES (?, ?)", (operation, result))
    conn.commit()
    conn.close()

# Arithmetic operations with error handling
def perform_operation(operator):
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            result = num1 / num2
        else:
            raise ValueError("Unknown operator.")

        result_label.config(text=f"Result: {result}")
        save_to_history(f"{num1} {operator} {num2}", str(result))

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric inputs.")
    except ZeroDivisionError as e:
        messagebox.showerror("Error", str(e))

# GUI setup
def view_history():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT operation, result FROM operations")
    records = cursor.fetchall()
    conn.close()

    history_window = tk.Toplevel(root)
    history_window.title("Operation History")

    tk.Label(history_window, text="Operation History", font=("Arial", 14, "bold")).pack()

    history_text = tk.Text(history_window, width=40, height=15, state="normal")
    history_text.pack()
    history_text.insert("1.0", "\n".join([f"{op} = {res}" for op, res in records]))
    history_text.config(state="disabled")

# Main application
root = tk.Tk()
root.title("Arithmetic Operations System")

setup_database()

tk.Label(root, text="Enter First Number:").grid(row=0, column=0, padx=10, pady=5)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Enter Second Number:").grid(row=1, column=0, padx=10, pady=5)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=10, pady=5)

frame = tk.Frame(root)
frame.grid(row=2, column=0, columnspan=2, pady=10)

operations = ["+", "-", "*", "/"]
for op in operations:
    tk.Button(frame, text=op, command=lambda o=op: perform_operation(o)).pack(side="left", padx=5)

result_label = tk.Label(root, text="Result: ")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

tk.Button(root, text="View History", command=view_history).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
