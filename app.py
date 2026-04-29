from config import Config
from flask import Flask, flash, redirect, render_template, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
# print("Loaded configuration:")
# for key, value in app.config.items():
#     print(f"  {key}: {value}")

SERVICES_DATA = [
    {
        "title": "Leaky Pipe Repair",
        "short_description": "Fix leaky or burst pipes quickly.",
        "description": "Emergency burst pipe repairs to prevent water damage and restore your plumbing system quickly.",
        "image": "burst_pipe.jpg",
        "featured": True,
    },
    {
        "title": "Water Heaters",
        "short_description": "Water heater servicing and replacement.",
        "description": "Professional water heater installation and replacement services for reliable hot water supply.",
        "image": "inst_water_heater.jpg",
        "featured": True,
    },
    {
        "title": "Toilet Repairs",
        "short_description": "Expert toilet repair and replacement.",
        "description": "Expert toilet repair and replacement to fix leaks, running toilets, and other issues.",
        "image": "toilet_repairs.jpg",
        "featured": True,
    },
    {
        "title": "Water Damage Restoration",
        "short_description": "Comprehensive water damage assessment and restoration.",
        "description": "Comprehensive water damage assessment and restoration to protect your property.",
        "image": "water_damage.jpg",
        "featured": True,
    },
    {
        "title": "Water Softener Installation",
        "short_description": "Improve water quality with water softener installation.",
        "description": "Install water softening systems to improve water quality and protect your plumbing.",
        "image": "water_softener.jpg",
        "featured": True,
    },
    {
        "title": "Reverse Osmosis Systems",
        "short_description": "Advanced water filtration with reverse osmosis technology.",
        "description": "Advanced water filtration with reverse osmosis technology for clean, safe drinking water.",
        "image": "reverse_osmosis.jpg",
        "featured": False,
    },
    {
        "title": "Commercial Plumbing",
        "short_description": "Full-service commercial plumbing solutions.",
        "description": "Full-service commercial plumbing solutions for businesses of all sizes.",
        "image": "commercial.jpg",
        "featured": False,
    },
    {
        "title": "Residential New Construction",
        "short_description": "Complete plumbing installation for new residential construction projects.",
        "description": "Complete plumbing installation for new residential construction projects.",
        "image": "res_new_const.jpg",
        "featured": False,
    },
    {
        "title": "Residential Remodeling",
        "short_description": "Complete plumbing installation for residential remodeling projects.",
        "description": "Complete plumbing installation for residential remodeling projects.",
        "image": "res_rem.jpg",
        "featured": True,
    },
]


@app.route("/")
def home():
    return render_template("index.html", services=SERVICES_DATA)


def send_contact_email(name, email, content, service):
    content = f"""
New contact form submission

Name: {name}
Email: {email}
Service: {service}

Message:
{content}
"""

    msg = Mail(
        from_email=app.config["MAIL_FROM"],
        to_emails=app.config["MAIL_TO"],
        subject="New Contact Form Submission",
        plain_text_content=content,
    )

    sg = SendGridAPIClient(app.config["SENDGRID_API_KEY"])
    print("FROM:", app.config["MAIL_FROM"])
    print("TO:", app.config["MAIL_TO"])
    print("NAME:", name)
    print("EMAIL:", email)
    print("MESSAGE:", content)
    sg.send(msg)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        service = request.form.get("service")
        message = request.form.get("message")

        if not name or not email or not message:
            flash("All fields required")
            return redirect("/#contact")

        try:
            send_contact_email(name, email, message, service)
            flash("Message sent successfully!")
            return redirect("/contact")
        except Exception as e:
            print(e)
            flash("Error sending message. Please try again.")
            return redirect("/contact")
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
