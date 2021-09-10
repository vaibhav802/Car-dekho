from types import MethodDescriptorType
from flask import Flask, helpers,render_template,redirect,request,url_for,flash
import requests
import pandas as pd
from pandas import json_normalize
import json
app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\xec]/'

@app.route("/")
def index():
    return render_template('home.html')

@app.route('/aboutus/')
def aboutus():
    return render_template('aboutus.html')

@app.route('/oldcar/')
def old_car():
    return render_template('form.html')

@app.route('/newcar/')
def new_car():
    return render_template('form1.html')


@app.route("/api/", methods = ['POST'])
def api():
    error = None;
    try:
        url = "https://car-stockpile.p.rapidapi.com/models-for-year"
        make = request.form.get('make').lower().capitalize()
        year = request.form.get('year')
        querystring = {"year":year,"make":make}
        headers = {
            'x-rapidapi-key': "3cf3fb53d6mshc4c9df53eb6a7dap1325cbjsn6c062c8d1c3c",
            'x-rapidapi-host': "car-stockpile.p.rapidapi.com"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        data1 =pd.DataFrame.from_dict(data,orient='columns')
        return data1.to_html()
    except Exception as e:
        error = 'Data Not Available for this input'
        return render_template('home.html',error=error)


def read_data():
    data = pd.read_csv("Car details v3.csv")
    return data 

def read_data1():
    data1 = pd.read_csv('cars_ds_final.csv')
    data1.drop('Unnamed: 0' , axis = 1,inplace = True)
    data1.drop(data1.iloc[:, 47:],axis = 1,inplace = True)
    data1.drop(['Variant','Displacement','Valves_Per_Cylinder','Drivetrain','Cylinder_Configuration','Fuel_System','ARAI_Certified_Mileage','ARAI_Certified_Mileage_for_CNG','Kerb_Weight','Front_Suspension','Rear_Suspension','Front_Track','Rear_Track','Front_Tyre_&_Rim','Rear_Tyre_&_Rim','Power','Torque','Tachometer','Tripmeter'],axis=1,inplace = True)
    return data1



@app.route("/filterold/")
def form():
    data = read_data()
    seller = list(data['seller_type'].unique())
    owner = list(data['owner'].unique())
    C_name = list(data['name'].apply(lambda x: x.split()[0]).unique())
    fuel = list(data['fuel'].unique())
    print(seller[:5])
    print()
    return render_template("form.html", seller=seller, owner=owner, C_name=C_name, fuel=fuel)


@app.route("/aftersubmitold/", methods=['GET', 'POST'])
def aftersubmitold():
    if request.method == "GET":
        return redirect(url_for("form"))
        #return render_template("form.html")
    else:
        seller = request.form.get("seller")
        owner = request.form.get("owner")
        company = request.form.get("company")
        fuel = request.form.get("fuel")
        data = read_data()
        temp = data.copy()
        print(seller,owner,company,fuel)
        if seller:
            temp = temp[temp['seller_type'] == seller]
        if company:
            temp = temp[temp['name'].apply(lambda x:True if company in x else False)]
        if owner:
            temp = temp[temp['owner'] == owner]
        if fuel:
            temp = temp[temp['fuel'] == fuel]
        return temp.to_html()

@app.route("/filternew/")
def form1():
    data1 = read_data1()
    company = list(data1['Make'].unique())
    fuel = list(data1['Fuel_Type'].unique())
    emission = list(data1['Type'].unique())
    seat= list(data1['Seating_Capacity'].unique())
    return render_template("form1.html", company = company, fuel=fuel, emission=emission, seat=seat)



    
@app.route("/aftersubmitnew/", methods=['GET', 'POST'])
def aftersubmitnew():
    try:
        if request.method == "GET":
            return redirect(url_for("form1"))
            #return render_template("form.html")
        else:
            company = request.form.get("company")
            fuel = request.form.get("fuel")
            emission = request.form.get("emission")
            seat = request.form.get("seat")
            data1 = read_data1()
            temp = data1.copy()
            print(company,fuel,emission,seat)
            if company:
                temp = temp[temp['Make'] == company]
            if fuel:
                temp = temp[temp['Fuel_Type'] == fuel]
            if emission:
                temp = temp[temp['Type'] == emission]
            if seat:
                temp = temp[temp['Seating_Capacity'] == float(seat)]
            return temp.to_html()
    except:
        return render_template('form1.html')

app.run(debug=True)
