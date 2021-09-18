from flask import render_template, flash, redirect, url_for, request
from flask.helpers import url_for
from werkzeug.utils import redirect
from scholarship_portal import app
from scholarship_portal.forms import (
    ScholarshipForm,
    ApplicationForm,
    StudentLoginForm,
    StudentRegistrationForm,
)
from scholarship_portal.models import Scholarship, Student
from scholarship_portal import db, bcrypt
from slugify import slugify
from flask_login import current_user, login_user, logout_user, login_required


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
            instructions=form.instructions.data,
            caste=form.caste.data,
            gender=form.gender.data,
            program=form.program.data,
            department=form.department.data,
            required_cgpa=form.required_cgpa.data,
            requires_caste_cert=form.requires_caste_cert.data,
            requires_income_cert=form.requires_income_cert.data,
            requires_resident_cert=form.requires_resident_cert.data,
            requires_other_doc=form.requires_other_doc.data,
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
    return render_template(
        "scholarship.html", data=sch, title=f"Scholarship {sch.name}"
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
    if form.validate_on_submit():
        student = Student(
            roll_no=form.roll_no.data,
            name=form.name.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode("utf-8"),
            program=form.program.data,
            caste=form.caste.data,
            gender=form.gender.data,
            department=form.department.data,
            cgpa=form.cgpa.data,
        )
        try:
            db.session.add(student)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Something went wrong while adding Student Details", "danger")
            return render_template("studentreg.html", form=form, title="Register")

        flash("Student added successfully!", "success")
        return redirect(url_for("home"))
    return render_template("studentreg.html", form=form, title="Register")


@app.route("/login", methods=["GET","POST"])
def login_student():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = StudentLoginForm()
    if form.validate_on_submit():
        stud = Student.query.filter_by(email=form.email.data).first()
        if stud and bcrypt.check_password_hash(stud.password, form.password.data):
            login_user(stud)
            next_page = request.args.get('next')
            flash(f"Welcome {stud.name}!", "success")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessful, please check email and password.")

    return render_template("studentlogin.html", form=form, title="Student Login")


@app.route("/logout", methods=["GET", "POST"])
def logout_student():
    logout_user()
    flash("You have logged out successfully.", "success")
    return redirect(url_for("home"))