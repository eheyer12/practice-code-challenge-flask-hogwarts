from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Student(db.Model, SerializerMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String)

    # Add relationship
    subject_enrollments = db.relationship('SubjectEnrollment', back_populates='student', cascade='all, delete-orphan')
    subjects = association_proxy('subject_enrollments', 'subject', creator=lambda j: SubjectEnrollment(subject = j))

    # Add serialization
    serialize_rules = ("-subject_enrollments",)

    # Add validation
    @validates('age')
    def validates_age(self, key, value):
        if not (11 <= value <= 18):
            raise ValueError(f"Must have {key} between 11 and 18.")
        return value
    
    def __repr__(self):
        return f'<Student {self.id}>'

class Subject(db.Model, SerializerMixin):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    # Add relationship
    subject_enrollments = db.relationship('SubjectEnrollment', back_populates='subject', cascade='all, delete-orphan')
    students = association_proxy('subject_enrollments', 'student', creator=lambda t: SubjectEnrollment(student = t))

    # Add serialization
    serialize_rules = ('-subject_enrollments',)

    def __repr__(self):
        return f'<Subject {self.id}>'

class SubjectEnrollment(db.Model, SerializerMixin):
    __tablename__ = 'subject_enrollments'

    id = db.Column(db.Integer, primary_key=True)
    enrollment_year = db.Column(db.Integer, nullable=False)

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))

    # Add relationships
    student  = db.relationship("Student", back_populates="subject_enrollments")
    subject = db.relationship("Subject", back_populates='subject_enrollments')
    
    # Add serialization
    serialize_rules = ('-student', '-subject')

    # Add validation
    @validates('enrollment_year')
    def validates_enrollment_year(self, key, value):
        if not (value > 2023):
            raise ValueError(f'Must have an {key} before 2023.')
        return value

    def __repr__(self):
        return f'<SubjectEnrollment {self.id}>'


