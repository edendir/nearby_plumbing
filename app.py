import os, requests
from flask import Flask, render_template
from flask_mail import Message

app = Flask(__name__)
request = requests.Request()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        service = request.form.get("service")
        message = request.form.get("message")
        return render_template("contact.html")
    else:
        return render_template("contact.html")

@app.route("/team")
def team():
    return render_template("team.html")

if __name__ == "__main__":
    app.run(debug=True)
