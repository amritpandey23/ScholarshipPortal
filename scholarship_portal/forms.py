from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField,
    FloatField,
    MultipleFileField
)
from wtforms.fields.html5 import DateField
from wtforms.fields.core import BooleanField, IntegerField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email, NumberRange
from wtforms.widgets.core import SubmitInput

caste_list = [
    ("null", "select"),
    ("open", "OPEN"),
    ("obc", "OBC"),
    ("scst", "SC/ST"),
    ("ews", "EWS"),
]

gender_list = [("null", "select"),("male", "MALE"), ("female", "FEMALE"), ("other", "OTHER")]

department_list = [
    ("null", "select"),
    ("Computer Science and Engineering", "CSE"),
    ("Electrical Engineering", "EE"),
    ("Civil Engineering", "CE"),
    ("Electronics and Communication Engineering", "ECE"),
    ("Mechanical Engineering", "ME"),
]

program_list = [
    ("null", "select"),
    ("MCA", "MCA"),
    ("B.Tech", "BTECH"),
    ("M.Tech", "MTECH"),
    ("MSc.", "MSC"),
    ("Phd", "PHD"),
]


class ScholarshipForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired(), Length(max=120)])
    opening_date = DateField(label="Start Date")
    closing_date = DateField(label="Close Date")
    description = TextAreaField(label="Description")
    instructions = TextAreaField(label="Instructions")
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
    requires_caste_cert = BooleanField(label="Caste Certificate")
    requires_income_cert = BooleanField(label="Income Certificate")
    requires_resident_cert = BooleanField(label="Resident Certificate")
    requires_other_doc = BooleanField(label="Other Document")
    external_link = StringField(label="External link for application (if any)")
    submit = SubmitField(label="Add Scholarship")


class ApplicationForm(FlaskForm):
    name = StringField(label="Scholarship Name")
    stud_roll_no = IntegerField(label="Student Roll No")
    files = MultipleFileField(label="Upload Files")
    submit = SubmitField(label="Apply")


class StudentRegistrationForm(FlaskForm):
    roll_no = IntegerField(label="Roll No")
    name = StringField(label="Name")
    email = StringField(label="Email", validators=[Email()])
    password = PasswordField(label="Password")
    confirm_password = PasswordField(label="Confirm Password", validators=[EqualTo("password")])
    program = SelectField(label="Select Branch", choices=program_list)
    department = SelectField(label="Select Department", choices=department_list)
    caste = SelectField(label="Caste", choices=caste_list)
    gender = SelectField(label="Gender", choices=gender_list)
    cgpa = FloatField(label="Current CGPA", validators=[NumberRange(min=3, max=10)])
    submit = SubmitField(label="Register")


class StudentLoginForm(FlaskForm):
    email = StringField(label="Email")
    password = PasswordField(label="Password")
    submit = SubmitField(label="Login")
