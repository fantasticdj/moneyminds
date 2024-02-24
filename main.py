from flask import Flask, render_template, url_for

app = Flask(__name__)
app.secret_key = "404 error"


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/register")
def register():
    return 


if __name__ == "__main__":
    app.run(debug=True)



