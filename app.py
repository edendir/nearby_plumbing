import os
import smtplib
from email.message import EmailMessage

import yaml
from flask import Flask, render_template, request

# Load environment variables from .env.yaml
try:
    with open(".env.yaml", "r") as f:
        env_vars = yaml.safe_load(f)
        for key, value in env_vars.items():
            os.environ[key] = str(value)
except FileNotFoundError:
    print("Warning: .env.yaml file not found")
except Exception as e:
    print(f"Warning: Error loading .env.yaml: {e}")

app = Flask(__name__)

SERVICES_DATA = [
    {
        "title": "Burst Pipe Repair",
        "description": "Emergency burst pipe repairs to prevent water damage and restore your plumbing system quickly.",
        "image": "burst_pipe.jpg",
    },
    {
        "title": "Water Heater Installation",
        "description": "Professional water heater installation and replacement services for reliable hot water supply.",
        "image": "inst_water_heater.jpg",
    },
    {
        "title": "Toilet Repairs",
        "description": "Expert toilet repair and replacement to fix leaks, running toilets, and other issues.",
        "image": "toilet_repairs.jpg",
    },
    {
        "title": "Water Damage Restoration",
        "description": "Comprehensive water damage assessment and restoration to protect your property.",
        "image": "water_damage.jpg",
    },
    {
        "title": "Water Softener Installation",
        "description": "Install water softening systems to improve water quality and protect your plumbing.",
        "image": "water_softener.jpg",
    },
    {
        "title": "Reverse Osmosis Systems",
        "description": "Advanced water filtration with reverse osmosis technology for clean, safe drinking water.",
        "image": "reverse_osmosis.jpg",
    },
    {
        "title": "Commercial Plumbing",
        "description": "Full-service commercial plumbing solutions for businesses of all sizes.",
        "image": "commercial.jpg",
    },
    {
        "title": "Residential New Construction",
        "description": "Complete plumbing installation for new residential construction projects.",
        "image": "res_new_const.jpg",
    },
    {
        "title": "Residential Remodeling",
        "description": "Complete plumbing installation for residential remodeling projects.",
        "image": "res_rem.jpg",
    },
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        service = request.form.get("service")
        message = request.form.get("message")

        msg = EmailMessage()
        msg["Subject"] = f"New Contact Form Submission from {name}"
        msg["From"] = os.getenv("MAIL_FROM")
        msg["To"] = os.getenv("MAIL_USERNAME")
        msg["Reply-To"] = email

        msg.set_content(
            f"""
                        New Service Request
                        Name: {name}
                        Email: {email}
                        Service: {service}
                        Message: {message}
                        """
        )

        confirm = EmailMessage()
        confirm["Subject"] = "We've received your request"
        confirm["From"] = os.getenv("MAIL_FROM")
        confirm["To"] = email
        confirm.set_content(
            f"""
                            Thank you for your submission, {name}!
                            We have received your request and will get back to you soon.

                            -The Nearby Plumbing Team
                            """
        )

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))
                smtp.send_message(msg)
                smtp.send_message(confirm)
            return render_template("contact.html", success=True)
        except Exception as e:
            print(f"Email sending failed: {e}")
            return render_template(
                "contact.html", error="Failed to send email. Please try again."
            )
    else:
        return render_template("contact.html")


@app.route("/services")
def services():
    return render_template("services.html", services=SERVICES_DATA)


@app.route("/offers")
def offers():
    return render_template("offers.html")


if __name__ == "__main__":
    app.run(debug=True)
