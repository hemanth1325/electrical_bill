import tkinter as tk
from tkinter import messagebox
import pandas as pd
from fpdf import FPDF

# Load the dataset (Replace with your actual dataset path)
data = pd.read_csv("MOCK_DATA.csv")

# Function to fetch customer details by ID
def fetch_customer_details():
    customer_id = entry_id.get()

    # Convert the ID to string (if necessary) and check if it exists
    if customer_id in data['id'].astype(str).values:
        # Get customer data
        customer_data = data[data['id'].astype(str) == customer_id]
        
        if not customer_data.empty:
            # Safely get the first row
            customer_data = customer_data.iloc[0]

            # Display the fetched details
            label_name.config(text=f"Name: {customer_data['Name']}")
            label_address.config(text=f"Address: {customer_data['Address']}")
            label_due.config(text=f"Due Charge: Rs{customer_data['Due']:.2f}")
        else:
            messagebox.showerror("Error", "No customer data found.")
    else:
        messagebox.showerror("Error", "Customer ID not found")

# Function to calculate the total bill and display it
def calculate_bill():
    customer_id = entry_id.get()
    user_consumption = entry_consumption.get()  # Get user input for consumption

    # Check if the consumption input is valid
    try:
        user_consumption = float(user_consumption)  # Convert consumption input to float
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid consumption value.")
        return

    # Get customer data based on the customer ID
    customer_data = data[data['id'].astype(str) == customer_id].iloc[0]

    # Bill Calculation (Assuming a rate of Rs0.12 per kWh)
    rate_per_kwh = 0.12
    total_consumption_bill = user_consumption * rate_per_kwh
    due_charge = customer_data['Due']
    service_charge = 40

    # Total bill calculation including due charge
    total_bill = total_consumption_bill + due_charge + service_charge

    # Display the total amount to pay
    label_total.config(text=f"Total Amount to Pay: Rs{total_bill:.2f}")

    return total_bill

# Function to generate the electric bill PDF
def generate_pdf():
    customer_id = entry_id.get()
    total_bill = calculate_bill()  # Calculate the total bill

    if total_bill is None:
        return  # If there was an error in bill calculation, exit the function

    # Get customer data based on the customer ID
    customer_data = data[data['id'].astype(str) == customer_id].iloc[0]
    user_consumption = float(entry_consumption.get())  # Get the user input for consumption

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()

    # Draw border
    pdf.set_line_width(1)
    pdf.rect(10, 10, 190, 277)  # x, y, width, height of the border

    # Add content to PDF
    pdf.set_font("Arial", 'B', size=16)  # Bold font for the title
    pdf.cell(200, 10, txt="Electric Bill", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)  # Reset to regular font
    pdf.cell(200, 10, txt=f"Customer ID: {customer_data['id']}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Name: {customer_data['Name']}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Address: {customer_data['Address']}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Consumption: {user_consumption} kWh", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Consumption Charge: Rs{user_consumption * 0.12:.2f}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Due Charge: Rs{customer_data['Due']:.2f}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Total Amount to Pay: Rs{total_bill:.2f}", ln=True, align='C')

    # Save the PDF to a file
    pdf_file = f"Electric_Bill_{customer_data['id']}.pdf"
    pdf.output(pdf_file)

    messagebox.showinfo("Success", f"Bill generated: {pdf_file}")

# Create the GUI window
root = tk.Tk()
root.title("Electric Bill Generator")
root.geometry("600x400")  # Set initial window size
root.minsize(400, 300)  # Minimum size to avoid too small a window
root.configure(bg="#f0f8ff")  # Light blue background

# Create a frame for better layout
frame = tk.Frame(root, bg="#f0f8ff", bd=10, relief=tk.RAISED)
frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame in the window

# Styling
label_font = ("Arial", 12, "bold")
entry_font = ("Arial", 11)
button_font = ("Arial", 11, "bold")

# Labels and entry for Customer ID input
label_id = tk.Label(frame, text="Enter Customer ID:", font=label_font, bg="#f0f8ff", fg="#333")
label_id.grid(row=0, column=0, padx=10, pady=10, sticky='ew', columnspan=3)

entry_id = tk.Entry(frame, font=entry_font, width=30)
entry_id.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

# Button to fetch details
button_fetch = tk.Button(frame, text="Fetch Details", font=button_font, bg="#4682b4", fg="white", command=fetch_customer_details)
button_fetch.grid(row=1, column=2, padx=10, pady=10)

# Labels to display customer details
label_name = tk.Label(frame, text="Name:", font=label_font, bg="#f0f8ff", fg="#333")
label_name.grid(row=2, column=0, padx=10, pady=5, sticky='ew', columnspan=3)

label_address = tk.Label(frame, text="Address:", font=label_font, bg="#f0f8ff", fg="#333")
label_address.grid(row=3, column=0, padx=10, pady=5, sticky='ew', columnspan=3)

label_due = tk.Label(frame, text="Due Charge:", font=label_font, bg="#f0f8ff", fg="#333")
label_due.grid(row=4, column=0, padx=10, pady=5, sticky='ew', columnspan=3)

# Input for the power consumption
label_consumption = tk.Label(frame, text="Enter Power Consumption (kWh):", font=label_font, bg="#f0f8ff", fg="#333")
label_consumption.grid(row=5, column=0, padx=10, pady=10, sticky='ew', columnspan=3)

entry_consumption = tk.Entry(frame, font=entry_font, width=30)
entry_consumption.grid(row=6, column=0, padx=10, pady=5, columnspan=2)

# Button to calculate total bill
button_calculate = tk.Button(frame, text="Calculate Total Bill", font=button_font, bg="#4682b4", fg="white", command=calculate_bill)
button_calculate.grid(row=6, column=2, padx=10, pady=10)

# Label to display total bill
label_total = tk.Label(frame, text="Total Amount to Pay:", font=label_font, bg="#f0f8ff", fg="#333")
label_total.grid(row=7, column=0, padx=10, pady=5, sticky='ew', columnspan=3)

# Button to generate PDF
button_pdf = tk.Button(frame, text="Generate PDF", font=button_font, bg="#4682b4", fg="white", command=generate_pdf)
button_pdf.grid(row=8, column=0, padx=10, pady=10, columnspan=3)

# Run the application
root.mainloop()
