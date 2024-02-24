from flask import Flask, render_template, url_for, session
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
    return


@app.route("/form")
def form():
    return render_template("form.html")



if __name__ == "__main__":
    app.run(debug=True)



