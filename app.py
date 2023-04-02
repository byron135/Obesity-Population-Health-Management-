from flask import Flask, render_template, url_for, redirect, request
app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/metrics")
def metrics():
    return render_template('metrics.html')


if __name__ == "__main__":
    app.run()