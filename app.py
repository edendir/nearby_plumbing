import os
from flask import Flask, render_template
from flask_mail import Message

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    service = request.form.get("service")
    message = request.form.get("message")
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
