import requests
# from urllib.request import urlopen as req_url
# from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, request
# import xgboost as xgb
import pickle
import sklearn
# from xgboost import XGBClassifier
# from sklearn.experimental import enable_hist_gradient_boosting
# from sklearn.ensemble import HistGradientBoostingClassifier
app = Flask(__name__, template_folder='template')
#
# @app.route('/',methods=['POST','GET'])
# def index():
#     print("Inside index route....")
#     if request.method == 'POST':
#         first_name = request.form['content_fname'].strip()
#         last_name = request.form['content_lname'].strip()
#         age = request.form['age'].strip()
#         height = request.form['height'].strip()
#         weight = request.form['weight'].strip()
#         sbp = request.form['sbp'].strip()
#         dbp = request.form['dbp'].strip()
#         cholesterol = request.form['cholesterol'].strip()
#         glucose = request.form['glucose'].strip()
#         smoke = request.form['smoke'].strip()
#         drink = request.form['drink'].strip()
#         activity = request.form['activity'].strip()
#         # print(first_name)
#         # print(last_name)
#         # print(age)
#         # print(height)
#         # print(weight)
#         # print(sbp)
#         # print(dbp)
#         # print(cholesterol)
#         # print(glucose)
#         # print(smoke)
#         # print(drink)
#         # print(activity)
#     else:
#         return render_template('index.html')
#
#
# if __name__ == "__main__":
#     app.run(port=7000,debug=True)

#
filename = 'grad_boost.pickle'
filename_scaler = 'scaler_model.pickle'
loaded_model = pickle.load(open(filename, 'rb'))
scaler_model = pickle.load(open(filename_scaler, 'rb'))

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    patient_data = dict()
    name = request.form['content_fname']
    last_name = request.form['content_lname'].strip()
    age = request.form['age']
    height = request.form['height'].strip()
    weight = request.form['weight'].strip()
    gender= request.form['gender']
    sbp = request.form['sbp'].strip()
    dbp = request.form['dbp'].strip()
    cholesterol = request.form.get('cholesterol')
    glucose = request.form.get('glucose')
    smoke = request.form['smoke']
    drink = request.form['drink']
    activity = request.form['activity']
    patient_data={'name':name,
                  'last_name':last_name,
                  'age':age,
                  'height':height,
                  'weight':weight,
                  'gender':gender,
                  'sbp':sbp,
                  'dbp':dbp,
                  'cholesterol':cholesterol,
                  'glucose':glucose,
                  'smoke':smoke,
                  'drink':drink,
                  'activity':activity
                  }
    # return patient_data

    params = []
    age = int(patient_data['age'])
    params.append(age)
    height = int(patient_data['height'])
    params.append(height)
    weight = float(patient_data['weight'])
    params.append(weight)
    gender = patient_data['gender']
    if gender == 'male':
        gender = 1
    else:
        gender = 0
    params.append(gender)
    sbp = int(patient_data['sbp'])
    params.append(sbp)
    dbp = int(patient_data['dbp'])
    params.append(dbp)
    chl = patient_data['cholesterol']
    if chl == 'Normal':
        chl = 1
    elif chl == 'Above normal':
        chl = 2
    else:
        chl = 3
    params.append(chl)
    gluc = patient_data['glucose']
    if gluc == 'Normal':
        gluc = 1
    elif gluc == 'Above normal':
        gluc = 2
    else:
        gluc = 3
    params.append(gluc)
    smoke = patient_data['smoke']
    if smoke == 'yes':
        smoke = 0
    else:
        smoke = 0
    params.append(smoke)

    alc = patient_data['drink']
    if alc == 'yes':
        alc = 1
    else:
        alc = 0
    params.append(alc)
    act = patient_data['activity']
    if act == 'yes':
        act = 1
    else:
        act = 0
    params.append(act)

    result  = scaler_model.transform([params])
    predicter = loaded_model.predict(result)
    if predicter[0]==0:
        user_out ='Negative'
    else:
        user_out = 'Positive'

    return 'Your health check up is done , you are '+user_out














    # model_prep(patient_data)
# def model_prep(patient_data):
#     params = []
#     age = int(patient_data['age'])
#     params.append(age)
#     height = int(patient_data['height'])
#     params.append(height)
#     weight = float(patient_data['weight'])
#     params.append(weight)
#     gender = patient_data['gender']
#     if gender == 'male':
#         gender = 1
#     else:
#         gender = 0
#     params.append(gender)
#     sbp = patient_data['sbp']
#     params.append(sbp)
#     dbp = patient_data['dbp']
#     params.append(dbp)
#     chl = patient_data['cholesterol']
#     if chl == 'Normal':
#         chl = 1
#     elif chl =='Above normal':
#         chl = 2
#     else:
#         chl = 3
#     params.append(chl)
#     gluc = patient_data['glucose']
#     if gluc == 'Normal':
#         gluc = 1
#     elif gluc == 'Above normal':
#         gluc = 2
#     else:
#         gluc = 3
#     params.append(gluc)
#     smoke= patient_data['smoke']
#     if smoke=='yes':
#         smoke = 0
#     else:
#         smoke = 0
#     params.append(smoke)
#
#     alc = patient_data['drink']
#     if alc =='yes':
#         alc = 1
#     else:
#         alc = 0
#     params.append(alc)
#     act = patient_data['activity']
#     if act =='yes':
#         act = 1
#     else:
#         act = 0
#     params.append(act)




if __name__ == "__main__":
    app.run(port=7000,debug=True)