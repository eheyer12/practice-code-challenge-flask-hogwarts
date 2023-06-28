#!/usr/bin/env python3
from models import db, Student, Subject, SubjectEnrollment
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Students(Resource):
    
    def get(self):
        students = Student.query.all()
        response_body = []
        for student in students:
            response_body.append(student.to_dict())
        return make_response(jsonify(response_body), 200)

api.add_resource(Students, "/students")

class StudentsById(Resource):
       
       def get(self, id):
        student = Student.query.filter(Student.id == id).first()
        response_body = student.to_dict()
        
        subject_enrollment_list = []
        for subject_enrollment in student.enrollment_subjects:
            subject_enrollment_dict = subject_enrollment.to_dict()
            subject_enrollment_dict.update({
                'subject': subject_enrollment.subject.to_dict()
            })
            subject_enrollment_list.append(subject_enrollment_dict)
        
        response_body.update({
            'subject_enrollments': subject_enrollment_list
        })

        return make_response(jsonify(response_body))

@app.route('/')
def home():
    return '<h1>🔮 Hogwarts Classes</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)
