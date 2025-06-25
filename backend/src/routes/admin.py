from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.engine import db
from models.role import Role
from models.user import User
import os
import psutil
#пересмотреть список подключаемых библиотек

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/create-user', methods=['POST'])
@jwt_required()  # Требуется JWT-токен для доступа
def admin_create_user():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    # Проверяем, является ли текущий пользователь администратором
    if current_user.role.name != 'admin':
        return jsonify(msg="Admin access required"), 403
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'admin':
        return jsonify(msg='Only one user in system!'), 400


    # Проверяем, существует ли пользователь с таким именем
    if User.query.filter_by(username=username).first():
        return jsonify(msg='User already exists'), 400

    # Находим роль 'user'
    user_role = Role.query.filter_by(name='user').first()
    if not user_role:
        return jsonify(msg="User role not found"), 500
    
    new_user = User(
        username=username,
        role=user_role
        )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(msg=f'User {username} created successfully'), 201
    