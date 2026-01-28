# ⚡ Electric Bill Generator (Python + Tkinter)

This project is a **desktop-based Electric Bill Generator application** built using **Python, Tkinter, Pandas, and FPDF**.  
It allows users to fetch customer details from a CSV file, calculate electricity bills based on power consumption, and generate a **PDF bill**.

---

## 📌 Features

- Fetch customer details using **Customer ID**
- Read customer data from a **CSV file**
- Calculate electricity bill based on consumption
- Includes:
  - Consumption charge
  - Previous due amount
  - Fixed service charge
- Generate and save **Electric Bill as a PDF**
- Simple and user-friendly **Tkinter GUI**

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** – GUI
- **Pandas** – Data handling
- **FPDF** – PDF generation
- **CSV file** – Customer data source

---

## 📁 Project Structure

electric-bill-generator/
│
├── MOCK_DATA.csv
├── electric_bill_generator.py
├── Electric_Bill_<CustomerID>.pdf
└── README.md


---

## 📊 Sample CSV Format (`MOCK_DATA.csv`)

```csv
id,Name,Address,Due
1,John Doe,New York,120.50
2,Jane Smith,California,75.00
3,Alex Brown,Texas,0.00
⚙️ Bill Calculation Logic
Rate per kWh: Rs 0.12

Service Charge: Rs 40

Total Bill =
(Consumption × Rate per kWh)
+ Due Charge
+ Service Charge
🚀 How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/hemanth1325/electrical_bil
2️⃣ Navigate to the Project Folder
cd electric-bill-generator
3️⃣ Install Required Libraries
pip install pandas fpdf
(Tkinter comes pre-installed with Python)

4️⃣ Run the Application
python electric_bill_generator.py
🖥️ Application Workflow
Enter Customer ID

Click Fetch Details

Enter Power Consumption (kWh)

Click Calculate Total Bill

Click Generate PDF

PDF bill is saved in the project folder

📄 Output
Generates a PDF named:

Electric_Bill_<CustomerID>.pdf
PDF contains:

Customer details

Consumption details

Due charges

Final bill amount

📌 Future Enhancements
Input validation improvements

Dynamic tariff slabs

Database integration (MySQL / SQLite)

Payment status tracking

Dark mode UI

👤 Author
Hemanth Sachi
Python Developer | Data & Automation Enthusiast

🔗 GitHub: https://github.com/hemanth1325
