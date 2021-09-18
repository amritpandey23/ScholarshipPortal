from flask import render_template, flash, redirect, url_for, request
from flask.helpers import url_for
from werkzeug.utils import redirect, secure_filename
from scholarship_portal import app
from scholarship_portal.forms import (
    ScholarshipForm,
    ApplicationForm,
    StudentLoginForm,
    StudentRegistrationForm,
)
from scholarship_portal.models import Scholarship, Student, Application, Document
from scholarship_portal import db, bcrypt
from slugify import slugify
from flask_login import current_user, login_user, logout_user, login_required
import os


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
@login_required
def apply_scholarship(sch_slug):
    sch = Scholarship.query.filter_by(slug=sch_slug).first()
    form = ApplicationForm()
    stud = current_user
    if (
        stud.gender != sch.gender
        or stud.caste != sch.caste
        or stud.program != sch.program
        or stud.department != sch.department
        or stud.cgpa < sch.required_cgpa
    ):
        flash(
            f"Sorry you are not eligible to apply for {sch.name} scholarship!", "danger"
        )
        return redirect(url_for("home"))
    if sch:
        if form.validate_on_submit():
            filenames = []
            for f in form.files.data:
                fname = secure_filename(f.filename)
                f.save(os.path.join(app.config["UPLOAD_FOLDER"], fname))
                filenames.append(fname)
            application = Application(
                app_name=form.name.data,
                stud_roll_no=int(form.stud_roll_no.data),
            )
            try:
                db.session.add(application)
                db.session.commit()
                for fname in filenames:
                    doc = Document(filename=fname, app_id=application.id)
                    db.session.add(doc)
                    db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
                flash(f"Some error occured on adding to database", "danger")
                return render_template(
                    "applicationreg.html",
                    form=form,
                    title=f"Apply for {sch.name}",
                    data=sch,
                )
            flash(f"Application completed successfully.", "success")
            return redirect(url_for("home"))
        return render_template(
            "applicationreg.html", form=form, title=f"Apply for {sch.name}", data=sch
        )

    flash("No such scholarship found")
    return redirect(url_for("home"))


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


@app.route("/login", methods=["GET", "POST"])
def login_student():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = StudentLoginForm()
    if form.validate_on_submit():
        stud = Student.query.filter_by(email=form.email.data).first()
        if stud and bcrypt.check_password_hash(stud.password, form.password.data):
            login_user(stud)
            next_page = request.args.get("next")
            flash(f"Welcome {stud.name}!", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful, please check email and password.")

    return render_template("studentlogin.html", form=form, title="Student Login")


@app.route("/logout", methods=["GET", "POST"])
def logout_student():
    logout_user()
    flash("You have logged out successfully.", "success")
    return redirect(url_for("home"))


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("profile.html", title="Profile Page")


@app.route("/track", methods=["GET"])
@login_required
def track():
    apps = Application.query.filter_by(stud_roll_no=current_user.roll_no).all()
    if len(apps) == 0:
        flash(f"No applications found.", "warning")
    return render_template("trackapp.html", data=apps, title="Track Application")
