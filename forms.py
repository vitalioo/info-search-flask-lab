from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import University
from datetime import datetime

# Форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтверждение пароля', validators=[
        DataRequired(),
        EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Зарегистрироваться')

    # Пользовательский валидатор для проверки уникальности имени пользователя
    def validate_username(self, username):
        from models import User
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Имя пользователя уже занято.')

# Форма входа
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

# Форма университета
class UniversityForm(FlaskForm):
    full_name = StringField('Полное название', validators=[DataRequired()])
    short_name = StringField('Сокращенное название', validators=[DataRequired()])
    established_date = DateField('Дата основания', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

# Форма студента
class StudentForm(FlaskForm):
    full_name = StringField('ФИО', validators=[DataRequired()])
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[DataRequired()])
    enrollment_year = IntegerField('Год поступления', validators=[DataRequired()])
    university_id = SelectField('Университет', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить')

    # Заполнение списка университетов в конструкторе формы
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.university_id.choices = [(u.id, u.short_name) for u in University.query.order_by('short_name')]
