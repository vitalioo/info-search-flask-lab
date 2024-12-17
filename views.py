from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import User, University, Student
from forms import RegistrationForm, LoginForm, UniversityForm, StudentForm

# Главная страница
@app.route('/')
def home():
    return render_template('home.html')

# Регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Хешируем пароль пользователя
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        # Создаем нового пользователя
        new_user = User(username=form.username.data, password=hashed_password)
        # Добавляем в базу данных
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Вход пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Находим пользователя в базе данных
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            # Входим в систему
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неверное имя пользователя или пароль.', 'danger')
    return render_template('login.html', form=form)

# Выход пользователя
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('home'))

# Список университетов
@app.route('/universities')
def university_list():
    universities = University.query.order_by(University.short_name).all()
    return render_template('university_list.html', universities=universities)

# Создание университета
@app.route('/universities/create', methods=['GET', 'POST'])
@login_required
def university_create():
    form = UniversityForm()
    if form.validate_on_submit():
        new_university = University(
            full_name=form.full_name.data,
            short_name=form.short_name.data,
            established_date=form.established_date.data
        )
        db.session.add(new_university)
        db.session.commit()
        flash('Университет успешно создан!', 'success')
        return redirect(url_for('university_list'))
    return render_template('university_form.html', form=form)

# Обновление университета
@app.route('/universities/<int:id>/update', methods=['GET', 'POST'])
@login_required
def university_update(id):
    university = University.query.get_or_404(id)
    form = UniversityForm(obj=university)
    if form.validate_on_submit():
        university.full_name = form.full_name.data
        university.short_name = form.short_name.data
        university.established_date = form.established_date.data
        db.session.commit()
        flash('Университет успешно обновлен!', 'success')
        return redirect(url_for('university_list'))
    return render_template('university_form.html', form=form)

# Удаление университета
@app.route('/universities/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def university_delete(id):
    # Вместо get_object_or_404 используем get_or_404
    university = University.query.get_or_404(id)
    if request.method == 'POST':
        # Сначала удаляем всех студентов этого университета
        for student in university.students:
            db.session.delete(student)

        db.session.delete(university)
        db.session.commit()
        flash('Университет успешно удален!', 'success')
        return redirect(url_for('university_list'))
    return render_template('university_confirm_delete.html', university=university)

# Список студентов
@app.route('/students')
def student_list():
    students = Student.query.order_by(Student.full_name).all()
    return render_template('student_list.html', students=students)

# Создание студента
@app.route('/students/create', methods=['GET', 'POST'])
@login_required
def student_create():
    form = StudentForm()
    if form.validate_on_submit():
        new_student = Student(
            full_name=form.full_name.data,
            birth_date=form.birth_date.data,
            enrollment_year=form.enrollment_year.data,
            university_id=form.university_id.data
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Студент успешно создан!', 'success')
        return redirect(url_for('student_list'))
    return render_template('student_form.html', form=form)

# Обновление студента
@app.route('/students/<int:id>/update', methods=['GET', 'POST'])
@login_required
def student_update(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.full_name = form.full_name.data
        student.birth_date = form.birth_date.data
        student.enrollment_year = form.enrollment_year.data
        student.university_id = form.university_id.data
        db.session.commit()
        flash('Студент успешно обновлен!', 'success')
        return redirect(url_for('student_list'))
    return render_template('student_form.html', form=form)

# Удаление студента
@app.route('/students/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def student_delete(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(student)
        db.session.commit()
        flash('Студент успешно удален!', 'success')
        return redirect(url_for('student_list'))
    return render_template('student_confirm_delete.html', student=student)
