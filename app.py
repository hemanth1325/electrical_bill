from flask import Flask, request, render_template, make_response, redirect, flash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-bill', methods=['POST'])
def generate_bill():
    customer_id = request.form['customerId']
    customer_name = request.form['customerName']
    address = request.form['address']
    start_date = request.form['startDate']
    end_date = request.form['endDate']
    units_consumed = request.form['unitsConsumed']
    rate_per_unit = request.form['ratePerUnit']
    monthly_service_charge = request.form['monthlyServiceCharge']
    additional_fees = request.form['additionalFees']
    discounts = request.form['discounts']

    # Server-side validation to check if any fields are empty
    if not all([customer_id, customer_name, address, start_date, end_date, units_consumed, rate_per_unit, monthly_service_charge, additional_fees, discounts]):
        flash("All fields are required.", "error")
        return redirect('/')

    # Convert to float and handle invalid number formats
    try:
        units_consumed = float(units_consumed)
        rate_per_unit = float(rate_per_unit)
        monthly_service_charge = float(monthly_service_charge)
        additional_fees = float(additional_fees)
        discounts = float(discounts)
    except ValueError:
        flash("Please enter valid numeric values for units consumed, rate per unit, charges, fees, and discounts.", "error")
        return redirect('/')

    # Calculate total amount
    electricity_charge = units_consumed * rate_per_unit
    total_before_discounts = electricity_charge + monthly_service_charge + additional_fees
    total_amount = total_before_discounts - discounts

    # Render the bill summary page
    return render_template('bill.html', 
                           customer_id=customer_id,
                           customer_name=customer_name, 
                           address=address, 
                           start_date=start_date, 
                           end_date=end_date, 
                           units_consumed=units_consumed, 
                           total_amount=total_amount)

@app.route('/download-bill', methods=['POST'])
def download_bill():
    try:
        customer_id = request.form['customerId']
        customer_name = request.form['customerName']
        address = request.form['address']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        units_consumed = request.form['unitsConsumed']
        rate_per_unit = request.form['ratePerUnit']
        monthly_service_charge = request.form['monthlyServiceCharge']
        additional_fees = request.form['additionalFees']
        discounts = request.form['discounts']

        # Server-side validation again for download request
        if not all([customer_id, customer_name, address, start_date, end_date, units_consumed, rate_per_unit, monthly_service_charge, additional_fees, discounts]):
            flash("All fields are required.", "error")
            return redirect('/')

        # Convert to float
        units_consumed = float(units_consumed)
        rate_per_unit = float(rate_per_unit)
        monthly_service_charge = float(monthly_service_charge)
        additional_fees = float(additional_fees)
        discounts = float(discounts)

        # Calculate total amount
        electricity_charge = units_consumed * rate_per_unit
        total_before_discounts = electricity_charge + monthly_service_charge + additional_fees
        total_amount = total_before_discounts - discounts

        # Create PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        p.drawString(100, height - 50, f"Customer ID: {customer_id}")
        p.drawString(100, height - 70, f"Customer Name: {customer_name}")
        p.drawString(100, height - 90, f"Address: {address}")
        p.drawString(100, height - 110, f"Billing Period: {start_date} to {end_date}")
        p.drawString(100, height - 130, f"Units Consumed: {units_consumed} kWh")
        p.drawString(100, height - 150, f"Total Amount Due: ₹{total_amount:.2f}")

        p.showPage()
        p.save()
        buffer.seek(0)

        # Create response
        pdf_data = buffer.getvalue()
        response = make_response(pdf_data)
        response.headers['Content-Disposition'] = 'attachment; filename=bill.pdf'
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Length'] = len(pdf_data)
        return response

    except ValueError as e:
        return f"Error in processing your request: {str(e)}", 400


if __name__ == '__main__':
    app.run(debug=True)
