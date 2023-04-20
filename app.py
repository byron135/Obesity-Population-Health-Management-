from flask import Flask
from app.src.tools import connectionHelper
app = Flask(__name__)

@app.route("/api/get_patient", methods=['GET'])
def get_patient():
    connectionHelper.init()
    print("done")
    return "File saved as patient.csv"

if __name__ == "__main__":
    app.run()