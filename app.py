from flask import Flask, render_template, url_for, redirect, request
app = Flask(__name__)


@app.route("/")
def home():
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

if __name__ == "__main__":
    app.run()