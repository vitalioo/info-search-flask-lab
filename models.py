from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db, login_manager
from datetime import date

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Модель пользователя для аутентификации
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Модель университета
class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    short_name = db.Column(db.String(50), nullable=False)
    established_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<University {self.short_name}>'

# Модель студента
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    enrollment_year = db.Column(db.Integer, nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)

    # Отношение для доступа к университету из студента
    university = db.relationship('University', backref=db.backref('students', lazy=True))

    def __repr__(self):
        return f'<Student {self.full_name}>'
