from flask import Flask, render_template, url_for, redirect, request, jsonify,send_file
import os
import numpy as np
import pandas as pd
from flask_cors import CORS
import sklearn
import openai


app = Flask(__name__)

#GPT chatbot

# openai.api_key = ""



#### model ####################################################################
Obesity_raw_data = pd.read_csv('ObesityDataSet_raw_and_data_sinthetic.csv')
#Obesity_raw_data = pd.read_csv('gs://obesity-data-set/ObesityDataSet_raw_and_data_sinthetic.csv'
Obesity_raw_data.info(verbose = True)

Obesity_raw_data['Gender_score'] = Obesity_raw_data.Gender.map({'Male':0,'Female':1})
Obesity_raw_data['FAVC_score'] = Obesity_raw_data.FAVC.map({'no':0,'yes':1})
Obesity_raw_data['family_history_with_overweight_score'] = Obesity_raw_data.family_history_with_overweight.map({'no':0,'yes':1})
Obesity_raw_data['SMOKE_score'] = Obesity_raw_data.SMOKE.map({'no':0,'yes':1})
Obesity_raw_data['SCC_score'] = Obesity_raw_data.SCC.map({'no':0,'yes':1})
Obesity_raw_data['CAEC_score'] = Obesity_raw_data.CAEC.map({'no':0,'Sometimes':1,'Frequently':2,'Always':3})
Obesity_raw_data['CALC_score'] = Obesity_raw_data.CALC.map({'no':0,'Sometimes':1,'Frequently':2,'Always':3})
Obesity_raw_data['MTRANS_score'] = Obesity_raw_data.MTRANS.map({'Bike':0,'Motorbike':1,'Walking':2,'Public_Transportation':3,'Automobile':3})
Obesity_scored_data = Obesity_raw_data.loc[:, ['Age','Height','Weight','FCVC','NCP','CH2O','FAF','TUE','FAVC_score','family_history_with_overweight_score','SMOKE_score','SCC_score','CAEC_score','CALC_score','MTRANS_score','Gender_score', 'NObeyesdad']]

female_data = Obesity_scored_data[Obesity_scored_data.Gender_score.isin([1])]
male_data = Obesity_scored_data[Obesity_scored_data.Gender_score.isin([0])]

female_data.describe()
male_data.describe()



from sklearn.preprocessing import StandardScaler
sc_X_female = StandardScaler()
X_female =  pd.DataFrame(sc_X_female.fit_transform(female_data.drop(["NObeyesdad","MTRANS_score","FAVC_score","NCP","SCC_score","TUE",'Gender_score'],axis = 1),),
        columns=['Age','Height','Weight','FCVC','CH2O','FAF',"CAEC_score",'family_history_with_overweight_score','SMOKE_score','CALC_score'])

y_female = female_data.NObeyesdad
X_female.head()

from sklearn.model_selection import train_test_split
X_train_female,X_test_female,y_train_female,y_test_female = train_test_split(X_female,y_female,test_size=1/3,random_state=42)

from sklearn.neighbors import KNeighborsClassifier
test_scores_female = []
train_scores_female = []

for i in range(1,19,2):
    knn = KNeighborsClassifier(i)
    knn.fit(X_train_female,y_train_female)
    train_scores_female.append(knn.score(X_train_female,y_train_female))
    test_scores_female.append(knn.score(X_test_female,y_test_female))

knn = KNeighborsClassifier(n_neighbors = 5)

knn.fit(X_train_female,y_train_female)
knn.score(X_test_female,y_test_female)

female_filtered_data = female_data.drop(["NObeyesdad","MTRANS_score","FAVC_score","NCP","SCC_score","TUE","Gender_score"],axis = 1)
female_filtered_data.head()

new_female_data =  [
    {
        'Age': 21,
        'Height': 1.7,
        'Weight': 80,
        'FCVC': 0,
        'CH2O': 3,
        'FAF': 1,
        'CAEC_score': 1,
        'family_history_with_overweight_score': 1,
        'SMOKE_score': 0,
        'CALC_score': 0
    }]

sc_X_male = StandardScaler()
X_male =  pd.DataFrame(sc_X_male.fit_transform(male_data.drop(["NObeyesdad","MTRANS_score","FAVC_score","NCP","SCC_score","TUE",'Gender_score'],axis = 1),),
        columns=['Age','Height','Weight','FCVC','CH2O','FAF',"CAEC_score",'family_history_with_overweight_score','SMOKE_score','CALC_score'])

y_male = male_data.NObeyesdad

X_train_male,X_test_male,y_train_male,y_test_male = train_test_split(X_male,y_male,test_size=1/3,random_state=42)
test_scores_male = []
train_scores_male = []

for i in range(1,19,2):

    knn = KNeighborsClassifier(i)
    knn.fit(X_train_male,y_train_male)
    train_scores_male.append(knn.score(X_train_male,y_train_male))
    test_scores_male.append(knn.score(X_test_male,y_test_male))

knn = KNeighborsClassifier(n_neighbors = 5)

knn.fit(X_train_male,y_train_male)
knn.score(X_test_male,y_test_male)

male_filtered_data = male_data.drop(["NObeyesdad","MTRANS_score","FAVC_score","NCP","SCC_score","TUE","Gender_score"],axis = 1)
male_filtered_data.head()

new_male_data =  [
    {
        'Age': 21,
        'Height': 1.7,
        'Weight': 70,
        'FCVC': 3,
        'CH2O': 3,
        'FAF': 3,
        'CAEC_score': 1,
        'family_history_with_overweight_score': 1,
        'SMOKE_score': 0,
        'CALC_score': 0
    }]

