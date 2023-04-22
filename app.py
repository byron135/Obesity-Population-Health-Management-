from flask import Flask, render_template, url_for, redirect, request
from app.src.tools import connectionHelper
import pandas as pd

app = Flask(__name__)
a = pd.read_csv("patient.csv")
print("hello")
print(a.columns)

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
    genders = set(a['gender'].unique())
    races = set(a['race'].unique())
    if request.method == 'POST':
        selected_gender = request.form['gender']
        selected_race = request.form['race']
        filtered_df = a
        if (selected_gender != "All genders"):
            filtered_df = a[a['gender'] == selected_gender]
        filtered_df2 = filtered_df
        if (selected_race != "All races"):
            filtered_df2 = filtered_df[filtered_df['race'] == selected_race]
        table_html = filtered_df2.to_html(classes='table table-striped')
        return render_template('table.html', table=table_html, genders = genders, races = races, selected_category=selected_gender)
    table_html = a.to_html(classes='table table-striped')
    return render_template('table.html', table=table_html, genders = genders, races = races, selected_category=None)

if __name__ == "__main__":
    app.run()