from sqlalchemy.orm import relationship
from scholarship_portal import db


class Student(db.Model):
    __tablename__ = "student"
    roll_no = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    branch = db.Column(db.String(8), nullable=False)
    caste = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    department = db.Column(db.String(10), nullable=False)
    cgpa = db.Column(db.Float)
    applications = relationship("application")


class Application(db.Model):
    __tablename__ = "application"
    id = db.Column(db.Integer, primary_key=True)
    stud_roll_no = db.Column(db.Integer, db.ForeignKey("student.id"))
    status = db.Column(db.Boolean, nullable=False, default=False)


class Scholarship(db.Model):
    __tablename__ = "scholarship"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    stub = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    caste = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    department = db.Column(db.String(10), nullable=False)
    required_cgpa = db.Column(db.Float)


class AdminUser(db.Model):
    __tablename__ = "adminuser"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(250), nullable=False)
