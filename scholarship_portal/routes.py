from flask import render_template
from scholarship_portal import app
from scholarship_portal.forms import (
    ScholarshipForm,
    ApplicationForm,
    StudentLoginForm,
    StudentRegistrationForm,
)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/scholarship/new", methods=["GET", "POST"])
def new_scholarship():
    form = ScholarshipForm()
    return render_template(
        "newscholarship.html", title="Add New Scholarship", form=form
    )


@app.route("/scholarship/apply", methods=["GET", "POST"])
def apply_scholarship():
    form = ApplicationForm()
    return render_template(
        "applicationreg.html", form=form, title="Apply for Scholarship"
    )


@app.route("/student/registration", methods=["GET", "POST"])
def register_student():
    form = StudentRegistrationForm()
    return render_template("studentreg.html", form=form, title="Register")


@app.route("/student/login", methods=["GET", "POST"])
def login_student():
    form = StudentLoginForm()
    return render_template("studentlogin.html", form=form, title="Student Login")
