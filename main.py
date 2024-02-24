from flask import Flask, render_template, url_for, session, request, redirect, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "404 error"
app.permanent_session_lifetime = timedelta(minutes= 1)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/info")
def infopage():
    return

@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        Starter_Deposit = request.form["Deposit"]
        Monthly_Saving = request.form["Monthly Saving"]
        Period_Time = request.form["Period of Time"]
        Goal_Amount = request.form["Goal Amount"]

        if Starter_Deposit == "" or Starter_Deposit == "0":
            flash("Please fill in the form")
            return redirect(url_for("form"))
        elif Monthly_Saving == "" or Monthly_Saving == "0":
            flash("Please fill in the form")
            return redirect(url_for("form"))
        elif Period_Time == "" or Period_Time == "0":
            flash("Please fill in the form")
            return redirect(url_for("form"))
        elif Goal_Amount == "" or Goal_Amount == "0":
            flash("Please fill in the form")
            return redirect(url_for("form"))
        else:
            session["Deposit"] = Starter_Deposit
            session["Monthly Saving"] = Monthly_Saving
            session["Period of Time"] = Period_Time
            session["Goal Amount"] = Goal_Amount
            return redirect(url_for("option"))

    if "Deposit" and "Monthly Saving" and "Period of Time" and "Goal Amount" in session:
        session.pop("Deposit", None)
        session.pop("Monthly Saving", None)
        session.pop("Period of Time", None)

    return render_template("form.html")

@app.route("/option", methods=["POST", "GET"])
def option():
    if request.method == "POST":
        Interest_Rate = request.form["Interest_rate"]
        Yes = request.form["YES"]

        if Interest_Rate != "" or Interest_Rate != "0":
            if Yes == "" or Yes == "0":
                session["Interest Rate"] = Interest_Rate
                return redirect(url_for("result"))
        elif Yes == "YES":
            if  Interest_Rate == "" or Interest_Rate == "0":
                session["YES"] = Yes
                
        flash("Please fill in the form correctly.")
    return render_template("option.html")

@app.route("/dictionary")
def dictionary():
    return render_template("dictionary.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/media")
def media():
    return render_template("media.html")

@app.route("/result")
def result():
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)



