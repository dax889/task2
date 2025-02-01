import os
import tkinter as tk
from tkinter import messagebox

# Logging functionality
def log_operation(operation, result):
    with open("operation_logs.txt", "a") as log_file:
        log_file.write(f"{operation} = {result}\n")

# Arithmetic operations with error handling
def perform_operation(operator, num1, num2):
    try:
        if operator == "+":
            return num1 + num2
        elif operator == "-":
            return num1 - num2
        elif operator == "*":
            return num1 * num2
        elif operator == "/":
            if num2 == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return num1 / num2
        else:
            raise ValueError("Unknown operator.")
    except Exception as e:
        return str(e)

# Console-based user interface
def console_interface():
    print("Welcome to the Calculator")
    print("Enter 'exit' to quit.")
    while True:
        try:
            input1 = input("Enter the first number (or 'exit' to quit): ")
            if input1.lower() == "exit":
                print("Goodbye!")
                break
            num1 = float(input1)

            operator = input("Enter an operator (+, -, *, /): ")

            input2 = input("Enter the second number: ")
            num2 = float(input2)

            result = perform_operation(operator, num1, num2)

            print(f"Result: {result}")

            log_operation(f"{num1} {operator} {num2}", result)

        except ValueError:
            print("Invalid input. Please enter numeric values.")

# Tkinter-based GUI (Optional)
def gui_interface():
    def calculate():
        try:
            num1 = float(entry1.get())
            num2 = float(entry2.get())
            operator = operator_var.get()
            result = perform_operation(operator, num1, num2)
            result_label.config(text=f"Result: {result}")

            log_operation(f"{num1} {operator} {num2}", result)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric inputs.")

    root = tk.Tk()
    root.title("Calculator")

    tk.Label(root, text="First Number:").grid(row=0, column=0, padx=5, pady=5)
    entry1 = tk.Entry(root)
    entry1.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Second Number:").grid(row=1, column=0, padx=5, pady=5)
    entry2 = tk.Entry(root)
    entry2.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Operator:").grid(row=2, column=0, padx=5, pady=5)
    operator_var = tk.StringVar(value="+")
    tk.OptionMenu(root, operator_var, "+", "-", "*", "/").grid(row=2, column=1, padx=5, pady=5)

    tk.Button(root, text="Calculate", command=calculate).grid(row=3, column=0, columnspan=2, pady=10)

    result_label = tk.Label(root, text="Result: ")
    result_label.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()

# Main
if __name__ == "__main__":
    mode = input("Choose mode: 1 for Console, 2 for GUI: ")
    if mode == "1":
        console_interface()
    elif mode == "2":
        gui_interface()
    else:
        print("Invalid choice. Exiting.")
