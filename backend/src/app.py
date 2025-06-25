from flask import Flask
from flask_migrate import Migrate
from models.engine import db
from models.user import User
from models.role import Role
from routes.auth import auth_bp
from routes.vm_manage import vm_bp
from routes.admin import admin_bp
from routes.attacks import attacks_bp
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# def assign_role_to_user(user_identifier, role_name, db):
#     """
#     Назначает роль пользователю.

#     :param user_identifier: Строка или число — имя пользователя (username) или его ID.
#     :param role_name: Название роли (например, 'admin').
#     :param db: Экземпляр SQLAlchemy для работы с базой данных.
#     """
#     # Поиск роли по названию
#     role = Role.query.filter_by(name=role_name).first()
#     if not role:
#         raise ValueError(f"Role '{role_name}' does not exist")

#     # Определение, является ли user_identifier строкой (username) или числом (ID)
#     if isinstance(user_identifier, str):  # Если передано имя пользователя
#         user = User.query.filter_by(username=user_identifier).first()
#     elif isinstance(user_identifier, int):  # Если передан ID пользователя
#         user = User.query.get(user_identifier)
#     else:
#         raise ValueError("Invalid user identifier. Must be a string (username) or an integer (user ID).")

#     if not user:
#         raise ValueError(f"User '{user_identifier}' does not exist")

#     # Назначение роли пользователю
#     user.role = role
#     db.session.commit()



app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(attacks_bp)
app.register_blueprint(vm_bp)

# настройка политики CORS
CORS(app, origins=["http://localhost:3000"])  


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)