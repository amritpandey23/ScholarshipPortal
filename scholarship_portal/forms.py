from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField,
    FloatField,
    DateField,
)
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from wtforms.widgets.core import SubmitInput

caste_list = [("null", "select"), ("open", "OPEN"), ("obc", "OBC"), ("scst", "SC/ST")]

gender_list = [("male", "MALE"), ("female", "FEMALE"), ("other", "OTHER")]

department_list = [
    ("CSE", "CSE"),
    ("ee", "EE"),
    ("ce", "CE"),
    ("ece", "ECE"),
    ("me", "ME"),
]

program_list = [
    ("mca", "MCA"),
    ("btech", "BTECH"),
    ("mtech", "MTECH"),
    ("MSC", "MSC"),
    ("Phd", "PHD"),
]


class ScholarshipForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired(), Length(max=120)])
    opening_date = DateField(label="Start Date")
    closing_date = DateField(label="Close Date")
    description = TextAreaField(label="Description")
    caste = SelectField("Caste Category", choices=caste_list)
    gender = SelectField("Gender Category", choices=gender_list)
    program = SelectField("Program", choices=program_list)
    department = SelectField("Department", choices=department_list)
    required_cgpa = FloatField(
        label="Minimum Required CGPA",
        validators=[
            NumberRange(min=3, max=10, message="CGPA must be between 3 and 10")
        ],
    )
    external_link = StringField(label="External link for application (if any)")
    submit = SubmitField(label="Add Scholarship")


class ApplicationForm(FlaskForm):
    name = StringField(label="Scholarship Name")
    stud_roll_no = IntegerField(label="Student Roll No")
    submit = SubmitField(label="Apply")


class StudentRegistrationForm(FlaskForm):
    roll_no = IntegerField(label="Roll No")
    name = StringField(label="Name")
    email = StringField(label="Email")
    password = PasswordField(label="Password")
    confirm_password = PasswordField(label="Confirm Password")
    branch = SelectField(label="Select Branch", choices=department_list)
    caste = SelectField(label="Caste", choices=caste_list)
    gender = SelectField(label="Gender", choices=gender_list)
    cgpa = FloatField(label="Current CGPA", validators=[NumberRange(min=3, max=10)])
    submit = SubmitField(label="Register")


class StudentLoginForm(FlaskForm):
    email = StringField(label="Email")
    password = PasswordField(label="Password")
    submit = SubmitField(label="Login")
