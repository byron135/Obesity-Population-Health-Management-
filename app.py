from flask import Flask, render_template, url_for, redirect, request
from app.src.tools import connectionHelper
import pandas as pd

app = Flask(__name__)
a = pd.read_csv("patient.csv")

@app.route("/", methods =['GET', 'POST'])
def home():
    #html_table = a.to_html()
    return render_template('home.html')

@app.route("/metrics")
def metrics():
    return render_template('metrics.html')

@app.route("/add")
def add():
    return render_template('addpatient.html')

@app.route("/update")
def update():
    return render_template('updatepatient.html')

@app.route("/styles.css")
def styleSheet():
    return app.send_static_file('styles.css')

@app.route("/api/get_patient", methods=['GET'])
def get_patient():
    connectionHelper.init()
    print("done")
    return "File saved as patient.csv"

@app.route('/table', methods=['GET', 'POST'])
def display_table():
    # get the unique values in the 'Category' column
    categories = a['Category'].unique()
    # handle form submission
    if request.method == 'POST':
        # get the selected category from the form
        selected_category = request.form['category']
        # filter the DataFrame based on the selected category
        filtered_df = a[a['Category'] == selected_category]
        # convert the filtered DataFrame to an HTML table
        table_html = filtered_df.to_html(classes='table table-striped')
        # render the template with the table and the category options
        return render_template('table.html', table=table_html, categories=categories, selected_category=selected_category)
    # if no form submission, render the template with the table and the category options
    table_html = a.to_html(classes='table table-striped')
    return render_template('table.html', table=table_html, categories=categories, selected_category=None)

if __name__ == "__main__":
    app.run()