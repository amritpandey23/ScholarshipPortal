import json
import os
try:
    config_file = open("config.json", "r")
    config = json.load(config_file)
    config_file.close()
    if config["setup_complete"] == True:
        print("Setup is already done!")
        exit()
except Exception as e:
    print(e)
from shutil import copyfile
try:
    copyfile("example.config.json", "config.json")
except Exception as e:
    print(e)
    
from scholarship_portal import db, bcrypt
from scholarship_portal.models import Student

db.drop_all()
db.create_all()
admin = Student(
    roll_no = 0,
    name = "Admin",
    email = "admin@portal.com",
    password = bcrypt.generate_password_hash("root").decode("utf-8"),
    program = "null",
    caste = "null",
    gender = "null",
    department = "null",
    is_admin = True,
    cgpa = 3
)
db.session.add(admin)
db.session.commit()
db.session.close()

os.mkdir("uploads")

config_file = open("config.json", "r")
config = json.load(config_file)
config_file.close()
config["setup_complete"] = True
config_file = open("config.json", "w")
json.dump(config, config_file)
config_file.close()