###############################################################################################################################################################



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

@app.route("/patientform", methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        response_object = {'status': 'success', 'Access-Control-Allow-Origin': '*'}
        diagnosis = None
        image_path = {"Insufficient_Weight" :"static/insufficient.png" , "Normal_Weight": "static/normal.png", "Overweight_Level_I": "static/OWI.png" , "Overweight_Level_II": "static/OWII.png","Obesity_Type_I": "static/OBI.png", "Obesity_Type_II": "static/OBII.png", "Obesity_Type_III": "static/OBIII.png"  }
        name = request.form['name']
        print(request.form["sex"])
        
        if request.form["sex"] == "1":
            print("male")
            new_male_data[0]['Age'] = int(request.form['age'])
            new_male_data[0]['Height'] = round(int(request.form['height']) * 0.0234, 1)
            new_male_data[0]['Weight'] = round(int(request.form['weight']) * 0.60592)
            new_male_data[0]['FCVC'] = int(request.form['question1'])
            new_male_data[0]['CH2O'] = int(request.form['question2'])
            new_male_data[0]['FAF'] = int(request.form['question3'])
            new_male_data[0]['CAEC_score'] = int(request.form['question4'])
            new_male_data[0]['family_history_with_overweight_score'] = int(request.form['question5'])
            new_male_data[0]['SMOKE_score'] = int(request.form['question6'])
            new_male_data[0]['CALC_score'] = int(request.form['question7'])
            
            print('data')
            print(new_male_data)
            new_male_df = pd.DataFrame(new_male_data, columns=male_filtered_data.columns)
            New_Prediction = pd.concat([male_filtered_data, new_male_df])
            sc_X_new_male = StandardScaler()
            X_new_male = pd.DataFrame(sc_X_new_male.fit_transform(New_Prediction),
                    columns=['Age','Height','Weight','FCVC','CH2O','FAF',"CAEC_score",'family_history_with_overweight_score','SMOKE_score','CALC_score'])

            last_item = len(knn.predict(X_new_male)) - 1
            diagnosis = knn.predict(X_new_male)[last_item]
            print("this is the diagnosis")
            print(diagnosis)
            # response_object['diagnosis'] = diagnosis
            # response = jsonify(response_object)
            # response.headers.add('Access-Control-Allow-Origin', '*')
            # print("this is the response")
            # print(response)

            # return response
        
        else:
            print("female")
            new_female_data[0]['Age'] = int(request.form['age'])
            new_female_data[0]['Height'] =round(int(request.form['height']) * 0.0254, 1)
            new_female_data[0]['Weight'] = round(int(request.form['weight']) * 0.440592)
            new_female_data[0]['CH2O'] = int(request.form['question2'])
            new_female_data[0]['FAF'] = int(request.form['question3'])
            new_female_data[0]['CAEC_score'] = int(request.form['question4'])
            new_female_data[0]['family_history_with_overweight_score'] = int(request.form['question5'])
            new_female_data[0]['SMOKE_score'] = int(request.form['question6'])
            new_female_data[0]['CALC_score'] = int(request.form['question7'])
            

            new_female_df = pd.DataFrame(new_female_data, columns=female_filtered_data.columns)
            New_Prediction = pd.concat([female_filtered_data, new_female_df])
            sc_X_new_female = StandardScaler()
            X_new_female = pd.DataFrame(sc_X_new_female.fit_transform(New_Prediction),
                    columns=['Age','Height','Weight','FCVC','CH2O','FAF',"CAEC_score",'family_history_with_overweight_score','SMOKE_score','CALC_score'])

            last_item = len(knn.predict(X_new_female)) - 1
            diagnosis = knn.predict(X_new_female)[last_item]
            print("THis is the diagnosis")
            print(diagnosis)
            # response_object['diagnosis'] = diagnosis
            # response = jsonify(response_object)
            # response.headers.add('Access-Control-Allow-Origin', '*')
            # print("this is the response")
            # print(response)
            # return response


        prompt = f"Patient name: {name}\nPatient diagnosis: {diagnosis}\nPatient age: {request.form['age']}\nPatient physical activity per week: {request.form['question3']}\nPatient's consuption of water: {request.form['question2']}\nPatient's consuption of vegeatables: {request.form['question1']}\nPatient BMI: {(int(request.form['weight'])/(int(request.form['height'])/12)**2 * 703)}\nPatient smoking status: {request.form['question6']}\nFamily history with obesity status: {request.form['question5']}\nPatient drinking status: {request.form['question7']}\n\nGenerate suggestions on what the patient can do based on the diagnosis given and the patient's information. Include potential solutions to these deficiencies.:"

        # response = openai.Completion.create(
        #     engine="text-davinci-002",
        #     prompt=prompt,
        #     max_tokens=1024,
        #     n=1,
        #     stop=None,
        #     temperature=0.5,
        # )

        # bot_diagnosis = response.choices[0].text.strip()
        # return render_template("home.html")
        print("image path")
        print(image_path[diagnosis])
        return render_template("results.html", name = name, diagnosis=diagnosis, image_path = image_path[diagnosis], description = None)
        # return send_file(image_path[diagnosis], mimetype='image/png')
    else:
        return render_template('patientform.html')
    
# @app.route("/results")
# def results(diagnosis, description, image_path):
#     return render_template("chatbot.html")

@app.route("/styles.css")
def styleSheet():
    return app.send_static_file('styles.css')



if __name__ == "__main__":
    app.run(debug=True)