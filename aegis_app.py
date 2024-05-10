from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

#-----------------------------------------------------------------------------
# Database quety functions that support the controller functions (routes)
#-----------------------------------------------------------------------------


# get all items - for the database display window
def get_items():
    conn = sqlite3.connect('project-aegis.db') 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM item")
    items = cursor.fetchall()
    conn.close()
    return items

# Get all the items past due date function
def get_items_past_return_due_date():
    conn = sqlite3.connect('project-aegis.db') 
    cursor = conn.cursor()
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT * FROM item WHERE return_due_date < ?", (current_date,))
    items = cursor.fetchall()
    conn.close()
    return items

# Return item function
def return_item(barcode_number):
    conn = sqlite3.connect('project-aegis.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE item SET is_checked_out = ?, borrower_name = ?, borrower_stud_id = ?, borrower_phone = ?, borrowed_date = ?, return_due_date = ? WHERE barcode_number = ?", (0, 'NA', 'NA', 'NA', None, None, barcode_number))
    conn.commit()
    conn.close()

# Checkout item function
def checkout_item(barcode_number, full_name, student_id, phone_number, date_checked_out, return_due_date):
    conn = sqlite3.connect('project-aegis.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE item SET is_checked_out = ?, borrower_name = ?, borrower_stud_id = ?, borrower_phone = ?, borrowed_date = ?, return_due_date = ? WHERE barcode_number = ?", (1, full_name, student_id, phone_number, date_checked_out, return_due_date, barcode_number))
    conn.commit()
    conn.close()

# Create item function
def create_item(barcode_number, item_name, item_description):
    conn = sqlite3.connect('project-aegis.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO item (item_name, item_description, is_checked_out, borrower_name, borrower_stud_id, borrower_phone, barcode_number, borrowed_date, return_due_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (item_name, item_description, 0, 'N/A', 'N/A', 'N/A', barcode_number, None, None))
    conn.commit()
    conn.close()

def update_item(form_data):
    conn = sqlite3.connect('project-aegis.db')
    cursor = conn.cursor()

    query = "UPDATE item SET"
    columns_to_update = []
    for key, value in form_data.items():
        if key == 'barcode_number':
            continue
        if value is not None and value != '':
            # Check if the column name exists in the table
            if key in ['item_name', 'item_description', 'is_checked_out', 'borrower_name', 'borrower_stud_id', 'borrower_phone', 'borrowed_date', 'return_due_date']:
                columns_to_update.append("{} = '{}'".format(key, value))
    query += " " + ", ".join(columns_to_update)
    query += " WHERE barcode_number = '{}'".format(form_data['barcode_number'])
    cursor.execute(query)
    conn.commit()
    conn.close()



def delete_item(barcode_number):
    conn = sqlite3.connect('project-aegis.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM item WHERE barcode_number = ?", (barcode_number,))
    conn.commit()
    conn.close()



#-----------------------------------------------------------------------------
# Functions that handle requests from the html form
#-----------------------------------------------------------------------------

# default route for index.html the homepage
@app.route('/')
def index():
    items = get_items()
    late_items = get_items_past_return_due_date()
    return render_template('index.html', items=items, late_items=late_items)

# Return the item route
@app.route('/return-item', methods=['POST'])
def return_item_route():
    barcode_number = request.form['barcode-number']
    return_item(barcode_number)
    return redirect(url_for('index'))

@app.route('/checkout-item', methods=['POST'])
def checkout_item_route():
    barcode_number = request.form['barcode-number']
    full_name = request.form['full-name']
    student_id = request.form['student-id']
    phone_number = request.form['phone-number']
    date_checked_out = request.form['date-checked-out']
    return_due_date = request.form['return-due-date']

    # Call the checkout_item function
    checkout_item(barcode_number, full_name, student_id, phone_number, date_checked_out, return_due_date)

    return redirect(url_for('index'))

@app.route('/create-item', methods=['POST'])
def create_item_route():
    barcode_number = request.form['barcode-number']
    item_name = request.form['item-name']
    item_description = request.form['item-description']

    create_item(barcode_number, item_name, item_description)
    return redirect(url_for('index'))

# Checkout item route
@app.route('/update-item', methods=['POST'])
def update_item_route():
    form_data = {
        'barcode_number': request.form['barcode-number'],
        'item_name': request.form['item-name'],
        'item_description': request.form['item-description'],
        'full_name': request.form['full-name'],
        'student_id': request.form['student-id'],
        'phone_number': request.form['phone-number'],
        'date_checked_out': request.form['date-checked-out'],
        'return_due_date': request.form['return-due-date']
    }

    update_item(form_data)

    return redirect(url_for('index'))


@app.route('/delete-item', methods=['GET','POST'])
def delete_item_route():
    barcode_number = request.form['barcode-number']

    delete_item(barcode_number)

    return redirect(url_for('index'))



# Run the python flask application

if __name__ == '__main__':
    app.run(debug=False)
