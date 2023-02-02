import pickle
import json

from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

app = Flask(__name__)
cors = CORS(app)

client = MongoClient(
    "mongodb+srv://Hawkeye:umy0rbhY3VUFquYp@healthcare.iwosepb.mongodb.net/?retryWrites=true&w=majority")
parameters = []

@app.route('/prediction', methods=["POST"], strict_slashes=False)
@cross_origin()
def get_parameters():
    age = int(request.json['Age'])
    print(age)
    SysBP = int(request.json['SysBP'])
    print(SysBP)
    DiaBP = float(request.json['DiaBP'])
    HR = int(request.json['HR'])
    Glucose = int(request.json['Glucose'])
    totChol = int(request.json['TotChol'])
    CiggsperDay = int(request.json['CiggsperDay'])
    # Gender=request.form['Gender']
    CurrSmok = 1 if request.json['CurrSmok'] == "Yes" else 0
    BPmeds = 1 if request.json['BPMeds'] == "Yes" else 0
    Diabetes = 1 if request.json['Diab'] == "Yes" else 0
    db = client['test']
    collection = db['health']
    result = collection.find({"username": "Om"})
    for item in result:
        bmi = item['bmi']
        Gender = 1 if item["gender"] == "Male" else 0
        # print(age,SysBP,DiaBP,HR,Glucose,totChol,CiggsperDay,Gender,CurrSmok,BPmeds,bmi)
    parameters.extend([Gender, age, CurrSmok, CiggsperDay, BPmeds,
                      0, 0, Diabetes, totChol, SysBP, DiaBP, bmi, HR, Glucose])
    print(parameters)
    with open('./ML/heart_disease_classifier.pkl', 'rb') as f:
        classifier = pickle.load(f)
    with open('./ML/scaler.pkl', 'rb') as f:
        sc = pickle.load(f)
    # Predicting a new result
    result = classifier.predict(sc.transform([parameters]))
    parameters.clear()
    print(result[0])
    return json.dumps(result[0], default=str)
    # return parameter

if __name__=='__main__':
    app.run()
