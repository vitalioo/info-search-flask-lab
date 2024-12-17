import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Инициализация приложения Flask
app = Flask(__name__)

# Конфигурация
app.config['SECRET_KEY'] = 'your_secret_key'  # Замените на ваш секретный ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'  # Путь к вашей базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация расширений
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Импорт маршрутов
import views  # Убедитесь, что этот импорт присутствует

@app.cli.command("create-db")
def create_db():
    """Создать все таблицы в базе данных."""
    with app.app_context():
        db.create_all()
    click.echo("Таблицы созданы.")
