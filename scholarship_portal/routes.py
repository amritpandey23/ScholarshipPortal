from flask import render_template, flash, redirect, url_for
from flask.helpers import url_for
from werkzeug.utils import redirect
from scholarship_portal import app
from scholarship_portal.forms import (
    ScholarshipForm,
    ApplicationForm,
    StudentLoginForm,
    StudentRegistrationForm,
)
from scholarship_portal.models import Scholarship
from scholarship_portal import db
from slugify import slugify


@app.route("/")
def home():
    scholarships = Scholarship.query.all()
    return render_template("home.html", data=scholarships, title="All Scholarship")


@app.route("/scholarship/new", methods=["GET", "POST"])
def new_scholarship():
    form = ScholarshipForm()
    if form.validate_on_submit():
        sch = Scholarship(
            name=form.name.data,
            opening_date=form.opening_date.data,
            closing_date=form.closing_date.data,
            slug=slugify(form.name.data),
            description=form.description.data,
            caste=form.caste.data,
            gender=form.gender.data,
            program=form.program.data,
            department=form.department.data,
            required_cgpa=form.required_cgpa.data,
            external_link=form.external_link.data,
        )
        try:
            db.session.add(sch)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Something went wrong while adding Scholarship Details", "danger")
            return render_template(
                "newscholarship.html", title="Add New Scholarship", form=form
            )
        flash("Successfully added Scholarship", "success")
        return redirect(url_for("home"))
    return render_template(
        "newscholarship.html", title="Add New Scholarship", form=form
    )

@app.route("/scholarship/<sch_slug>", methods=["GET", "POST"])
def scholarship_present(sch_slug):
    sch = Scholarship.query.filter_by(slug=sch_slug).first()
    return render_template("scholarship.html", data=sch, title=f"Scholarship {sch.name}")

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
