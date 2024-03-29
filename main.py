from flask import Flask, render_template, url_for, session, request, redirect, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "404 error"
app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/")
@app.route("/home")
def home():
    if "name" in session:
        name = session["name"]
        return render_template("index.html", name=name)
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "POST":
        name = request.form["nm"]
        email = request.form["email"]
        

        if name == "":
            flash("Please fill in the form.")
        elif email == "":
            flash("Please fill in the form.")
        else:
            session["name"] = name
            session["email"] = email
            session.permanent = True
            
            return redirect(url_for("home"))
    elif "name" in session and "email" in session:
        flash("Already Logged in!")
        return redirect(url_for("home"))
    
    if "name" in session:
        name = session["name"]
        return render_template("register.html", name=session["name"])

    return render_template("register.html")

@app.route("/calculator")
def calculator():
    if "name" in session:
        name = session["name"]
        return render_template("calculator.html", name=name)

    return render_template("calculator.html")

@app.route("/goalform", methods=["POST", "GET"])
def goalform():
    session["IfGoalCalculator"] = True

    
    if request.method == "POST":
        Starter_Deposit = request.form["Deposit"]
        Monthly_Allowance = request.form["Monthly Allowance"]
        Period_Time = request.form["Period of Time"]
        Goal_Money = request.form["Goal Money"]


        if Monthly_Allowance == "" or Monthly_Allowance == "0":
            flash("Please fill in the form")
            return redirect(url_for("goalform"))
        elif Period_Time == "" or Period_Time == "0":
            flash("Please fill in the form")
            return redirect(url_for("goalform"))
        elif Goal_Money == "" or Goal_Money == "0":
            flash("Please fill in the form")
            return redirect(url_for("goalform"))
        else:
            if Starter_Deposit == "" or Starter_Deposit == "0":
                if (int(Monthly_Allowance) * int(Period_Time)) < int(Goal_Money):
                    flash("Unable to reach goal money")
                    return redirect(url_for("goalform"))
            elif (int(Monthly_Allowance) * int(Period_Time) + int(Starter_Deposit)) < int(Goal_Money):
                flash("Unable to reach goal money")
                return redirect(url_for("goalform"))

            session["Deposit"] = Starter_Deposit
            session["Monthly Allowance"] = Monthly_Allowance
            session["Period of Time"] = Period_Time
            session["Goal Money"] = Goal_Money
            
            return redirect(url_for("result"))

    if "name" in session:
        name = session["name"]
        return render_template("goalform.html", name=name)

    if "Deposit" and "Monthly Saving" and "Period of Time" and "Goal Amount" in session:
        session.pop("Deposit", None)
        session.pop("Monthly Saving", None)
        session.pop("Period of Time", None)
    return render_template("goalform.html")   

@app.route("/form", methods=["POST", "GET"])
def form():
    session["IfGoalCalculator"] = False

    if request.method == "POST":
        Starter_Deposit = request.form["Deposit"]
        Monthly_Saving = request.form["Monthly Saving"]
        Period_Time = request.form["Period of Time"]

        if Starter_Deposit == "":
            flash("Please fill in the form")
            return redirect(url_for("form"))
        elif Monthly_Saving == "":
            flash("Please fill in the form")
            return redirect(url_for("form"))
        elif Period_Time == "" or Period_Time == "0":
            flash("Please fill in the form")
            return redirect(url_for("form"))
        else:
            session["Deposit"] = Starter_Deposit
            session["Monthly Saving"] = Monthly_Saving
            session["Period of Time"] = Period_Time
            
            return redirect(url_for("option"))

    if "Deposit" and "Monthly Saving" and "Period of Time" and "Goal Amount" in session:
        session.pop("Deposit", None)
        session.pop("Monthly Saving", None)
        session.pop("Period of Time", None)

    if "name" in session:
        name = session["name"]
        return render_template("form.html", name=name)
    return render_template("form.html")

@app.route("/option", methods=["POST", "GET"])
def option():

    
    if request.method == "POST":
        Interest_Rate = request.form["Interest_rate"]
        Yes = request.form["YES"]
        if Interest_Rate != "" or Interest_Rate != "0":
            if Yes == "":
                session["YES"] = Yes
                session["Interest Rate"] = Interest_Rate
                return redirect(url_for("result"))

        if Yes.lower() == "yes":  
            session["YES"] = Yes 
            session["Interest Rate"] = Interest_Rate
            return redirect(url_for("result"))
     
        flash("Please fill in the form correctly.")
    if "name" in session:
        name = session["name"]
        return render_template("option.html", name=name)
    return render_template("option.html")  
    

