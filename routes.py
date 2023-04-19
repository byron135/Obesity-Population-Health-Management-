from flask import Flask, render_template, url_for, redirect, request
from app.src.tools.FHIRDataHelper import *

app = Flask(__name__)


@app.route("/")
def home():
    fdh = FHIRDataHelper("app\src\source\Zack583_Kertzmann286_9a9986bd-e4aa-4591-90e7-6171bdc69689.json")
    single_patient = fdh.get_all()
    return render_template('home.html', single_patient = single_patient)

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

if __name__ == "__main__":
    app.run()