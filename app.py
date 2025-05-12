from flask import Flask, render_template, request, redirect, g, url_for
from database import getDatabase, connectToDatabase
import pickle
import numpy as np

filename = 'diabetes-prediction-rfc-model.pkl'
classifier = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.teardown_appcontext
def closeDatabase(error):
    if hasattr(g, 'diabetes_db'):
        g.diabetes_db.close()

@app.route('/datacollection', methods=["POST", "GET"])
def datacollection():
    if request.method == 'POST':
        username = request.form['username']
        age = request.form['age']
        height = int(request.form['height'])
        weight = int(request.form['weight'])
        pregnancies = int(request.form['pregnancies'])
        mealsperday = int(request.form['mealsperday'])
        totalexersisehours = int(request.form['totalexersisehours'])
        glucose = int(request.form['glucose'])
        bloodpressure = int(request.form['bloodpressure'])
        skinthickness = int(request.form['skinthickness'])
        insulin = int(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        familyhistory = int(request.form['familyhistory'])
        meal1 = request.form['meal1']
        meal2 = request.form['meal2']
        meal3 = request.form['meal3']
        meal4 = request.form['meal4']
        meal5 = request.form['meal5']

        db = getDatabase()
        db.execute("insert into persondata (username, age, height, weight, pregnancies, mealsperday, totalexersisehours, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, familyhistory, meal1, meal2, meal3, meal4, meal5 ) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                  [username, age, height, weight, pregnancies, mealsperday, totalexersisehours, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, familyhistory, meal1, meal2, meal3, meal4, meal5])
        db.commit()
        return redirect(url_for("home"))            
    return render_template("datacollection.html")

@app.route('/bmiresult')
def bmiresult():
    return render_template("bmiresult.html")

@app.route('/glucoseresult')
def glucoseresult():
    return render_template("glucoseresult.html")

@app.route('/team')
def team():
    return render_template("team.html")

@app.route('/bmicalculator', methods=["POST","GET"])
def bmicalculator():
    bmivalue = 0
    if request.method == "POST":
        height = int(request.form['height'])
        height = height/100
        height = height ** 2
        weight = int(request.form['weight'])
        bmivalue = weight / height
        return render_template('bmiresult.html', bmivalue=bmivalue)
    return render_template("bmicalculator.html", bmivalue=bmivalue)

@app.route('/glucosecalculator', methods=["POST", "GET"])
def glucosecalculator():
    meal1 = None
    meal2 = None
    meal3 = None
    meal4 = None
    meal5 = None
    glucoseresult = 0
    if request.method == "POST":
        meal1 = request.form['meal1']
        meal2 = request.form['meal2']
        meal3 = request.form['meal3']
        meal4 = request.form['meal4']
        meal5 = request.form['meal5']

        food_scores = {
            "cake": 47, "apple": 44, "bagel": 72, "bun": 61,
            "bread": 56, "wheat": 71, "floor": 73, "grains": 51,
            "coke": 63, "fanta": 68, "applejuice": 50, "orange": 38,
            "tomato": 55, "potato": 61, "honey": 58, "corn": 55,
            "coconut": 54, "banana": 51
        }

        meals = [meal1, meal2, meal3, meal4, meal5]
        sum = 0
        for i in meals:
            if i.lower() in food_scores:
                sum = sum + food_scores[i.lower()]
                
        glucoseresult = sum / len(meals)

        return render_template("glucoseresult.html", meal1=meal1, meal2=meal2, meal3=meal3, meal4=meal4, meal5=meal5, glucoseresult=glucoseresult)
    return render_template("glucosecalculator.html", meal1=meal1, meal2=meal2, meal3=meal3, meal4=meal4, meal5=meal5, glucoseresult=glucoseresult)

@app.route("/showcollecteddata", methods=["POST", "GET"])
def showcollecteddata():
    db = getDatabase()
    db_cur = db.execute("select * from persondata")
    alldata = db_cur.fetchall()
    return render_template("showcollecteddata.html", alldata=alldata)

@app.route('/predict', methods=["POST", "GET"])
def predict():
    prediction_result = None
    recommendedinsulin = None
    recommendedmealsperday = None
    recommendedtotalexersisehours = None
    recommendedglucose = None
    recommendedbloodpressure = None

    if request.method == 'POST':
        username = request.form['username']
        username = username.lower()
        age = request.form['age']
        height = int(request.form['height'])
        weight = int(request.form['weight'])
        pregnancies = int(request.form['pregnancies'])
        mealsperday = int(request.form['mealsperday'])
        totalexersisehours = int(request.form['totalexersisehours'])
        glucose = float(request.form['glucose'])
        bloodpressure = int(request.form['bloodpressure'])
        skinthickness = int(request.form['skinthickness'])
        insulin = int(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        familyhistory = int(request.form['familyhistory'])
        meal1 = request.form['meal1']
        meal2 = request.form['meal2']
        meal3 = request.form['meal3']
        meal4 = request.form['meal4']
        meal5 = request.form['meal5']

        # Enhanced recommendations
        if mealsperday < 4:
            recommendedmealsperday = "Very low meal frequency. Increase to 5-6 balanced meals per day for better glucose control."
        elif mealsperday < 6:
            recommendedmealsperday = "Consider increasing to 5-6 smaller meals per day for optimal metabolism."
        elif mealsperday == 6:
            recommendedmealsperday = "Good meal frequency. Maintain this pattern."
        else:
            recommendedmealsperday = "Reduce meal frequency to 5-6 meals per day to prevent constant insulin stimulation."

        if totalexersisehours < 0.5:
            recommendedtotalexersisehours = "Very low activity level. Aim for at least 30 minutes daily to improve insulin sensitivity."
        elif totalexersisehours < 1:
            recommendedtotalexersisehours = "Moderate activity. Increase to 1 hour daily for better metabolic health."
        elif totalexersisehours == 1:
            recommendedtotalexersisehours = "Good exercise duration. Maintain this routine."
        else:
            recommendedtotalexersisehours = "Excellent activity level. Ensure you're including both cardio and strength training."

        if glucose < 70:
            recommendedglucose = "DANGER: Hypoglycemic range. Seek immediate medical attention if symptomatic."
        elif glucose < 100:
            recommendedglucose = "Normal fasting glucose. Maintain healthy habits."
        elif glucose < 126:
            recommendedglucose = "Prediabetic range. Consult doctor for oral glucose tolerance test."
        else:
            recommendedglucose = "Diabetic range. Urgent medical evaluation required."
        
        if bloodpressure < 90:
            recommendedbloodpressure = "Low blood pressure. Ensure proper hydration and consult if symptomatic."
        elif bloodpressure < 120:
            recommendedbloodpressure = "Normal blood pressure. Ideal range to maintain."
        elif bloodpressure < 140:
            recommendedbloodpressure = "Elevated blood pressure. Lifestyle modifications recommended."
        else:
            recommendedbloodpressure = "Hypertensive range. Medical evaluation required."
        
        if insulin < 16:
            recommendedinsulin = "Very low insulin. Could indicate type 1 diabetes. Medical evaluation required."
        elif insulin < 30:
            recommendedinsulin = "Low insulin. May indicate early insulin resistance."
        elif insulin <= 846:
            recommendedinsulin = "Normal insulin range."
        else:
            recommendedinsulin = "Extremely high insulin. Strong indication of insulin resistance."

        # BMI classification
        if bmi < 18.5:
            bmi_class = "Underweight (increased health risks)"
        elif 18.5 <= bmi < 25:
            bmi_class = "Normal weight"
        elif 25 <= bmi < 30:
            bmi_class = "Overweight"
        else:
            bmi_class = "Obese (significant health risks)"

        # Food analysis
        food_scores = {
            "cake": 47, "apple": 44, "bagel": 72, "bun": 61,
            "bread": 56, "wheat": 71, "floor": 73, "grains": 51,
            "coke": 63, "fanta": 68, "applejuice": 50, "orange": 38,
            "tomato": 55, "potato": 61, "honey": 58, "corn": 55,
            "coconut": 54, "banana": 51
        }

        problematic_foods = []
        for meal in [meal1, meal2, meal3, meal4, meal5]:
            if meal.lower() in food_scores and food_scores[meal.lower()] > 60:
                problematic_foods.append(meal)

        food_recommendations = []
        if problematic_foods:
            food_recommendations.append(
                f"High GI foods detected: {', '.join(problematic_foods)}. Limit these to reduce glucose spikes."
            )
            food_recommendations.append(
                "Replace with: leafy greens, nuts, legumes, whole grains, lean proteins"
            )
        else:
            food_recommendations.append(
                "Your food choices show good balance. Focus on variety and fiber."
            )

        # Risk assessment
        data = np.array([[pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, age]])
        prediction_result = classifier.predict(data)[0]
        
        if prediction_result == 1:
            risk_level = "High"
            risk_description = "Our analysis indicates a 85% likelihood of diabetes based on your metrics."
            immediate_actions = [
                "Urgent: Schedule doctor visit within 1 week",
                "Get HbA1c and fasting glucose tests",
                "Begin monitoring blood sugar daily",
                "Consult dietitian for meal planning"
            ]
        else:
            risk_level = "Low"
            risk_description = "Your current diabetes risk appears low, but regular screening is advised."
            immediate_actions = [
                "Annual diabetes screening recommended",
                "Maintain healthy diet and exercise routine",
                "Monitor for symptoms like excessive thirst",
                "Reassess if family history changes"
            ]

        return render_template('result.html', 
            prediction_result=prediction_result,
            username=username,
            meal1=meal1, meal2=meal2, meal3=meal3, meal4=meal4, meal5=meal5,
            weight=weight, height=height, glucose=glucose, 
            bloodpressure=bloodpressure, insulin=insulin,
            totalexersisehours=totalexersisehours, mealsperday=mealsperday,
            recommendedmealsperday=recommendedmealsperday,
            recommendedtotalexersisehours=recommendedtotalexersisehours,
            recommendedglucose=recommendedglucose,
            recommendedinsulin=recommendedinsulin,
            recommendedbloodpressure=recommendedbloodpressure,
            risk_level=risk_level,
            risk_description=risk_description,
            immediate_actions=immediate_actions,
            bmi_class=bmi_class,
            food_recommendations=food_recommendations,
            age=age, bmi=bmi, familyhistory=familyhistory
        )        

    return render_template("predict.html", prediction_result=prediction_result)

if __name__ == '__main__':
    app.run(debug=True)