@app.route("/dictionary")
def dictionary():
    if "name" in session:
        name = session["name"]
        return render_template("dictionary.html", name=name)
    return render_template("dictionary.html")

@app.route("/about")
def about():
    if "name" in session:
        name = session["name"]
        return render_template("about.html", name=name)
    return render_template("about.html")

@app.route("/quiz")
def quiz():
    if "name" in session:
        name = session["name"]
        return render_template("quiz.html", name=name)
    return render_template("quiz.html")

@app.route("/result")
def result():

    if "IfGoalCalculator" in session and session["IfGoalCalculator"] == False:
        IfGoal = session["IfGoalCalculator"]
        Yes = session["YES"]
        Starter_Deposit = int(session["Deposit"])
        Monthly_Saving = int(session["Monthly Saving"])
        Period_Time = int(session["Period of Time"])

        if Yes.lower() == "yes":  
            session["YES"] = Yes 
            result = Starter_Deposit + Monthly_Saving*Period_Time
            if "name" in session:
                name = session["name"]
                return render_template("result.html", name=name, result=result,IfGoal=IfGoal, Period_Time=Period_Time)
            return render_template("result.html", result=result,IfGoal=IfGoal, Period_Time=Period_Time)
        else:
            Interest_Rate = int(session["Interest Rate"]) * 0.01
            if Yes == "":
                real_interest_rate = pow(1 + Interest_Rate/12, Period_Time)
                StarterMoney = real_interest_rate * Starter_Deposit
                MonthlyMoney = 0
                for _ in range(0, Period_Time):
                    monthly_interest_rate = pow(1 + Interest_Rate/12, Period_Time - _)
                    MonthlyMoney += monthly_interest_rate * Monthly_Saving
                result = round(MonthlyMoney + StarterMoney, 2)
                if "name" in session:
                    name = session["name"]
                    return render_template("result.html", name=name, result=result,IfGoal=IfGoal, Period_Time=Period_Time)
                return render_template("result.html", result=result,IfGoal=IfGoal, Period_Time=Period_Time)

    if "IfGoalCalculator" in session and session["IfGoalCalculator"] == True:
        Starter_Deposit = session["Deposit"]
        IfGoal = session["IfGoalCalculator"]
        if Starter_Deposit == "" or Starter_Deposit == "0":
            Monthly_Allowance = int(session["Monthly Allowance"] )
            Period_Time = int(session["Period of Time"] )
            Goal_Money = int(session["Goal Money"])
            UsableCash = Monthly_Allowance*Period_Time - Goal_Money
            FastestTime = round((Goal_Money - Starter_Deposit) / Period_Time,2)
            UsablePerMonth = UsableCash / Period_Time
            if "name" in session:
                name = session["name"]
                return render_template("result.html", name=name, NeededCash= NeededCash, UsableCash=UsableCash, FastestTime= FastestTime, IfGoal= IfGoal, UsablePerMonth=UsablePerMonth)
            return render_template("result.html", NeededCash= Goal_Money, UsableCash=UsableCash, FastestTime= FastestTime, IfGoal= IfGoal, UsablePerMonth=UsablePerMonth)
        else:
            Starter_Deposit = int(session["Deposit"])
            Monthly_Allowance = int(session["Monthly Allowance"] )
            Period_Time = int(session["Period of Time"] )
            Goal_Money = int(session["Goal Money"])
            NeededCash = Goal_Money
            UsableCash = (Monthly_Allowance*Period_Time + Starter_Deposit) - Goal_Money
            UsablePerMonth = round(UsableCash / Period_Time, 2)
            FastestTime = round(NeededCash / Period_Time,2)
            if "name" in session:
                name = session["name"]
                return render_template("result.html", name=name, NeededCash= NeededCash, UsableCash=UsableCash, FastestTime= FastestTime, IfGoal= IfGoal, UsablePerMonth=UsablePerMonth)
    
            return render_template("result.html", NeededCash= NeededCash, UsableCash=UsableCash, FastestTime= FastestTime, IfGoal= IfGoal, UsablePerMonth=UsablePerMonth)
    return redirect(url_for("calculator"))       

if __name__ == "__main__":
    app.run(debug=True)
